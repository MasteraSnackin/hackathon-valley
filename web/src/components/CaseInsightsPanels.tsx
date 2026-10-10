import { useEffect, useRef, useState } from 'react';
import type { CaseListItem } from '../lib/types';
import type { PolicyCollection } from '../lib/policies';
import { policyLabel } from '../lib/policies';
import { describePolicyChangeValue, policyChangeLabel } from '../lib/portfolio-presentation';
import { comparePolicy, dateLabel, errorText, getCaseInsights, getComparisonPolicies, readableValue, timezone } from '../lib/portfolio-api';
import type { CaseInsights, ComparedDecision, InsightClaim, PolicyComparison } from '../lib/portfolio-api';
import { Badge, CaseSelection, Empty, Field, StatusBadge, button, card, input, muted, primary } from './PortfolioShared';

function Scope({ scope }: { scope: Record<string, unknown> }) {
  return <dl className="grid gap-2 text-xs sm:grid-cols-2">{Object.entries(scope).map(([key, value]) => <div key={key} className="min-w-0"><dt className="text-[var(--color-muted)]">{policyLabel(key)}</dt><dd className="break-words">{readableValue(value)}</dd></div>)}</dl>;
}

function ClaimCard({ claim }: { claim: InsightClaim }) {
  return <article className="min-w-0 rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-canvas)] p-4">
    <h4 className="break-words font-semibold">{claim.source_label}</h4>
    <div className="mt-2 flex flex-wrap gap-2"><Badge tone={claim.verified ? 'success' : 'attention'}>{claim.verified ? 'Assertion verified' : 'Assertion unverified'}</Badge><Badge tone={claim.applicability === 'CURRENT' ? 'quiet' : 'attention'}>{policyLabel(claim.applicability)}</Badge></div>
    <p className="mt-3 text-sm font-medium">Asserted value: {readableValue(claim.value)}</p>
    {claim.source_quote ? <blockquote className="mt-3 whitespace-pre-wrap break-words border-l-2 border-[var(--color-border)] pl-3 text-sm">“{claim.source_quote}”</blockquote> : <p className={`${muted} mt-3`}>No supporting quotation was recorded.</p>}
    <dl className="mt-4 space-y-2 text-xs"><div><dt className="text-[var(--color-muted)]">Source occurrence time</dt><dd>{dateLabel(claim.occurred_at)}</dd></div><div><dt className="text-[var(--color-muted)]">Assertion recorded</dt><dd>{dateLabel(claim.created_at)}</dd></div><div><dt className="text-[var(--color-muted)]">Source submitter role</dt><dd>{claim.actor?.role ? policyLabel(claim.actor.role) : 'Not recorded'} · not verified sender identity</dd></div>{claim.expires_at && <div><dt className="text-[var(--color-muted)]">Expires</dt><dd>{dateLabel(claim.expires_at)}</dd></div>}</dl>
    {claim.hearsay && <p className="mt-3 text-sm text-[var(--color-attention)]">Second-hand assertion: does not establish this fact.</p>}
    {claim.superseded_by && <p className="mt-3 break-words text-xs text-[var(--color-muted)]">Superseded by assertion {claim.superseded_by}</p>}
    <details className="mt-3 text-sm"><summary className="cursor-pointer font-medium">Scope and source reference</summary><div className="mt-3 space-y-3"><Scope scope={claim.scope} /><p className="break-all text-xs">Source: {claim.source_id}<br />Assertion: {claim.id}</p>{claim.verification && <p className="break-words text-xs">Verification: {claim.verification}{claim.verified_by?.role ? ` (${policyLabel(claim.verified_by.role)})` : ''}</p>}{claim.party && <p className="break-words text-xs">Recorded party metadata: {readableValue(claim.party)}</p>}</div></details>
  </article>;
}

function DecisionView({ decision, label }: { decision: ComparedDecision; label: string }) {
  return <section className="min-w-0 rounded-[var(--radius-sm)] border border-[var(--color-border)] p-4" aria-label={label}>
    <h3 className="font-semibold">{label}</h3><div className="mt-2"><StatusBadge status={decision.outcome} /></div>
    {decision.next_step && <p className="mt-3 break-words text-sm">{decision.next_step}</p>}
    {decision.owner && <p className={`${muted} mt-2`}>Decision owner: {policyLabel(decision.owner)}</p>}
    <h4 className="mt-4 text-sm font-semibold">Independent blockers ({decision.blockers.length})</h4>
    {!decision.blockers.length ? <p className={`${muted} mt-2`}>No blockers recorded in this decision. This does not prove that an external action happened.</p> : <ul className="mt-2 space-y-3">{decision.blockers.map((blocker, index) => <li key={`${blocker.key}:${blocker.rule_id}:${index}`} className="border-l-2 border-[var(--color-border)] pl-3 text-sm"><p className="font-medium">{policyLabel(blocker.key)} · {policyLabel(blocker.status)}</p><p className="mt-1 break-words">{blocker.reason}</p><p className="mt-1 text-xs text-[var(--color-muted)]">{policyLabel(blocker.response)} · {policyLabel(blocker.owner)}</p></li>)}</ul>}
    <details className="mt-4 text-sm"><summary className="cursor-pointer font-medium">All checks ({decision.checks.length})</summary><ul className="mt-3 space-y-3">{decision.checks.map((check, index) => <li key={`${check.key}:${index}`}><p className="font-medium">{policyLabel(check.key)} · {policyLabel(check.status)}</p><p className="break-words text-[var(--color-muted)]">{check.reason}</p></li>)}</ul></details>
  </section>;
}

function ChangedRequirement({ value, label }: { value: unknown; label: 'Before' | 'After' }) {
  const presentation = describePolicyChangeValue(value);
  return <section className="min-w-0 rounded-[var(--radius-sm)] border border-[var(--color-border)] p-3" aria-label={`${label} requirement`}>
    <h5 className="font-semibold">{label}</h5>
    {presentation.text && <p className="mt-2 break-words">{presentation.text}</p>}
    {!!presentation.fields.length && <dl className="mt-2 space-y-2">{presentation.fields.map((field) => <div key={field.label}><dt className="text-xs text-[var(--color-muted)]">{field.label}</dt><dd className="break-words">{field.value}</dd></div>)}</dl>}
    {!!Object.keys(presentation.metadata).length && <details className="mt-3"><summary className="cursor-pointer text-xs text-[var(--color-muted)]">Supporting metadata</summary><pre tabIndex={0} aria-label={`${label} supporting metadata`} className="mt-2 max-h-48 overflow-auto whitespace-pre-wrap break-all rounded bg-[var(--color-canvas)] p-2 text-xs">{JSON.stringify(presentation.metadata, null, 2)}</pre></details>}
  </section>;
}

export function CaseInsightsPanel({ caseId, mode }: { caseId: string; mode: 'evidence' | 'playback' }) {
  const [data, setData] = useState<CaseInsights | null>(null);
  const [index, setIndex] = useState(0);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');
  const [reload, setReload] = useState(0);
  const [onlyUnresolved, setOnlyUnresolved] = useState(false);
  useEffect(() => {
    const controller = new AbortController();
    getCaseInsights(caseId, controller.signal).then((result) => {
      if (controller.signal.aborted) return;
      setData(result); setIndex(0); setBusy(false); setError('');
    }).catch((failure) => { if (!controller.signal.aborted) { setError(errorText(failure)); setBusy(false); } });
    return () => controller.abort();
  }, [caseId, reload]);
  const comparisons = data?.comparisons.filter((group) => !onlyUnresolved || ['CONFLICT', 'UNKNOWN', 'FAIL'].includes(group.status)) || [];
  const frame = data?.frames[Math.min(index, Math.max(0, data.frames.length - 1))];
  return <section className={card} aria-labelledby={`case-${mode}-heading`}>
    <div className="flex flex-wrap items-start justify-between gap-3"><div><h2 id={`case-${mode}-heading`} className="text-lg font-semibold">{mode === 'evidence' ? 'Compare source assertions' : 'Recorded case playback'}</h2><p className={`${muted} mt-1`}>{mode === 'evidence' ? 'Review statements about the same fact and action without discarding the disagreement.' : 'Step through saved decisions using only the information recorded by each point.'}</p></div><button type="button" className={button} disabled={busy} onClick={() => { setBusy(true); setError(''); setReload((value) => value + 1); }}>Refresh {mode === 'evidence' ? 'evidence' : 'recording'}</button></div>
    {busy && <p role="status" className={`${muted} mt-4`}>Loading {mode === 'evidence' ? 'evidence comparison' : 'recorded decisions'}…</p>}
    {error && <p role="alert" className="mt-4 rounded bg-[var(--color-danger-bg)] p-3 text-sm text-[var(--color-danger)]">{error} {data ? 'The previous snapshot is still shown; refresh to retry.' : 'Use Refresh to retry.'}</p>}
    {data && <>
      <p className={`${muted} mt-3`}>Snapshot retrieved {dateLabel(data.as_of)} · times in {timezone} · case <span className="break-all">{data.case_id}</span></p>
      {mode === 'evidence' ? <>
        <p className="mt-4 rounded bg-[var(--color-information-bg)] p-3 text-sm text-[var(--color-information)]">{data.comparison_notice}</p>
        <label className="my-4 flex min-h-11 items-center gap-3 text-sm"><input type="checkbox" className="h-5 w-5 accent-[var(--color-primary)]" checked={onlyUnresolved} onChange={(event) => setOnlyUnresolved(event.target.checked)} />Show only unresolved, refused or conflicting facts</label>
        <div className="space-y-5">{!comparisons.length ? <Empty>{data.comparisons.length ? 'No source groups match this filter.' : 'No structured assertions have been recorded. This does not mean the evidence is complete. Recorded source material is available in playback after a saved decision.'}</Empty> : comparisons.map((group, groupIndex) => <section key={`${group.key}:${groupIndex}`} className="min-w-0 rounded-[var(--radius-sm)] border border-[var(--color-border)] p-4"><div className="flex flex-wrap items-start justify-between gap-2"><h3 className="font-semibold">{policyLabel(group.key)}</h3><StatusBadge status={group.status} /></div><p className="mt-2 text-sm">{group.reason}</p><p className={`${muted} mt-2`}>{group.applies_to_current_action ? 'Applies to the current proposed action.' : 'Outside the current action scope.'}</p><details className="mt-3 text-sm"><summary className="cursor-pointer font-medium">Compared action scope</summary><div className="mt-2"><Scope scope={group.scope} /></div></details><div className="mt-4 grid items-start gap-3 lg:grid-cols-2">{group.claims.map((claim) => <ClaimCard key={claim.id} claim={claim} />)}</div></section>)}</div>
      </> : <>
        <p className="mt-4 rounded bg-[var(--color-information-bg)] p-3 text-sm text-[var(--color-information)]">{data.playback_notice}</p>
        {!frame ? <div className="mt-4"><Empty>No decision has been recorded for this case yet. Playback will become available after its first saved assessment.</Empty></div> : <div className="mt-5 space-y-4">
          <div className="rounded-[var(--radius-sm)] border border-[var(--color-border)] p-4"><Field label={`Recorded decision ${index + 1} of ${data.frames.length}`}><input className="w-full accent-[var(--color-primary)]" type="range" min={0} max={Math.max(0, data.frames.length - 1)} step={1} value={index} aria-valuetext={`Decision ${index + 1}, recorded ${dateLabel(frame.at)}`} disabled={data.frames.length < 2} onChange={(event) => setIndex(Number(event.target.value))} /></Field><div className="mt-3 flex flex-wrap items-center justify-between gap-2"><button type="button" className={button} disabled={index === 0} onClick={() => setIndex((value) => Math.max(0, value - 1))}>Previous decision</button><p role="status" className="text-sm">Recorded {dateLabel(frame.at)}</p><button type="button" className={button} disabled={index >= data.frames.length - 1} onClick={() => setIndex((value) => Math.min(data.frames.length - 1, value + 1))}>Next decision</button></div></div>
          <p className={muted}>Policy version {frame.decision.policy_version} · case revision {frame.decision.case_revision} · action revision {frame.decision.action_revision}. The sections below contain this historical frame only.</p>
          <DecisionView decision={frame.decision} label="Decision as recorded" />
          <section aria-label="Evidence available at this decision"><h3 className="font-semibold">Evidence received by this point ({frame.evidence.length})</h3><div className="mt-3 space-y-3">{!frame.evidence.length ? <Empty>No evidence was recorded before this decision.</Empty> : frame.evidence.map((source) => <details key={source.id} className="min-w-0 rounded-[var(--radius-sm)] border border-[var(--color-border)] p-3"><summary className="cursor-pointer break-words text-sm font-medium">{source.source_label || 'Recorded source'} · received {dateLabel(source.created_at)}</summary><p className={`${muted} mt-2`}>Source occurrence time: {dateLabel(source.occurred_at)}. This is separate from receipt order.</p><blockquote className="mt-3 whitespace-pre-wrap break-words text-sm">{source.text}</blockquote><p className="mt-3 break-all text-xs text-[var(--color-muted)]">Source {source.id}</p></details>)}</div></section>
          <details className="text-sm"><summary className="cursor-pointer font-medium">Recorded events available by this point ({frame.events.length})</summary><ol className="mt-3 space-y-3">{frame.events.map((event) => <li key={event.id} className="min-w-0 border-l-2 border-[var(--color-border)] pl-3"><p className="font-medium">{policyLabel(event.kind)} · {dateLabel(event.created_at)}</p><details className="mt-1"><summary className="cursor-pointer text-[var(--color-muted)]">Recorded payload</summary><pre tabIndex={0} aria-label={`${event.kind} event payload`} className="mt-2 max-h-72 overflow-auto whitespace-pre-wrap break-all rounded bg-[var(--color-canvas)] p-3 text-xs">{JSON.stringify(event.payload, null, 2)}</pre></details></li>)}</ol></details>
        </div>}
      </>}
    </>}
  </section>;
}

export function PolicyComparisonPanel({ cases, sessionRole, onSelectCase, onOpenPolicies }: {
  cases: CaseListItem[]; sessionRole: string; onSelectCase: (id: string) => void; onOpenPolicies?: () => void;
}) {
  const [collection, setCollection] = useState<PolicyCollection | null>(null);
  const [draftId, setDraftId] = useState('');
  const [caseIds, setCaseIds] = useState<string[]>([]);
  const [comparison, setComparison] = useState<PolicyComparison | null>(null);
  const [busy, setBusy] = useState('load');
  const [error, setError] = useState('');
  const [reload, setReload] = useState(0);
  const controllerRef = useRef<AbortController | null>(null);
  const canCompare = sessionRole === 'policy_editor';
  useEffect(() => {
    const controller = new AbortController();
    getComparisonPolicies(controller.signal).then((data) => { if (!controller.signal.aborted) { setCollection(data); setBusy(''); setError(''); } }).catch((failure) => { if (!controller.signal.aborted) { setError(errorText(failure)); setBusy(''); } });
    return () => controller.abort();
  }, [reload]);
  useEffect(() => () => controllerRef.current?.abort(), []);
  async function compare() {
    if (busy || !canCompare || !draftId || !caseIds.length) return;
    controllerRef.current?.abort();
    const controller = new AbortController(); controllerRef.current = controller;
    setBusy('compare'); setError(''); setComparison(null);
    try { const result = await comparePolicy(draftId, caseIds, controller.signal); if (!controller.signal.aborted) setComparison(result); }
    catch (failure) { if (!controller.signal.aborted) setError(errorText(failure)); }
    finally { if (!controller.signal.aborted) setBusy(''); }
  }
  return <div className="space-y-5">
    <section className={card} aria-labelledby="portfolio-policy-compare"><div className="flex flex-wrap items-start justify-between gap-3"><div><h2 id="portfolio-policy-compare" className="text-lg font-semibold">Compare a saved policy draft</h2><p className={`${muted} mt-1`}>Compare the current rules and a proposed version against the same case facts. This view never publishes a policy or reassesses a live case.</p></div>{onOpenPolicies && <button type="button" className={button} onClick={onOpenPolicies}>Open policy editor</button>}</div>
      {!canCompare && <p className="mt-4 rounded bg-[var(--color-attention-bg)] p-3 text-sm text-[var(--color-attention)]">Use the policy editor role to run comparisons. Your current role is {policyLabel(sessionRole || 'not signed in')}.</p>}
      {error && <p role="alert" className="mt-4 rounded bg-[var(--color-danger-bg)] p-3 text-sm text-[var(--color-danger)]">{error}</p>}
      {busy === 'load' && <p role="status" className={`${muted} mt-4`}>Loading saved drafts…</p>}
      <form className="mt-4 space-y-4" onSubmit={(event) => { event.preventDefault(); void compare(); }}>
        <fieldset disabled={!!busy || !canCompare} className="space-y-4 disabled:opacity-60"><legend className="sr-only">Choose draft and cases to compare</legend>
          <Field label="Saved draft"><select className={input} value={draftId} onChange={(event) => { setDraftId(event.target.value); setComparison(null); }} required><option value="">Choose a draft</option>{collection?.drafts.map((draft) => <option key={draft.id} value={draft.id}>{draft.reason || draft.id} · based on version {draft.base_version}</option>)}</select></Field>
          {collection && !collection.drafts.length && <Empty>No saved drafts yet. Save a draft in the policy editor, then refresh this list.</Empty>}
          <CaseSelection cases={cases} ids={caseIds} onChange={(ids) => { setCaseIds(ids); setComparison(null); }} />
          <button type="submit" className={primary} disabled={!draftId || !caseIds.length}>{busy === 'compare' ? 'Comparing rules…' : 'Run preview comparison'}</button>
        </fieldset>
        <button type="button" className={button} disabled={!!busy} onClick={() => { setBusy('load'); setComparison(null); setDraftId(''); setReload((value) => value + 1); }}>Refresh draft list</button>
      </form>
      {collection && <p className={`${muted} mt-3`}>Published version when drafts were loaded: {collection.active.version}. Each comparison checks the current server version again.</p>}
    </section>
    {comparison && <section className={card} aria-labelledby="portfolio-policy-results"><div className="flex flex-wrap items-start justify-between gap-2"><h2 id="portfolio-policy-results" className="text-lg font-semibold">Policy comparison results</h2><Badge>Preview only · nothing published</Badge></div><p className={`${muted} mt-2`}>Current version {comparison.active_version} → proposed version {comparison.proposed_version}. Same evaluation time: {dateLabel(comparison.as_of)} ({timezone}).</p>
      {comparison.stale_base && <p role="status" className="mt-4 rounded bg-[var(--color-attention-bg)] p-3 text-sm text-[var(--color-attention)]">This draft was based on an older policy. You can inspect its effect, but it must be rebased in the policy editor before publication.</p>}
      <div className="mt-4 rounded bg-[var(--color-information-bg)] p-4 text-sm text-[var(--color-information)]"><h3 className="font-semibold">What this preview includes</h3><ul className="mt-2 list-disc space-y-2 pl-5">{comparison.assumptions.map((assumption) => <li key={assumption}>{assumption}</li>)}</ul></div>
      <div className="mt-5 space-y-5">{!comparison.rows.length ? <Empty>No case rows were returned.</Empty> : comparison.rows.map((row) => <article key={row.case_id} className="min-w-0 rounded-[var(--radius-sm)] border border-[var(--color-border)] p-4"><div className="flex flex-wrap items-start justify-between gap-2"><button type="button" className="min-h-11 break-words text-left font-semibold text-[var(--color-primary)] underline underline-offset-4" onClick={() => onSelectCase(row.case_id)}>{row.title || row.case_id}</button><Badge tone={row.changes.length ? 'attention' : 'quiet'}>{row.completed ? 'Recorded action retained' : row.changes.length ? `${row.changes.length} changes` : 'No rule changes for this case'}</Badge></div>
        {row.completed && <p className={`${muted} mt-2`}>This action has a recorded simulated result. The comparison preserves its original decision and receipt; it does not reopen it.</p>}
        <div className="mt-3 grid items-start gap-3 lg:grid-cols-2"><DecisionView decision={row.before} label={row.completed ? `Recorded result · original policy version ${row.before.recorded_decision?.policy_version ?? row.before.policy_version ?? 'not recorded'}` : `Current rules · version ${comparison.active_version}`} /><DecisionView decision={row.after} label={row.completed ? 'Retained result · not re-evaluated' : `Proposed rules · version ${comparison.proposed_version}`} /></div>
        {row.completed && row.before.recorded_decision && <details className="mt-3 text-sm"><summary className="cursor-pointer font-medium">Original decision before the simulated action</summary><div className="mt-3"><DecisionView decision={row.before.recorded_decision} label="Decision when the action was authorised" /></div></details>}
        {!!row.changes.length && <section className="mt-4"><h3 className="font-semibold">What changes and why</h3><ul className="mt-3 space-y-3">{row.changes.map((change, index) => <li key={`${change.key}:${index}`} className="min-w-0 border-l-2 border-[var(--color-border)] pl-3 text-sm"><h4 className="break-words font-medium">{policyChangeLabel(change.key)}</h4><p className="mt-1">{change.reason}</p><div className="mt-2 grid gap-2 lg:grid-cols-2"><ChangedRequirement value={change.before} label="Before" /><ChangedRequirement value={change.after} label="After" /></div></li>)}</ul></section>}
        {row.receipt && <details className="mt-3 text-sm"><summary className="cursor-pointer font-medium">Retained simulated receipt</summary><pre tabIndex={0} aria-label="Retained simulated receipt" className="mt-2 max-h-72 overflow-auto whitespace-pre-wrap break-all rounded bg-[var(--color-canvas)] p-3 text-xs">{JSON.stringify(row.receipt, null, 2)}</pre></details>}
      </article>)}</div>
    </section>}
  </div>;
}
