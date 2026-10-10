import { useCallback, useEffect, useRef, useState } from 'react';
import {
  ROLE_LABELS,
  approveMessage,
  getCaseDetail,
  getSession,
  importBuildCase,
  listCases,
  rejectMessage,
  respondToReview,
  reviewPolicySuggestion,
  runTimers,
  type Role,
} from './lib/api';
import type { CaseDetail, CaseListItem, ReviewResponseInput, SessionInfo } from './lib/types';
import {
  computeActions,
  computeDetailedPipeline,
  computeStageRows,
  formatTime,
  primaryResolution,
  readableFactKey,
  reviewForTopBlocker,
  severityOf,
  stagePillOf,
  toCaseSummaryVM,
  translateActivity,
} from './lib/pipeline';
import type { ActionKey, CaseSummaryVM, Severity } from './components/dashboard-types';
import CaseList from './components/CaseList';
import RightPanel from './components/RightPanel';
import Pipeline from './components/Pipeline';
import StageDetailCard from './components/StageDetailCard';
import PolicyEngine, { type PolicyRequest } from './components/PolicyEngine';
import MessageDrafts from './components/MessageDrafts';

/** The workflow advances cases in the background (routing, Claude reading,
 * drafting, timers), so the dashboard polls for the latest state. */
const POLL_MS = 4000;

const WORKFLOW_LABELS: Record<string, string> = {
  native_local: 'Native workflow · local',
  native_cloud: 'Native workflow · Vercel',
  manual_demo: 'Manual demo mode',
};

/** A curated spread of BUILD cases (varied category/complexity/event-count)
 * loaded on request so the dashboard has enough variety to demo — real
 * imports via the real API, not fabricated data. Loading twice won't
 * duplicate: we check the existing case titles first (BUILD imports are
 * titled "BUILD {id} · through event {n}"). */
const SEED_CASES: [buildId: string, eventCount: number][] = [
  ['013', 2],
  ['016', 2],
  ['017', 3],
  ['021', 2],
  ['023', 4],
  ['027', 1],
  ['028', 2],
  ['034', 3],
  ['049', 2],
];

const SEVERITY_BADGE: Record<Severity, string> = {
  red: 'bg-[var(--color-danger-bg)] text-[var(--color-danger)]',
  amber: 'bg-[var(--color-attention-bg)] text-[var(--color-attention)]',
  green: 'bg-[var(--color-success-bg)] text-[var(--color-success)]',
};

async function seedCasesIfNeeded(existing: CaseListItem[]): Promise<void> {
  const alreadyImported = (buildId: string) =>
    existing.some((c) => c.title.includes(`BUILD ${buildId} ·`));
  const toImport = SEED_CASES.filter(([buildId]) => !alreadyImported(buildId));
  for (const [buildId, eventCount] of toImport) {
    try {
      await importBuildCase(buildId, eventCount);
    } catch {
      // A single bad seed case shouldn't block the rest of the dashboard.
    }
  }

  // Genuinely reject the first couple of freshly-seeded cases' top review so
  // the dashboard has real "Blocked" (red) cases to show, rather than every
  // seed landing in the same amber "needs verification" state. This is a
  // real state transition through the real API, not a cosmetic label.
  if (toImport.length > 0) {
    const refreshed = await listCases();
    const freshlySeeded = refreshed.filter((c) =>
      toImport.some(([buildId]) => c.title.includes(`BUILD ${buildId} ·`)),
    );
    for (const item of freshlySeeded.slice(0, 2)) {
      try {
        const detail = await getCaseDetail(item.id);
        const topBlocker = detail.decision?.blockers[0];
        const review = detail.reviews.find(
          (r) => r.rule_id === topBlocker?.rule_id && r.status === 'open',
        );
        if (review) {
          await respondToReview(review.id, review.owner as Role, {
            decision: 'reject',
            reason: 'Flagged for escalation during demo seeding',
          });
        }
      } catch {
        // Non-critical — the case just stays amber instead of red.
      }
    }
  }
}

function App() {
  const [cases, setCases] = useState<CaseListItem[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [selectedDetail, setSelectedDetail] = useState<CaseDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [responding, setResponding] = useState(false);
  const [seeding, setSeeding] = useState(false);
  const [session, setSession] = useState<SessionInfo | null>(null);
  const [lastSync, setLastSync] = useState<Date | null>(null);
  const [syncError, setSyncError] = useState(false);

  const [view, setView] = useState<'operations' | 'policies'>('operations');
  // Human-in-the-loop: after a decision, the backend policy assistant may
  // offer a conservative reusable rule built from that review.
  const [policySuggestion, setPolicySuggestion] = useState<{ text: string; reviewId: string } | null>(
    null,
  );
  const [policyRequest, setPolicyRequest] = useState<PolicyRequest | null>(null);

  // Refs let the polling loop read the latest selection and skip a tick
  // while a mutation is in flight.
  const selectedIdRef = useRef<string | null>(null);
  const busyRef = useRef(false);
  useEffect(() => {
    selectedIdRef.current = selectedId;
  }, [selectedId]);
  useEffect(() => {
    busyRef.current = responding || seeding;
  }, [responding, seeding]);

  const refresh = useCallback(async () => {
    const list = await listCases();
    setCases(list);
    const id = selectedIdRef.current;
    if (id) {
      const detail = await getCaseDetail(id);
      // Ignore a late response for a case the user has since left.
      if (selectedIdRef.current === id) setSelectedDetail(detail);
    }
    setLastSync(new Date());
    setSyncError(false);
    return list;
  }, []);

  useEffect(() => {
    let cancelled = false;
    async function bootstrap() {
      try {
        setSession(await getSession());
        const list = await listCases();
        if (cancelled) return;
        setCases(list);
        setLastSync(new Date());
        // Open on a case that genuinely needs a human decision, so the
        // "Action required" hero is the first thing on screen — fall back to
        // the first case if none are pending review.
        const firstPending = list.find(
          (c) => c.outcome === 'HUMAN REVIEW' || c.outcome === 'CLARIFY',
        );
        setSelectedId(firstPending?.id ?? list[0]?.id ?? null);
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    bootstrap();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!selectedId) {
      setSelectedDetail(null);
      return;
    }
    let cancelled = false;
    getCaseDetail(selectedId)
      .then((detail) => {
        if (!cancelled) setSelectedDetail(detail);
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Unknown error');
      });
    return () => {
      cancelled = true;
    };
  }, [selectedId]);

  // Live view of background workflow progress.
  useEffect(() => {
    if (loading) return;
    const timer = window.setInterval(() => {
      if (document.hidden || busyRef.current) return;
      refresh().catch(() => setSyncError(true));
    }, POLL_MS);
    return () => window.clearInterval(timer);
  }, [loading, refresh]);

  async function loadDemoCases() {
    setSeeding(true);
    setActionError(null);
    try {
      await seedCasesIfNeeded(await listCases());
      const list = await refresh();
      if (!selectedIdRef.current) {
        const firstPending = list.find((c) => c.outcome === 'HUMAN REVIEW' || c.outcome === 'CLARIFY');
        setSelectedId(firstPending?.id ?? list[0]?.id ?? null);
      }
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Could not load demo cases');
    } finally {
      setSeeding(false);
    }
  }

  /** Run a case mutation, show its result at once, then pick up whatever the
   * workflow does next on the following poll. */
  async function mutate(call: () => Promise<CaseDetail>): Promise<CaseDetail | null> {
    setResponding(true);
    setActionError(null);
    try {
      const updated = await call();
      setSelectedDetail(updated);
      setCases(await listCases());
      return updated;
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Unknown error');
      return null;
    } finally {
      setResponding(false);
    }
  }

  async function handleAction(key: ActionKey) {
    if (!selectedDetail?.decision || responding) return;
    const review = reviewForTopBlocker(selectedDetail);
    if (!review) {
      setActionError('No open review found for this blocker — it may already be resolved.');
      return;
    }
    const primary = primaryResolution(selectedDetail, review);
    const dayFromNow = new Date(Date.now() + 24 * 3600 * 1000).toISOString();

    let body: ReviewResponseInput;
    switch (key) {
      case 'approve':
        body = {
          decision: 'approve',
          reason: 'Approved via staff dashboard',
          source_id: review.source_ids[0] ?? selectedDetail.evidence[0]?.id,
          expires_at: dayFromNow,
          scope: selectedDetail.decision.scope,
        };
        break;
      case 'verify': {
        const claim = primary?.claim;
        if (!claim) return;
        body = {
          decision: 'correct',
          reason: 'Verified against the quoted source via staff dashboard',
          claim_id: claim.id,
          source_id: claim.source_id,
          key: review.key,
        };
        break;
      }
      case 'defer':
        body = { decision: 'defer', reason: 'Deferred via staff dashboard', deadline: dayFromNow };
        break;
      case 'reject':
        body = { decision: 'reject', reason: 'Rejected via staff dashboard' };
        break;
      case 'more_evidence':
        body = { decision: 'more_evidence', reason: 'Requested more information via staff dashboard' };
        break;
    }

    setPolicySuggestion(null);
    // Each review belongs to one role (app/service.py respond); act as it.
    const updated = await mutate(() => respondToReview(review.id, review.owner as Role, body));
    if (!updated || (key !== 'approve' && key !== 'reject')) return;
    // A committed human decision is the kind of judgement worth turning into a
    // reusable rule. The backend assistant suggests one only where that is safe.
    try {
      const suggestion = await reviewPolicySuggestion(review.id);
      if (suggestion.suggested_text) {
        setPolicySuggestion({ text: suggestion.suggested_text, reviewId: review.id });
      }
    } catch {
      // No suggestion is fine; the decision itself already succeeded.
    }
  }

  if (error) {
    return (
      <div className="flex h-screen items-center justify-center bg-[var(--color-canvas)] p-6">
        <div className="max-w-md rounded-[var(--radius-md)] border border-[var(--color-danger)] bg-[var(--color-danger-bg)] p-4 text-sm text-[var(--color-danger)]">
          {error}
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-[var(--color-canvas)]">
        <p className="text-sm text-[var(--color-muted)]">Loading dashboard…</p>
      </div>
    );
  }

  const summaries: CaseSummaryVM[] = cases.map(toCaseSummaryVM);
  const selectedSummary = cases.find((c) => c.id === selectedId);
  const inProgress = summaries.filter((s) => s.severity !== 'green' && s.id !== selectedId);
  const finishedToday = summaries.filter((s) => s.resolvedInHours !== undefined);
  const stats = {
    active: cases.filter((c) => c.outcome !== 'NO FURTHER ACTION').length,
    escalations: cases.filter((c) => c.outcome === 'STOP ACTION').length,
    resolvedToday: cases.filter((c) => c.outcome === 'NO FURTHER ACTION').length,
  };

  const selectedSeverity = selectedSummary ? severityOf(selectedSummary) : 'amber';
  const pipelineNodes = selectedDetail ? computeDetailedPipeline(selectedDetail) : [];
  const stageRows = selectedDetail ? computeStageRows(selectedDetail) : [];
  const { actions, disabledNote } = selectedDetail
    ? computeActions(selectedDetail)
    : { actions: [], disabledNote: undefined };
  // Approve is promoted to the hero callout; the detail-card row keeps only
  // the secondary responses (Request more info / Defer / Reject).
  const detailActions = actions.filter((a) => a.key !== 'approve');
  const activity = selectedDetail ? translateActivity(selectedDetail.timeline) : [];
  const currentStageLabel =
    pipelineNodes.find((n) => n.state === 'current')?.label ??
    (selectedSummary ? stagePillOf(selectedSummary) : '');

  // A case "needs a decision" when its current assessment is held for a human
  // (anything other than ready-to-act or already resolved). This drives the
  // amber hero callout.
  const topBlocker = selectedDetail?.decision?.blockers[0];
  const topReview = selectedDetail ? reviewForTopBlocker(selectedDetail) : undefined;
  const primary = selectedDetail && topReview ? primaryResolution(selectedDetail, topReview) : undefined;
  const needsDecision = Boolean(
    topReview &&
      topBlocker &&
      (topBlocker.response === 'HUMAN REVIEW' || topBlocker.response === 'CLARIFY'),
  );

  return (
    <div className="flex h-screen w-screen flex-col overflow-hidden bg-[var(--color-canvas)] font-[var(--font-body)] text-[var(--color-ink)]">
      <nav className="flex h-12 shrink-0 items-center justify-between border-b border-[var(--color-border)] bg-[var(--color-surface)] px-5">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2.5">
            <span
              className="h-2 w-2 rounded-full bg-[var(--color-primary)]"
              style={{ boxShadow: '0 0 6px rgba(33,88,72,.5)', animation: 'dot-pulse 2.2s ease-out infinite' }}
            />
            <span className="text-[15px] font-semibold tracking-[-0.2px] text-[var(--color-ink)]">
              Property Desk
            </span>
          </div>
          <div className="flex items-center gap-1 rounded-[var(--radius-sm)] bg-[var(--color-canvas)] p-0.5">
            {(['operations', 'policies'] as const).map((v) => (
              <button
                key={v}
                type="button"
                onClick={() => setView(v)}
                className="rounded-[5px] px-3 py-1 text-[12px] font-medium transition-colors"
                style={
                  view === v
                    ? { background: 'var(--color-surface)', color: 'var(--color-ink)', boxShadow: '0 1px 2px rgba(25,44,48,.08)' }
                    : { background: 'transparent', color: 'var(--color-muted)' }
                }
              >
                {v === 'operations' ? 'Operations' : 'Policies'}
              </button>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={() => refresh().catch(() => setSyncError(true))}
            title="Refresh now"
            className="flex items-center gap-1.5 text-[11px] text-[var(--color-muted)] hover:text-[var(--color-ink)]"
          >
            <span
              className="h-1.5 w-1.5 rounded-full"
              style={{ background: syncError ? 'var(--color-danger)' : 'var(--color-success)' }}
            />
            {syncError ? 'Backend unreachable — retrying' : `Live · ${formatTime(lastSync?.toISOString()) ?? '—'}`}
          </button>
          {session && (
            <span className="text-[11px] text-[var(--color-muted)]">
              {WORKFLOW_LABELS[session.workflow_mode] ?? session.workflow_mode} · Claude{' '}
              {session.model.credential_configured ? 'connected' : 'not configured'}
            </span>
          )}
          <span
            className="rounded-full border px-3 py-1 text-[11px] font-medium"
            style={{
              background: 'rgba(33,88,72,.08)',
              color: '#215848',
              borderColor: 'rgba(33,88,72,.2)',
            }}
          >
            Local demonstration — no real actions taken
          </span>
        </div>
      </nav>

      {view === 'policies' ? (
        <div className="min-h-0 flex-1 overflow-y-auto">
          <PolicyEngine
            request={policyRequest}
            onPublished={() => {
              refresh().catch(() => setSyncError(true));
            }}
          />
        </div>
      ) : (
      <div className="flex min-h-0 flex-1">
        <div className="w-[260px] shrink-0 border-r border-[var(--color-border)] bg-[var(--color-sidebar)]">
          <CaseList cases={summaries} selectedId={selectedId} onSelect={setSelectedId} />
        </div>

        <div className="flex min-h-0 flex-1 flex-col">
          <div className="flex h-12 shrink-0 items-center justify-between border-b border-[var(--color-border)] px-4">
            {selectedSummary ? (
              <>
                <span className="truncate text-[13px] text-[var(--color-ink)]">
                  {selectedSummary.property_ref}
                  <span className="text-[var(--color-muted)]"> · {selectedSummary.category}</span>
                </span>
                <span className="flex shrink-0 items-center gap-3">
                  <button
                    type="button"
                    disabled={responding}
                    onClick={() => void mutate(() => runTimers(selectedSummary.id))}
                    title="Process due reminders, escalations and review deadlines now"
                    className="text-[11px] font-medium text-[var(--color-muted)] hover:text-[var(--color-ink)] disabled:opacity-50"
                  >
                    Run due timers
                  </button>
                  <span
                    className={`rounded-full px-2.5 py-1 text-[11px] font-medium ${SEVERITY_BADGE[selectedSeverity]}`}
                  >
                    {stagePillOf(selectedSummary)}
                  </span>
                </span>
              </>
            ) : (
              <span className="text-[13px] text-[var(--color-muted)]">No case selected</span>
            )}
          </div>

          <div className="flex-1 overflow-y-auto px-6 py-6">
            {selectedDetail ? (
              <>
                <MessageDrafts
                  messages={selectedDetail.tenant_messages ?? []}
                  busy={responding}
                  onSend={(id, text) => void mutate(() => approveMessage(id, text))}
                  onReject={(id, reason, redraft) => void mutate(() => rejectMessage(id, reason, redraft))}
                />

                {needsDecision && selectedSummary && topReview && (
                  <div
                    className="mb-5 rounded-[var(--radius-md)] px-5 py-4"
                    style={{
                      borderLeft: '4px solid #865719',
                      background: '#FBF1DF',
                    }}
                  >
                    <p className="text-[11px] font-bold uppercase tracking-wide text-[var(--color-attention)]">
                      ⚠ Action required
                    </p>
                    <p className="mt-1.5 text-[14px] font-semibold text-[var(--color-ink)]">
                      {selectedSummary.property_ref}
                    </p>
                    <p className="mt-0.5 text-[13px] text-[var(--color-ink)]/80">
                      {readableFactKey(topReview.key)}: {selectedDetail.decision?.next_step}
                    </p>
                    {primary ? (
                      <>
                        <p className="mt-2 text-[12px] italic text-[var(--color-ink)]/70">
                          {primary.explanation}
                        </p>
                        <div className="mt-3 flex items-center gap-3">
                          <button
                            type="button"
                            onClick={() => handleAction(primary.key)}
                            disabled={responding}
                            className="rounded-[var(--radius-sm)] bg-[var(--color-primary)] px-5 py-2.5 text-[13px] font-semibold text-white transition-colors hover:bg-[var(--color-primary-hover)] disabled:opacity-60"
                          >
                            {primary.label}
                          </button>
                          <span className="text-[11px] text-[var(--color-attention)]">
                            as {ROLE_LABELS[topReview.owner] ?? topReview.owner} (demo role)
                          </span>
                        </div>
                      </>
                    ) : (
                      <p className="mt-2 text-[11px] text-[var(--color-attention)]">
                        Nothing on file can settle this yet — request more information, defer or
                        reject below.
                      </p>
                    )}
                  </div>
                )}

                <div className="mb-8 flex justify-center">
                  <Pipeline nodes={pipelineNodes} />
                </div>
                {actionError && (
                  <div className="mb-3 rounded-[var(--radius-md)] border border-[var(--color-danger)] bg-[var(--color-danger-bg)] px-4 py-3 text-sm text-[var(--color-danger)]">
                    {actionError}
                  </div>
                )}
                <StageDetailCard
                  stageTitle={currentStageLabel}
                  rows={stageRows}
                  actions={detailActions}
                  onAction={handleAction}
                  disabledNote={disabledNote}
                  activity={activity}
                />

                {policySuggestion !== null && (
                  <PolicySuggestion
                    value={policySuggestion.text}
                    onChange={(text) => setPolicySuggestion({ ...policySuggestion, text })}
                    onAdd={(text) => {
                      setPolicyRequest({ text, reviewId: policySuggestion.reviewId, nonce: Date.now() });
                      setPolicySuggestion(null);
                      setView('policies');
                    }}
                    onDismiss={() => setPolicySuggestion(null)}
                  />
                )}
              </>
            ) : cases.length === 0 ? (
              <div className="mx-auto mt-16 max-w-sm text-center">
                <p className="text-[15px] font-semibold text-[var(--color-ink)]">No cases yet</p>
                <p className="mt-1 text-[13px] text-[var(--color-muted)]">
                  Cases arrive from the tenant portal, or load nine replayed BUILD cases into this
                  local demo store.
                </p>
                <button
                  type="button"
                  onClick={() => void loadDemoCases()}
                  disabled={seeding}
                  className="mt-4 rounded-[var(--radius-sm)] bg-[var(--color-primary)] px-5 py-2.5 text-[13px] font-semibold text-white transition-colors hover:bg-[var(--color-primary-hover)] disabled:opacity-60"
                >
                  {seeding ? 'Loading demo cases…' : 'Load demo cases'}
                </button>
                {actionError && (
                  <p className="mt-3 text-[12px] text-[var(--color-danger)]">{actionError}</p>
                )}
              </div>
            ) : (
              <p className="text-sm text-[var(--color-muted)]">Select a case to see its pipeline.</p>
            )}
          </div>
        </div>

        <div className="w-[220px] shrink-0 border-l border-[var(--color-border)] bg-[var(--color-sidebar)]">
          <RightPanel stats={stats} inProgress={inProgress} finishedToday={finishedToday} />
        </div>
      </div>
      )}
    </div>
  );
}

/** Human-in-the-loop capture card: shown after an approval, lets the operator
 * turn the decision into a reusable AI-learned policy. */
function PolicySuggestion({
  value,
  onChange,
  onAdd,
  onDismiss,
}: {
  value: string;
  onChange: (v: string) => void;
  onAdd: (text: string) => void;
  onDismiss: () => void;
}) {
  return (
    <div
      className="mt-4 rounded-[var(--radius-md)] border p-4"
      style={{ borderColor: 'var(--color-border)', background: 'var(--color-information-bg)' }}
    >
      <p className="text-[13px] font-semibold text-[var(--color-ink)]">Add this as a policy?</p>
      <p className="mt-0.5 text-[12px] text-[var(--color-muted)]">
        The policy assistant suggests a reusable rule from this decision. You preview its impact
        before anything is published.
      </p>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="mt-3 w-full rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] px-3.5 py-2.5 text-[13px] text-[var(--color-ink)] outline-none focus:border-[var(--color-primary)]"
      />
      <div className="mt-3 flex gap-2">
        <button
          type="button"
          onClick={() => onAdd(value.trim())}
          disabled={!value.trim()}
          className="rounded-[var(--radius-sm)] bg-[var(--color-primary)] px-4 py-2 text-[13px] font-semibold text-white transition-colors hover:bg-[var(--color-primary-hover)] disabled:opacity-50"
        >
          Draft in Policy Engine
        </button>
        <button
          type="button"
          onClick={onDismiss}
          className="rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-transparent px-4 py-2 text-[13px] font-medium text-[var(--color-ink)] transition-colors hover:bg-[var(--color-canvas)]"
        >
          Not now
        </button>
      </div>
    </div>
  );
}

export default App;
