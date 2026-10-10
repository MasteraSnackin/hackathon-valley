import { useEffect, useState } from 'react';
import {
  createDemoSession,
  getCaseDetail,
  importBuildCase,
  listCases,
  respondToReview,
} from './lib/api';
import type { CaseDetail, CaseListItem } from './lib/types';
import {
  computeActions,
  computeDetailedPipeline,
  computeStageRows,
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

/** A curated spread of BUILD cases (varied category/complexity/event-count)
 * seeded once so the dashboard has enough variety to demo — real imports via
 * the real API, not fabricated data. Re-running the app won't re-seed: we
 * check the existing case titles first (BUILD imports are titled
 * "BUILD {id} · through event {n}"). */
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

/** Module-level guard so React 18 StrictMode's dev-only double-invoke of
 * this effect (mount → unmount → mount) can't race two parallel seed runs
 * that both read the same pre-seed case list and both import the same
 * BUILD cases. Real double page-loads will still race (acceptable for a
 * local demo); this only needs to survive a single page's lifecycle. */
let bootstrapPromise: Promise<CaseListItem[]> | null = null;
function ensureBootstrapped(): Promise<CaseListItem[]> {
  if (!bootstrapPromise) {
    bootstrapPromise = (async () => {
      const initial = await listCases();
      await seedCasesIfNeeded(initial);
      return listCases();
    })();
  }
  return bootstrapPromise;
}

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
          await respondToReview(review.id, {
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

  useEffect(() => {
    let cancelled = false;
    async function bootstrap() {
      try {
        await createDemoSession('case_manager');
        const finalList = await ensureBootstrapped();
        if (cancelled) return;
        setCases(finalList);
        // Open on a case that genuinely needs a human decision, so the
        // "Action required" hero is the first thing on screen — fall back to
        // the first case if none are pending review.
        const firstPending = finalList.find(
          (c) => c.outcome === 'HUMAN REVIEW' || c.outcome === 'CLARIFY',
        );
        setSelectedId(firstPending?.id ?? finalList[0]?.id ?? null);
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
    if (!selectedId) return;
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

  async function handleAction(key: ActionKey) {
    if (!selectedDetail?.decision || responding) return;
    const topBlocker = selectedDetail.decision.blockers[0];
    if (!topBlocker) return;
    const review = selectedDetail.reviews.find(
      (r) => r.rule_id === topBlocker.rule_id && r.status === 'open',
    );
    if (!review) {
      setActionError('No open review found for this blocker — it may already be resolved.');
      return;
    }

    const reasonByKey: Record<ActionKey, string> = {
      approve: 'Approved via ops dashboard',
      reject: 'Rejected via ops dashboard',
      defer: 'Deferred via ops dashboard',
      more_evidence: 'Requested more information via ops dashboard',
    };
    const body: Parameters<typeof respondToReview>[1] = {
      decision: key,
      reason: reasonByKey[key],
    };
    if (key === 'approve') {
      body.source_id = selectedDetail.evidence[0]?.id;
      body.expires_at = new Date(Date.now() + 24 * 3600 * 1000).toISOString();
      body.scope = selectedDetail.decision.scope;
    }
    if (key === 'defer') {
      body.deadline = new Date(Date.now() + 24 * 3600 * 1000).toISOString();
    }

    setResponding(true);
    setActionError(null);
    try {
      const updated = await respondToReview(review.id, body);
      setSelectedDetail(updated);
      const refreshed = await listCases();
      setCases(refreshed);
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setResponding(false);
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
  const needsDecision = Boolean(
    topBlocker &&
      (topBlocker.response === 'HUMAN REVIEW' || topBlocker.response === 'CLARIFY'),
  );
  const canApprove = topBlocker?.key === 'authority' || topBlocker?.key === 'finance';

  return (
    <div className="flex h-screen w-screen flex-col overflow-hidden bg-[var(--color-canvas)] font-[var(--font-body)] text-[var(--color-ink)]">
      <nav className="flex h-12 shrink-0 items-center justify-between border-b border-[var(--color-border)] bg-[var(--color-surface)] px-5">
        <div className="flex items-center gap-2.5">
          <span
            className="h-2 w-2 rounded-full bg-[var(--color-primary)]"
            style={{ boxShadow: '0 0 6px rgba(33,88,72,.5)', animation: 'dot-pulse 2.2s ease-out infinite' }}
          />
          <span className="text-[15px] font-semibold tracking-[-0.2px] text-[var(--color-ink)]">
            Property Desk
          </span>
          <span className="text-[13px] text-[var(--color-muted)]">· Maintenance operations</span>
        </div>
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
      </nav>

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
                <span
                  className={`shrink-0 rounded-full px-2.5 py-1 text-[11px] font-medium ${SEVERITY_BADGE[selectedSeverity]}`}
                >
                  {stagePillOf(selectedSummary)}
                </span>
              </>
            ) : (
              <span className="text-[13px] text-[var(--color-muted)]">No case selected</span>
            )}
          </div>

          <div className="flex-1 overflow-y-auto px-6 py-6">
            {selectedDetail ? (
              <>
                {needsDecision && selectedSummary && (
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
                      {selectedDetail.decision?.next_step}
                    </p>
                    <button
                      type="button"
                      onClick={() => handleAction('approve')}
                      disabled={responding}
                      className="mt-3 rounded-[var(--radius-sm)] bg-[var(--color-primary)] px-5 py-2.5 text-[13px] font-semibold text-white transition-colors hover:bg-[var(--color-primary-hover)] disabled:opacity-60"
                    >
                      {canApprove ? 'Approve & assign contractor' : 'Approve this action'}
                    </button>
                    {!canApprove && (
                      <p className="mt-2 text-[11px] text-[var(--color-attention)]">
                        This review needs the underlying source verified rather than a general
                        approval — use the responses below.
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
              </>
            ) : (
              <p className="text-sm text-[var(--color-muted)]">Select a case to see its pipeline.</p>
            )}
          </div>
        </div>

        <div className="w-[220px] shrink-0 border-l border-[var(--color-border)] bg-[var(--color-sidebar)]">
          <RightPanel stats={stats} inProgress={inProgress} finishedToday={finishedToday} />
        </div>
      </div>
    </div>
  );
}

export default App;
