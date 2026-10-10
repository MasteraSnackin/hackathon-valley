import { useCallback, useEffect, useRef, useState } from 'react';
import { approveMessage, createDemoSession, evaluateCase, getCaseDetail, getSession, importBuildCase, listCases, rejectMessage, respondToReview, runTimers } from './lib/api';
import type { CaseDetail, CaseListItem, Review, ReviewResponseInput, SessionInfo } from './lib/types';
import { computeDetailedPipeline, computeStageRows, readableRole, severityOf, stagePillOf, toCaseSummaryVM, translateActivity } from './lib/pipeline';
import CaseList from './components/CaseList';
import RightPanel from './components/RightPanel';
import Pipeline from './components/Pipeline';
import StageDetailCard from './components/StageDetailCard';
import PolicyEngine, { type PolicyRequest } from './components/PolicyEngine';
import { reviewPolicySuggestion } from './lib/policy-api';
import MessageDrafts from './components/MessageDrafts';
import CaseReviewPanel from './components/CaseReviewPanel';

/** Only these chronological BUILD prefixes are imported, after an explicit click. */
const DEMO_CASES: [string, number][] = [['013', 2], ['016', 2], ['017', 3], ['021', 2], ['023', 4], ['027', 1], ['028', 2], ['034', 3], ['049', 2]];
const BUTTON = 'rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2 text-sm font-medium hover:bg-[var(--color-canvas)] disabled:cursor-not-allowed disabled:opacity-50';
const originalWorkspace = import.meta.env.VITE_ORIGINAL_WORKSPACE_URL || (import.meta.env.DEV ? 'http://127.0.0.1:8017/' : '/');
const WORKFLOW_LABELS: Record<string, string> = { native_local: 'Native workflow · local', native_cloud: 'Native workflow · Vercel', manual_demo: 'Manual demo mode' };
let sessionPromise: ReturnType<typeof getSession> | null = null;
function initialiseSession() {
  if (!sessionPromise) sessionPromise = (async () => {
    let session = await getSession();
    if (!session.actor && session.mode === 'demo') { await createDemoSession('case_manager'); session = await getSession(); }
    return session;
  })().finally(() => { sessionPromise = null; });
  return sessionPromise;
}
const messageOf = (error: unknown) => error instanceof Error ? error.message : 'The request failed. Please try again.';

function App() {
  const [cases, setCases] = useState<CaseListItem[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const selectedRef = useRef<string | null>(null);
  const selectedHeading = useRef<HTMLHeadingElement | null>(null);
  const [details, setDetails] = useState<Record<string, CaseDetail>>({});
  const [checkedAt, setCheckedAt] = useState(0);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [detailError, setDetailError] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [responding, setResponding] = useState(false);
  const [importing, setImporting] = useState(false);
  const [reassessing, setReassessing] = useState(false);
  const [sessionRole, setSessionRole] = useState('');
  const [mode, setMode] = useState('');
  const [sessionInfo, setSessionInfo] = useState<SessionInfo | null>(null);
  const [runningTimers, setRunningTimers] = useState(false);
  const [view, setView] = useState<'operations' | 'policies'>('operations');
  const [policyVisited, setPolicyVisited] = useState(false);
  const [policySuggestion, setPolicySuggestion] = useState<{ text: string; reviewId: string } | null>(null);
  const [policyRequest, setPolicyRequest] = useState<PolicyRequest | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);
  const [pollPaused, setPollPaused] = useState(false);
  const refreshController = useRef<AbortController | null>(null);
  const refreshVersion = useRef(0);
  const failedPolls = useRef(0);
  const mutation = useRef(false);
  const mounted = useRef(true);

  const rememberDetail = useCallback((detail: CaseDetail) => {
    setCheckedAt(Date.now());
    setDetails((current) => current[detail.case.id]?.case.revision > detail.case.revision ? current : { ...current, [detail.case.id]: detail });
  }, []);
  const selectCase = useCallback((id: string, explicit = false) => {
    if (mutation.current) return;
    if (selectedRef.current !== id) setDetailLoading(true);
    selectedRef.current = id; setSelectedId(id);
    setDetailError(null); setActionError(null); setPolicySuggestion(null);
    if (explicit && window.matchMedia('(max-width: 1023px)').matches) {
      window.requestAnimationFrame(() => {
        selectedHeading.current?.scrollIntoView({ block: 'start', behavior: 'auto' });
        selectedHeading.current?.focus({ preventScroll: true });
      });
    }
  }, []);
  const refresh = useCallback(async (manual = false) => {
    if (mutation.current || (!manual && failedPolls.current >= 3)) return;
    if (manual) { failedPolls.current = 0; setPollPaused(false); }
    refreshController.current?.abort();
    const controller = new AbortController(); refreshController.current = controller;
    const version = ++refreshVersion.current;
    const selected = selectedRef.current;
    setRefreshing(true);
    const timeout = window.setTimeout(() => controller.abort(), 15000);
    try {
      const [rows, session] = await Promise.all([listCases(controller.signal), getSession(controller.signal)]);
      if (!mounted.current || version !== refreshVersion.current) return;
      setCases(rows); setSessionRole(session.actor?.role ?? ''); setMode(session.mode); setSessionInfo(session); setError(null);
      if (!selected && rows.length) {
        const attention = rows.find((item) => ['HUMAN REVIEW', 'STOP ACTION', 'CLARIFY'].includes(item.outcome));
        selectCase(attention?.id ?? rows[0].id);
      } else if (selected) {
        const detail = await getCaseDetail(selected, controller.signal);
        if (!mounted.current || version !== refreshVersion.current) return;
        rememberDetail(detail);
        if (selectedRef.current === selected) setDetailError(null);
      }
      failedPolls.current = 0; setPollPaused(false);
      setLastUpdated(new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
    } catch (failure) {
      if (!mounted.current || version !== refreshVersion.current) return;
      failedPolls.current += 1; setPollPaused(failedPolls.current >= 3);
      setError(controller.signal.aborted ? 'Refresh timed out. Your last loaded cases are still shown.' : `Could not refresh: ${messageOf(failure)}`);
    } finally {
      window.clearTimeout(timeout);
      if (mounted.current && version === refreshVersion.current) { setRefreshing(false); setLoading(false); }
    }
  }, [rememberDetail, selectCase]);

  useEffect(() => {
    mounted.current = true;
    let cancelled = false;
    initialiseSession().then((session) => {
      if (cancelled) return;
      setSessionRole(session.actor?.role ?? ''); setMode(session.mode); setSessionInfo(session); return refresh(true);
    }).catch((failure) => { if (!cancelled) { setError(messageOf(failure)); setLoading(false); } });
    const interval = window.setInterval(() => { if (document.visibilityState === 'visible') void refresh(); }, 20000);
    return () => { cancelled = true; mounted.current = false; window.clearInterval(interval); refreshVersion.current += 1; refreshController.current?.abort(); };
  }, [refresh]);

  useEffect(() => {
    if (!selectedId) return;
    const controller = new AbortController();
    let cancelled = false;
    const timeout = window.setTimeout(() => controller.abort(), 15000);
    getCaseDetail(selectedId, controller.signal).then((detail) => {
      if (!cancelled) { rememberDetail(detail); setDetailError(null); }
    }).catch((failure) => {
      if (!cancelled) setDetailError(controller.signal.aborted ? 'Case loading timed out. Refresh to retry.' : messageOf(failure));
    }).finally(() => { window.clearTimeout(timeout); if (!cancelled && selectedRef.current === selectedId) setDetailLoading(false); });
    return () => { cancelled = true; window.clearTimeout(timeout); controller.abort(); };
  }, [selectedId, rememberDetail]);

  function beginMutation() {
    mutation.current = true; refreshVersion.current += 1; refreshController.current?.abort(); setRefreshing(false);
    setActionError(null); setNotice(null);
  }
  async function loadDemoCases() {
    if (mutation.current) return;
    beginMutation(); setImporting(true);
    let imported = 0;
    const failures: string[] = [];
    try {
      const existing = await listCases();
      for (const [buildId, eventCount] of DEMO_CASES) {
        if (existing.some((item) => item.title.includes(`BUILD ${buildId} ·`))) continue;
        try { await importBuildCase(buildId, eventCount); imported += 1; }
        catch (failure) { failures.push(`${buildId}: ${messageOf(failure)}`); }
      }
      setNotice(imported ? `Imported ${imported} fictional BUILD cases. No reviews were answered automatically.` : 'These demo prefixes are already loaded. No reviews were changed.');
      if (failures.length) setActionError(`Some cases could not be imported. Retry skips prefixes already loaded. ${failures.join(' · ')}`);
    } catch (failure) { setActionError(messageOf(failure)); }
    finally { mutation.current = false; setImporting(false); await refresh(true); }
  }
  async function handleResponse(review: Review, response: ReviewResponseInput): Promise<boolean> {
    const caseId = selectedRef.current;
    const detail = caseId ? details[caseId] : null;
    if (!detail || mutation.current) return false;
    beginMutation(); setResponding(true);
    let success = false;
    try {
      const updated = await respondToReview(review.id, response); rememberDetail(updated);
      const remaining = updated.decision?.blockers.length ?? 0;
      setNotice(`Response recorded. ${remaining ? `${remaining} requirement${remaining === 1 ? '' : 's'} still hold the current action.` : 'No blockers are recorded for the current action.'} External operations are simulated.`);
      // The backend only suggests reusable rules where the completed review supports one.
      // A suggestion failure must not turn a successful review response into an error.
      try {
        const suggestion = await reviewPolicySuggestion(review.id);
        if (suggestion.suggested_text) setPolicySuggestion({ text: suggestion.suggested_text, reviewId: suggestion.source_review_id ?? review.id });
      } catch { /* The recorded response remains successful without a policy suggestion. */ }
      success = true;
    } catch (failure) { setActionError(`${messageOf(failure)} Your response is still in the form. Refresh and check the current review before trying again.`); }
    finally { mutation.current = false; setResponding(false); await refresh(true); }
    return success;
  }
  async function reassessSelectedCase() {
    const id = selectedRef.current;
    if (!id || mutation.current || !['case_manager', 'policy_editor', 'reviewer', 'approver', 'access_officer'].includes(sessionRole)) return;
    beginMutation(); setReassessing(true);
    try {
      const updated = await evaluateCase(id); rememberDetail(updated);
      const remaining = updated.decision?.blockers.length ?? 0;
      setNotice(`Reassessed with policy ${updated.decision?.policy_version ?? 'current'}. ${remaining ? `${remaining} requirement${remaining === 1 ? '' : 's'} still hold the action.` : 'No blockers are recorded for this action.'} Reassessment does not grant new permission; external operations are simulated.`);
    } catch (failure) { setActionError(`Could not reassess this action: ${messageOf(failure)} Refresh and check its current state before retrying.`); }
    finally { mutation.current = false; setReassessing(false); await refresh(true); }
  }
  async function handleMessageAction(call: () => Promise<CaseDetail>, successMessage: string) {
    if (mutation.current || sessionRole !== 'case_manager') return;
    beginMutation(); setResponding(true);
    try { rememberDetail(await call()); setNotice(successMessage); }
    catch (failure) { setActionError(`${messageOf(failure)} Your draft is still in the form. Refresh and check its current status before retrying.`); }
    finally { mutation.current = false; setResponding(false); await refresh(true); }
  }
  async function runDueTimers() {
    const id = selectedRef.current;
    if (!id || mutation.current || sessionRole !== 'case_manager') return;
    beginMutation(); setRunningTimers(true);
    try {
      rememberDetail(await runTimers(id));
      setNotice('Due timers processed for this case. Any reminder or external action is simulated; check the activity log for recorded changes.');
    } catch (failure) { setActionError(`Could not process due timers: ${messageOf(failure)} Refresh and check the activity log before retrying.`); }
    finally { mutation.current = false; setRunningTimers(false); await refresh(true); }
  }
  async function useCaseManagerRole() {
    if (mutation.current) return;
    beginMutation();
    try { await createDemoSession('case_manager'); setSessionRole('case_manager'); setNotice('Using the case manager demo role. Other review owners remain responsible for their decisions.'); }
    catch (failure) { setActionError(messageOf(failure)); }
    finally { mutation.current = false; await refresh(true); }
  }

  const summaries = cases.map(toCaseSummaryVM);
  const selectedSummary = cases.find((item) => item.id === selectedId);
  const selectedDetail = selectedId ? details[selectedId] : undefined;
  const stats = {
    active: cases.filter((item) => item.outcome !== 'NO FURTHER ACTION').length,
    escalations: cases.filter((item) => item.outcome === 'STOP ACTION').length,
    resolvedToday: cases.filter((item) => item.outcome === 'NO FURTHER ACTION').length,
  };
  const inProgress = summaries.filter((summary) => cases.find((item) => item.id === summary.id)?.outcome !== 'NO FURTHER ACTION' && summary.id !== selectedId);
  const finishedToday = summaries.filter((summary) => cases.find((item) => item.id === summary.id)?.outcome === 'NO FURTHER ACTION');
  const busy = responding || importing || reassessing || runningTimers;
  const canReassess = ['case_manager', 'policy_editor', 'reviewer', 'approver', 'access_officer'].includes(sessionRole);

  return <div className="flex min-h-dvh w-full flex-col bg-[var(--color-canvas)] font-[var(--font-body)] text-[var(--color-ink)] lg:h-dvh lg:overflow-hidden">
    <nav aria-label="Workspace" className="flex shrink-0 flex-wrap items-center justify-between gap-3 border-b border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-3">
      <div className="flex flex-wrap items-center gap-4">
        <span className="text-base font-semibold">Property Desk</span>
        <div className="flex gap-1 rounded-[var(--radius-sm)] bg-[var(--color-canvas)] p-1">
          {(['operations', 'policies'] as const).map((tab) => <button key={tab} type="button" disabled={busy} aria-current={view === tab ? 'page' : undefined} onClick={() => { if (tab === 'policies') setPolicyVisited(true); setView(tab); }} className={`rounded px-3 py-2 text-sm font-medium ${view === tab ? 'bg-[var(--color-surface)] text-[var(--color-primary)] shadow-sm' : 'text-[var(--color-muted)]'}`}>{tab === 'operations' ? 'Cases' : 'Policies'}</button>)}
        </div>
        <a className="text-sm underline underline-offset-4" href={originalWorkspace} target="_blank" rel="noreferrer">Tenant and staff workspace</a>
      </div>
      <span className="text-xs text-[var(--color-muted)]">{sessionInfo?.mode === 'demo' ? 'Demonstration' : 'Staff workspace'} · external actions are simulated</span>
    </nav>
    <div className="flex shrink-0 flex-wrap items-center justify-between gap-2 border-b border-[var(--color-border)] px-4 py-2 text-xs text-[var(--color-muted)]">
      <span>{mode === 'demo' ? 'Demo role' : 'Session role'}: <strong>{sessionRole ? readableRole(sessionRole) : 'no session'}</strong>{lastUpdated ? ` · Updated ${lastUpdated}` : ''}{pollPaused ? ' · Automatic refresh paused after errors' : ' · Refreshes every 20 seconds while visible'}</span>
      <div className="flex flex-wrap gap-2">
        {mode === 'demo' && sessionRole !== 'case_manager' && <button type="button" className={BUTTON} disabled={busy} onClick={useCaseManagerRole}>Use case manager role</button>}
        <button type="button" className={BUTTON} disabled={busy || refreshing} onClick={() => void refresh(true)}>{refreshing ? 'Refreshing…' : 'Refresh cases'}</button>
        {view === 'operations' && <button type="button" className={BUTTON} disabled={busy || sessionRole !== 'case_manager' || mode !== 'demo'} onClick={loadDemoCases}>{importing ? 'Loading demo cases…' : 'Load demo cases'}</button>}
      </div>
    </div>
    {sessionInfo && <div className="shrink-0 border-b border-[var(--color-border)] px-4 py-2 text-xs text-[var(--color-muted)]">
      {WORKFLOW_LABELS[sessionInfo.workflow_mode] ?? sessionInfo.workflow_mode} · Model: {sessionInfo.model.provider} / {sessionInfo.model.model} · {sessionInfo.model.credential_configured ? 'Credentials configured; connection not verified here' : 'Credentials not configured'}
    </div>}
    {(error || actionError || notice) && <div className="shrink-0 space-y-2 px-4 pt-3">
      {error && <div role="alert" className="rounded border border-[var(--color-attention)] bg-[var(--color-attention-bg)] p-3 text-sm">{error} <button type="button" className="font-semibold underline" disabled={busy} onClick={() => void refresh(true)}>Retry refresh</button></div>}
      {actionError && <div role="alert" className="rounded border border-[var(--color-danger)] bg-[var(--color-danger-bg)] p-3 text-sm">{actionError}</div>}
      {notice && <div role="status" className="flex items-start justify-between gap-2 rounded bg-[var(--color-success-bg)] p-3 text-sm"><span>{notice}</span><button type="button" aria-label="Dismiss notice" className="underline" onClick={() => setNotice(null)}>Dismiss</button></div>}
    </div>}
    {policyVisited && <main className={view === 'policies' ? 'min-h-0 flex-1 overflow-y-auto' : 'hidden'}><PolicyEngine request={policyRequest} onDraftConsumed={() => setPolicyRequest(null)} sessionRole={sessionRole} onRoleChange={setSessionRole} onPublished={() => void refresh(true)} /></main>}
    <div className={view === 'operations' ? 'contents' : 'hidden'}>
      <div className="grid grid-cols-3 gap-3 border-b border-[var(--color-border)] px-4 py-3 text-xs xl:hidden" aria-label="Case overview">
        <div><strong className="block text-xl">{stats.active}</strong>Active actions</div><div><strong className="block text-xl">{stats.escalations}</strong>Actions stopped</div><div><strong className="block text-xl">{stats.resolvedToday}</strong>Action complete</div>
      </div>
      <main className="flex min-h-0 flex-1 flex-col lg:flex-row">
        <aside aria-label="Case queue" className="max-h-[24rem] w-full shrink-0 overflow-y-auto border-b border-[var(--color-border)] bg-[var(--color-sidebar)] lg:max-h-none lg:w-[270px] lg:border-r lg:border-b-0">
          {loading ? <p role="status" className="p-5 text-sm">Loading cases…</p> : <CaseList cases={summaries} selectedId={selectedId} onSelect={(id) => selectCase(id, true)} />}
        </aside>
        <section aria-label="Selected case" className="flex min-h-0 min-w-0 flex-1 flex-col">
          <div className="flex shrink-0 flex-wrap items-center justify-between gap-2 border-b border-[var(--color-border)] px-4 py-3">
            <h1 ref={selectedHeading} tabIndex={-1} className="min-w-0 break-words text-base font-semibold">{selectedSummary?.property_ref ?? 'Your maintenance cases'}</h1>
            {selectedSummary && <button type="button" className={BUTTON} disabled={busy || sessionRole !== 'case_manager'} onClick={runDueTimers} title="Process due reminders, escalations and review deadlines for this case">{runningTimers ? 'Processing timers…' : 'Run due timers'}</button>}
            {selectedSummary && <span className={`rounded-full px-3 py-1 text-xs ${severityOf(selectedSummary) === 'red' ? 'bg-[var(--color-danger-bg)]' : severityOf(selectedSummary) === 'amber' ? 'bg-[var(--color-attention-bg)]' : 'bg-[var(--color-success-bg)]'}`}>{stagePillOf(selectedSummary)}</span>}
          </div>
          <div className="min-w-0 flex-1 p-4 sm:p-6 lg:overflow-y-auto">
            {detailLoading && <p role="status" className="mb-3 text-sm text-[var(--color-muted)]">Loading the selected case…</p>}
            {detailError && <p role="alert" className="mb-3 rounded bg-[var(--color-danger-bg)] p-3 text-sm">{detailError} <button className="underline" type="button" onClick={() => void refresh(true)}>Retry</button></p>}
            {selectedDetail ? <>
              <MessageDrafts key={selectedDetail.case.id} messages={selectedDetail.tenant_messages ?? []} actionRevision={selectedDetail.case.action_revision} busy={busy} canManage={sessionRole === 'case_manager'}
                onSend={(id, text) => void handleMessageAction(() => approveMessage(id, text), 'Message delivery recorded (simulated). No real message was sent.')}
                onReject={(id, reason, redraft) => void handleMessageAction(() => rejectMessage(id, reason, redraft), redraft ? 'Draft rejected and a redraft requested. Check this case for the next draft; no real message was sent.' : 'Draft rejected. No real message was sent.')} />
              {selectedDetail.case.policy_pending && <div className="mb-4 rounded-[var(--radius-sm)] border border-[var(--color-attention)] bg-[var(--color-attention-bg)] p-4">
                <h2 className="text-sm font-semibold">A new policy needs to be checked against this action</h2>
                <p className="mt-1 text-sm">The action stays held until reassessment. This rechecks the evidence under the current published policy; it does not grant permission or resolve conflicting facts. If all checks pass, the workflow can continue with simulated actions.</p>
                <button type="button" className={`${BUTTON} mt-3`} disabled={busy || !canReassess} onClick={reassessSelectedCase}>{reassessing ? 'Reassessing…' : 'Reassess with current policy'}</button>
                {!canReassess && <p className="mt-2 text-xs">An authenticated staff role is needed to reassess this case.</p>}
              </div>}

              <p className="mb-4 text-xs text-[var(--color-muted)]">Current action only. These checks do not represent physical repair progress or prove that a contractor was contacted.</p>
              <div className="mb-6 overflow-x-auto py-2"><Pipeline nodes={computeDetailedPipeline(selectedDetail)} /></div>
              <p className="text-sm"><strong>Proposed action:</strong> {selectedDetail.case.proposal.action.replace(/_/g, ' ')} · {selectedDetail.case.proposal.work_item}</p>
              <CaseReviewPanel key={selectedDetail.case.id} detail={selectedDetail} checkedAt={checkedAt} sessionRole={sessionRole} busy={busy} onRespond={handleResponse} onRefresh={() => void refresh(true)} />
              {policySuggestion !== null && <section className="mt-5 rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-information-bg)] p-4">
                <h2 className="text-sm font-semibold">Consider a policy for similar cases</h2>
                <p className="mt-1 text-sm text-[var(--color-muted)]">A single decision does not establish a general rule. Edit this suggestion, then review its conditions and preview before publication.</p>
                <label className="mt-3 block text-sm font-medium">Policy suggestion<textarea rows={4} value={policySuggestion.text} onChange={(event) => setPolicySuggestion({ ...policySuggestion, text: event.target.value })} className="mt-1 w-full rounded border border-[var(--color-border)] bg-[var(--color-surface)] p-3 font-normal" /></label>
                <div className="mt-3 flex flex-wrap gap-2"><button type="button" className={BUTTON} disabled={!policySuggestion.text.trim()} onClick={() => { setPolicyRequest({ text: policySuggestion.text, reviewId: policySuggestion.reviewId, nonce: Date.now() }); setPolicySuggestion(null); setPolicyVisited(true); setView('policies'); }}>Review suggestion in Policies</button><button type="button" className={BUTTON} onClick={() => setPolicySuggestion(null)}>Dismiss</button></div>
              </section>}
              <div className="mt-5"><StageDetailCard stageTitle="Current proposed action" rows={computeStageRows(selectedDetail)} activity={translateActivity(selectedDetail.timeline)} /></div>
            </> : !detailLoading && <div className="rounded-[var(--radius-md)] border border-dashed border-[var(--color-border)] p-6"><h2 className="font-semibold">{selectedId ? 'Case details are unavailable' : 'Start with a maintenance request'}</h2><p className="mt-2 text-sm text-[var(--color-muted)]">{selectedId ? 'Refresh to retry. Your case selection is preserved.' : 'Existing cases appear here. Use the tenant workspace to submit a request, or load fictional BUILD prefixes with “Load demo cases”. Loading this page does not import or answer cases.'}</p></div>}
          </div>
        </section>
        <aside aria-label="Case summary" className="hidden w-[220px] shrink-0 border-l border-[var(--color-border)] bg-[var(--color-sidebar)] xl:block"><RightPanel stats={stats} inProgress={inProgress} finishedToday={finishedToday} onSelect={(id) => selectCase(id, true)} /></aside>
      </main>
    </div>
  </div>;
}
export default App;
