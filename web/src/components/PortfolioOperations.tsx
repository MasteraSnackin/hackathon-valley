import { useState } from 'react';
import type { CaseListItem } from '../lib/types';
import type { CaseProfile, Incident, IncidentSuggestion, Portfolio, VisitPlan } from '../lib/portfolio-api';
import { cancelVisitPlan, createContractor, createIncident, createVisitPlan, dateLabel, dismissSuggestion, errorText, isoToLocalInput, localDateTimeToIso, saveCaseProfile, timezone, updateIncident } from '../lib/portfolio-api';
import { policyLabel } from '../lib/policies';
import { Badge, CaseLinks, CaseSelection, Empty, Field, StatusBadge, button, card, input, muted, primary } from './PortfolioShared';

export type PortfolioMutation = (work: () => Promise<unknown>, notice: string) => Promise<boolean>;
interface OperationsProps {
  portfolio: Portfolio;
  cases: CaseListItem[];
  busy: boolean;
  canManage: boolean;
  mutate: PortfolioMutation;
  onSelectCase: (id: string) => void;
}

function DateWindow({ start, end, onStart, onEnd, required = false, fromLabel = 'Window starts', toLabel = 'Window ends' }: {
  start: string; end: string; onStart: (value: string) => void; onEnd: (value: string) => void; required?: boolean; fromLabel?: string; toLabel?: string;
}) {
  return <div className="grid min-w-0 gap-3 sm:grid-cols-2">
    <Field label={fromLabel}><input type="datetime-local" className={input} value={start} onChange={(event) => onStart(event.target.value)} required={required || !!end} /></Field>
    <Field label={toLabel}><input type="datetime-local" className={input} value={end} onChange={(event) => onEnd(event.target.value)} required={required || !!start} min={start || undefined} /></Field>
    <p className={`${muted} sm:col-span-2`}>Times use {timezone}. {required ? 'Both times are required.' : 'Leave both blank if the window is unknown.'}</p>
  </div>;
}

function ProfileForm({ item, existing, busy, canManage, mutate }: {
  item: CaseListItem; existing?: CaseProfile; busy: boolean; canManage: boolean; mutate: PortfolioMutation;
}) {
  const [property, setProperty] = useState(existing?.property_key || '');
  const [asset, setAsset] = useState(existing?.asset_ref || '');
  const [trade, setTrade] = useState(existing?.trade || '');
  const [start, setStart] = useState(isoToLocalInput(existing?.window_start));
  const [end, setEnd] = useState(isoToLocalInput(existing?.window_end));
  const [reason, setReason] = useState('');
  const [error, setError] = useState('');
  async function submit() {
    setError('');
    try {
      const window_start = localDateTimeToIso(start), window_end = localDateTimeToIso(end);
      if (window_start && window_end && window_start >= window_end) throw new Error('The window must end after it starts.');
      await mutate(() => saveCaseProfile(item.id, { property_key: property.trim(), asset_ref: asset.trim(), trade: trade.trim(), window_start, window_end, reason: reason.trim() }), 'Case profile saved. This groups records for planning; existing evidence and permissions are unchanged.');
    } catch (failure) { setError(errorText(failure)); }
  }
  return <form onSubmit={(event) => { event.preventDefault(); void submit(); }} className="mt-4 space-y-4">
    <p className={muted}>Original property reference: <span className="font-medium text-[var(--color-ink)]">{item.property_ref || 'Not recorded'}</span>. Confirm a shared building identifier from your records; do not group by proximity alone.</p>
    {error && <p role="alert" className="text-sm text-[var(--color-danger)]">{error}</p>}
    <fieldset disabled={busy || !canManage} className="space-y-4 disabled:opacity-60"><legend className="sr-only">Staff-confirmed case profile</legend>
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="Confirmed building identifier" hint="Use the same identifier for cases at the same verified building. This does not change the original property reference."><input className={input} value={property} onChange={(event) => setProperty(event.target.value)} required maxLength={200} /></Field>
        <Field label="Asset reference (optional)" hint="For example, an existing boiler ID. Leave blank when unknown."><input className={input} value={asset} onChange={(event) => setAsset(event.target.value)} maxLength={200} /></Field>
        <Field label="Required trade" hint="Use the same trade name as the contractor record."><input className={input} value={trade} onChange={(event) => setTrade(event.target.value)} required maxLength={100} /></Field>
      </div>
      <DateWindow start={start} end={end} onStart={setStart} onEnd={setEnd} />
      <Field label="Confirmation source and reason" hint="Record how you checked the building, asset, trade and any appointment window. This does not grant access permission."><textarea className={`${input} min-h-20`} value={reason} onChange={(event) => setReason(event.target.value)} required minLength={3} maxLength={2000} /></Field>
      <button type="submit" className={primary}>{busy ? 'Saving…' : existing ? 'Update case profile' : 'Save case profile'}</button>
    </fieldset>
    {existing && <p className={muted}>Last confirmed {dateLabel(existing.created_at)} by {existing.actor?.role || 'staff'}. {existing.reason}</p>}
  </form>;
}

function IncidentStatus({ incident, ...props }: OperationsProps & { incident: Incident }) {
  const [status, setStatus] = useState<'resolved' | 'dismissed'>('resolved');
  const [reason, setReason] = useState('');
  return <article className="min-w-0 rounded-[var(--radius-sm)] border border-[var(--color-border)] p-4">
    <div className="flex flex-wrap items-start justify-between gap-2"><h3 className="break-words font-semibold">{incident.title}</h3><Badge tone={incident.stale ? 'attention' : 'quiet'}>{incident.stale ? `${incident.status} · changed profiles` : incident.status}</Badge></div>
    <p className={`${muted} mt-2 break-words`}>{incident.reason}</p>
    <CaseLinks ids={incident.case_ids} cases={props.cases} onSelectCase={props.onSelectCase} />
    <p className={muted}>Recorded {dateLabel(incident.created_at)}. Individual conversations, permission checks and case outcomes stay separate.</p>
    {incident.stale && <p className="mt-2 text-sm text-[var(--color-attention)]">One or more case profiles changed after this grouping was confirmed. Review the linked cases before relying on it.</p>}
    {incident.status === 'confirmed' && <details className="mt-3"><summary className="cursor-pointer text-sm font-medium">Update incident status</summary>
      <form className="mt-3 space-y-3" onSubmit={(event) => { event.preventDefault(); void props.mutate(() => updateIncident(incident.id, status, reason.trim()), 'Incident status updated. Its individual cases have not been closed.'); }}>
        <fieldset disabled={!props.canManage || props.busy} className="space-y-3 disabled:opacity-60"><legend className="sr-only">Update incident status</legend>
          <Field label="New incident status"><select className={input} value={status} onChange={(event) => setStatus(event.target.value as 'resolved' | 'dismissed')}><option value="resolved">Resolved at incident level</option><option value="dismissed">Dismiss grouping</option></select></Field>
          <Field label="Reason for this status"><textarea className={input} required minLength={3} maxLength={2000} value={reason} onChange={(event) => setReason(event.target.value)} /></Field>
          <p className={muted}>Resolving this coordination record does not verify a repair or close its cases.</p><button className={button} type="submit">Save incident status</button>
        </fieldset>
      </form>
    </details>}
  </article>;
}

function SuggestionCard({ suggestion, onReview, ...props }: OperationsProps & { suggestion: IncidentSuggestion; onReview: () => void }) {
  const [reason, setReason] = useState('');
  return <article className="rounded-[var(--radius-sm)] border border-[var(--color-border)] p-4">
    <Badge tone="attention">Possible connection · {suggestion.case_ids.length} reports</Badge><h3 className="mt-2 break-words font-medium">{suggestion.property_key}</h3>
    <p className={`${muted} mt-2`}>{suggestion.reason || suggestion.reasons?.join(' ') || 'Review the source records to confirm whether these cases belong together.'}</p>
    {suggestion.time_basis && <p className={`${muted} mt-2`}>Time basis: {suggestion.time_basis}{suggestion.window_days ? ` · within ${suggestion.window_days} days` : ''}.</p>}
    <CaseLinks ids={suggestion.case_ids} cases={props.cases} onSelectCase={props.onSelectCase} />
    {!!suggestion.signals?.length && <details className="mt-2 text-sm"><summary className="cursor-pointer font-medium">Signals and source references</summary><ul className="mt-3 space-y-3">{suggestion.signals.map((signal) => <li key={signal.case_id} className="break-words"><p className="font-medium">{signal.title}</p><p>{signal.category} · {signal.work_item} · case recorded {dateLabel(signal.reported_at)}</p><p className="break-all text-xs text-[var(--color-muted)]">Records: {signal.source_record_ids.join(', ') || 'No linked source references'}</p></li>)}</ul></details>}
    <button type="button" className={`${button} mt-3`} disabled={props.busy || !props.canManage} onClick={onReview}>Review this grouping</button>
    {suggestion.id && <details className="mt-3 text-sm"><summary className="cursor-pointer font-medium">These cases are unrelated</summary><form className="mt-3 space-y-3" onSubmit={(event) => { event.preventDefault(); void props.mutate(() => dismissSuggestion(suggestion.id!, reason.trim()), 'Suggestion dismissed with its current supporting records. New evidence can create a new suggestion.'); }}><fieldset disabled={props.busy || !props.canManage} className="space-y-3 disabled:opacity-60"><legend className="sr-only">Dismiss suggested connection</legend><Field label="Reason for dismissing this connection"><textarea className={input} value={reason} onChange={(event) => setReason(event.target.value)} required minLength={3} maxLength={2000} /></Field><button type="submit" className={button}>Dismiss suggestion</button></fieldset></form></details>}
  </article>;
}

export function IncidentsPanel(props: OperationsProps & { selectedCaseId: string | null; onChooseCase: (id: string) => void }) {
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [title, setTitle] = useState('');
  const [reason, setReason] = useState('');
  const [confirmed, setConfirmed] = useState(false);
  const selectedCase = props.cases.find((item) => item.id === props.selectedCaseId);
  const profile = props.portfolio.profiles.find((item) => item.case_id === selectedCase?.id);
  return <div className="space-y-5">
    <section className={card} aria-labelledby="portfolio-profiles"><h2 id="portfolio-profiles" className="text-lg font-semibold">Confirm property and planning details</h2>
      <p className={`${muted} mt-1`}>Suggestions use recorded case information and staff-confirmed building identifiers. A possible connection does not establish a shared cause.</p>
      <Field label="Case to profile"><select className={`${input} mt-3`} value={selectedCase?.id || ''} onChange={(event) => props.onChooseCase(event.target.value)}><option value="">Choose a case</option>{props.cases.map((item) => <option key={item.id} value={item.id}>{item.title}</option>)}</select></Field>
      {selectedCase ? <ProfileForm key={`${selectedCase.id}:${profile?.id || 'new'}`} item={selectedCase} existing={profile} {...props} /> : <div className="mt-4"><Empty>Select a case to confirm its building and optional asset details.</Empty></div>}
    </section>
    <div className="grid items-start gap-5 xl:grid-cols-2">
      <section className={card} aria-labelledby="portfolio-suggestions"><h2 id="portfolio-suggestions" className="text-lg font-semibold">Possible shared incidents</h2><p className={`${muted} mt-1`}>Review the matching signals before confirming. Similar symptoms or a shared building are clues, not a diagnosis.</p>
        <div className="mt-4 space-y-3">{!props.portfolio.suggestions.length ? <Empty>No matching suggestions yet. Confirm building profiles for related cases first; unrelated cases should stay separate.</Empty> : props.portfolio.suggestions.map((suggestion, index) => <SuggestionCard key={suggestion.id || `${suggestion.property_key}:${index}`} {...props} suggestion={suggestion} onReview={() => { setSelectedIds(suggestion.case_ids); setTitle(`Shared incident at ${suggestion.property_key}`); setReason(''); setConfirmed(false); document.getElementById('portfolio-confirm-incident')?.focus(); }} />)}</div>
      </section>
      <section className={card} aria-labelledby="portfolio-confirm-incident"><h2 id="portfolio-confirm-incident" tabIndex={-1} className="text-lg font-semibold">Confirm an incident</h2>
        <form className="mt-4 space-y-4" onSubmit={(event) => { event.preventDefault(); void props.mutate(() => createIncident(selectedIds, title.trim(), reason.trim()), 'Shared incident recorded. All cases retain their own evidence, conversations and approval checks.').then((saved) => { if (saved) { setSelectedIds([]); setTitle(''); setReason(''); setConfirmed(false); } }); }}>
          <fieldset disabled={props.busy || !props.canManage} className="space-y-4 disabled:opacity-60"><legend className="sr-only">Confirm shared incident</legend>
            <CaseSelection cases={props.cases} ids={selectedIds} onChange={(ids) => { setSelectedIds(ids); setConfirmed(false); }} label="Related cases (choose at least two)" />
            <Field label="Incident title"><input className={input} value={title} onChange={(event) => setTitle(event.target.value)} required minLength={3} maxLength={200} /></Field>
            <Field label="Evidence and reason for grouping"><textarea className={`${input} min-h-20`} value={reason} onChange={(event) => setReason(event.target.value)} required minLength={3} maxLength={2000} /></Field>
            <label className="flex items-start gap-3 text-sm"><input type="checkbox" className="mt-1 h-5 w-5 shrink-0 accent-[var(--color-primary)]" checked={confirmed} onChange={(event) => setConfirmed(event.target.checked)} required /><span>I checked these records and confirm the grouping. This does not merge conversations, establish a cause or grant authority.</span></label>
            <button type="submit" className={primary} disabled={!confirmed || selectedIds.length < 2}>Confirm shared incident</button>
          </fieldset>
        </form>
      </section>
    </div>
    <section className={card} aria-labelledby="portfolio-incidents"><h2 id="portfolio-incidents" className="text-lg font-semibold">Recorded incidents</h2><div className="mt-4 grid gap-3 lg:grid-cols-2">{!props.portfolio.incidents.length ? <Empty>No incident has been confirmed.</Empty> : props.portfolio.incidents.map((incident) => <IncidentStatus key={incident.id} incident={incident} {...props} />)}</div></section>
  </div>;
}

function ContractorForm({ mutate, busy, canManage }: Pick<OperationsProps, 'mutate' | 'busy' | 'canManage'>) {
  const [name, setName] = useState('');
  const [trades, setTrades] = useState('');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [reason, setReason] = useState('');
  const [error, setError] = useState('');
  async function submit() {
    setError('');
    try {
      const available_from = localDateTimeToIso(start), available_until = localDateTimeToIso(end);
      if (!available_from || !available_until || available_from >= available_until) throw new Error('Enter an availability window that ends after it starts.');
      const saved = await mutate(() => createContractor({ name: name.trim(), trades: [...new Set(trades.split(',').map((value) => value.trim()).filter(Boolean))], available_from, available_until, reason: reason.trim() }), 'Contractor availability recorded from staff input. No contractor has been contacted.');
      if (saved) { setName(''); setTrades(''); setStart(''); setEnd(''); setReason(''); }
    } catch (failure) { setError(errorText(failure)); }
  }
  return <form className="mt-4 space-y-3" onSubmit={(event) => { event.preventDefault(); void submit(); }}>
    {error && <p role="alert" className="text-sm text-[var(--color-danger)]">{error}</p>}
    <fieldset disabled={busy || !canManage} className="space-y-3 disabled:opacity-60"><legend className="sr-only">Record contractor availability</legend>
      <Field label="Contractor or team name"><input className={input} value={name} required maxLength={200} onChange={(event) => setName(event.target.value)} /></Field>
      <Field label="Trades (separated by commas)" hint="Match the trade names in case profiles."><input className={input} value={trades} required maxLength={500} onChange={(event) => setTrades(event.target.value)} /></Field>
      <DateWindow start={start} end={end} onStart={setStart} onEnd={setEnd} required fromLabel="Available from" toLabel="Available until" />
      <Field label="Source of this availability"><textarea className={input} value={reason} onChange={(event) => setReason(event.target.value)} required minLength={3} maxLength={2000} /></Field>
      <button className={primary} type="submit">Record availability</button>
    </fieldset>
  </form>;
}

function VisitCard({ plan, ...props }: OperationsProps & { plan: VisitPlan }) {
  const [reason, setReason] = useState('');
  const contractor = props.portfolio.contractors.find((item) => item.id === plan.contractor_id);
  return <article className="min-w-0 rounded-[var(--radius-sm)] border border-[var(--color-border)] p-4">
    <div className="flex flex-wrap items-start justify-between gap-2"><h3 className="break-words font-semibold">{contractor?.name || plan.contractor_id}</h3><Badge tone={plan.stale ? 'attention' : 'quiet'}>{plan.status === 'cancelled' ? 'Cancelled' : 'Tentative · not dispatched'}</Badge></div>
    <p className="mt-2 text-sm">{dateLabel(plan.start)} – {dateLabel(plan.end)}</p><CaseLinks ids={plan.case_ids} cases={props.cases} onSelectCase={props.onSelectCase} /><p className={`${muted} break-words`}>{plan.reason}</p>
    {plan.stale && <p className="mt-3 rounded bg-[var(--color-attention-bg)] p-3 text-sm text-[var(--color-attention)]">Case information, planning details or policy changed after planning. This plan is stale; review the current records and create a new plan if needed.</p>}
    {plan.planning_warning && <p className="mt-3 rounded bg-[var(--color-attention-bg)] p-3 text-sm text-[var(--color-attention)]">{plan.planning_warning}</p>}
    {!!plan.blockers?.length && <div className="mt-3"><h4 className="text-sm font-semibold">Outstanding requirements by case</h4><ul className="mt-2 space-y-3 text-sm">{plan.blockers.map((blocker, index) => <li key={index} className="break-words border-l-2 border-[var(--color-border)] pl-3"><p className="font-medium">{props.cases.find((item) => item.id === blocker.case_id)?.title || blocker.case_id}</p><p>{policyLabel(blocker.key)} · {policyLabel(blocker.status)}: {blocker.reason}</p><p className="text-xs text-[var(--color-muted)]">Owner: {policyLabel(blocker.owner)}</p></li>)}</ul></div>}
    {!plan.blockers?.length && plan.status !== 'cancelled' && <p className={`${muted} mt-3`}>No current blockers reported by this snapshot. This remains a tentative local plan, not a booking or permission to act.</p>}
    {plan.status !== 'cancelled' && <details className="mt-3"><summary className="cursor-pointer text-sm font-medium">Cancel this tentative plan</summary><form className="mt-3 space-y-3" onSubmit={(event) => { event.preventDefault(); void props.mutate(() => cancelVisitPlan(plan.id, reason.trim()), 'Tentative plan cancelled. No external booking was changed.'); }}><fieldset disabled={props.busy || !props.canManage} className="space-y-3 disabled:opacity-60"><legend className="sr-only">Cancel tentative plan</legend><Field label="Reason for cancellation"><input className={input} value={reason} onChange={(event) => setReason(event.target.value)} required minLength={3} maxLength={2000} /></Field><button className={button} type="submit">Cancel tentative plan</button></fieldset></form></details>}
  </article>;
}

export function PlanningPanel(props: OperationsProps) {
  const [contractorId, setContractorId] = useState('');
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [reason, setReason] = useState('');
  const [day, setDay] = useState('');
  const [error, setError] = useState('');
  async function submit() {
    setError('');
    try {
      const starts = localDateTimeToIso(start), ends = localDateTimeToIso(end);
      if (!starts || !ends || starts >= ends) throw new Error('Enter a visit window that ends after it starts.');
      const saved = await props.mutate(() => createVisitPlan({ contractor_id: contractorId, case_ids: selectedIds, start: starts, end: ends, reason: reason.trim() }), 'Tentative plan saved. No contractor was assigned, contacted or dispatched.');
      if (saved) { setReason(''); setSelectedIds([]); }
    } catch (failure) { setError(errorText(failure)); }
  }
  const plans = props.portfolio.plans.filter((plan) => !day || isoToLocalInput(plan.start).slice(0, 10) === day).slice().sort((a, b) => a.start.localeCompare(b.start));
  const grouped = new Map<string, VisitPlan[]>();
  for (const plan of plans) {
    const date = isoToLocalInput(plan.start).slice(0, 10);
    grouped.set(date, [...(grouped.get(date) || []), plan]);
  }
  return <div className="space-y-5">
    <div className="rounded-[var(--radius-sm)] bg-[var(--color-information-bg)] p-4 text-sm text-[var(--color-information)]">Planning uses staff-entered availability, trades and case windows. Every plan is tentative. Access, authority and other case checks remain independent; nothing here dispatches a contractor.</div>
    <div className="grid items-start gap-5 xl:grid-cols-2">
      <section className={card} aria-labelledby="portfolio-contractors"><h2 id="portfolio-contractors" className="text-lg font-semibold">Contractor availability</h2><p className={`${muted} mt-1`}>Record availability you have actually obtained. No directory or calendar has been connected.</p><ContractorForm {...props} />
        <details className="mt-5"><summary className="cursor-pointer font-medium">Recorded availability ({props.portfolio.contractors.length})</summary><div className="mt-3 space-y-3">{!props.portfolio.contractors.length ? <Empty>No availability recorded yet.</Empty> : props.portfolio.contractors.map((contractor) => <article key={contractor.id} className="break-words border-t border-[var(--color-border)] pt-3 text-sm"><h3 className="font-semibold">{contractor.name}</h3><p>{contractor.trades.join(', ')}</p><p>{dateLabel(contractor.available_from)} – {dateLabel(contractor.available_until)}</p><p className={muted}>{contractor.reason}</p></article>)}</div></details>
      </section>
      <section className={card} aria-labelledby="portfolio-plan"><h2 id="portfolio-plan" className="text-lg font-semibold">Propose a visit</h2><p className={`${muted} mt-1`}>The server checks trade, availability, time conflicts and confirmed case windows. Missing permission remains visible on a saved tentative plan.</p>
        <form onSubmit={(event) => { event.preventDefault(); void submit(); }} className="mt-4 space-y-3">{error && <p role="alert" className="text-sm text-[var(--color-danger)]">{error}</p>}
          <fieldset disabled={props.busy || !props.canManage} className="space-y-4 disabled:opacity-60"><legend className="sr-only">Create tentative visit plan</legend>
            <Field label="Contractor availability record"><select className={input} value={contractorId} onChange={(event) => setContractorId(event.target.value)} required><option value="">Choose recorded availability</option>{props.portfolio.contractors.map((contractor) => <option key={contractor.id} value={contractor.id}>{contractor.name} · {contractor.trades.join(', ')} · {dateLabel(contractor.available_from)}</option>)}</select></Field>
            <CaseSelection cases={props.cases} ids={selectedIds} onChange={setSelectedIds} />
            <DateWindow start={start} end={end} onStart={setStart} onEnd={setEnd} required fromLabel="Visit starts" toLabel="Visit ends" />
            <Field label="Reason for this visit plan"><textarea className={input} value={reason} onChange={(event) => setReason(event.target.value)} required minLength={3} maxLength={2000} /></Field>
            <button className={primary} type="submit" disabled={!contractorId || !selectedIds.length}>Save tentative plan</button>
          </fieldset>
        </form>
      </section>
    </div>
    <section className={card} aria-labelledby="portfolio-day-board"><div className="flex flex-wrap items-start justify-between gap-3"><div><h2 id="portfolio-day-board" className="text-lg font-semibold">Visit planning board</h2><p className={`${muted} mt-1`}>Dates shown in {timezone}. Refresh to check for changed case records.</p></div><Field label="Show a day (blank for all)"><input type="date" className={input} value={day} onChange={(event) => setDay(event.target.value)} /></Field></div>
      <div className="mt-5 space-y-5">{!plans.length ? <Empty>No tentative plans match this day.</Empty> : [...grouped.entries()].map(([date, entries]) => <section key={date} aria-label={`Plans for ${date}`}><h3 className="mb-3 font-semibold">{new Date(`${date}T12:00:00`).toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })}</h3><div className="grid gap-3 lg:grid-cols-2">{entries.map((plan) => <VisitCard key={plan.id} plan={plan} {...props} />)}</div></section>)}</div>
    </section>
  </div>;
}

export function HistoryPanel({ portfolio, cases, onSelectCase }: Pick<OperationsProps, 'portfolio' | 'cases' | 'onSelectCase'>) {
  const [query, setQuery] = useState('');
  const groups = new Map<string, CaseProfile[]>();
  for (const profile of portfolio.profiles) {
    if (query && !`${profile.property_key} ${profile.asset_ref} ${profile.trade} ${cases.find((item) => item.id === profile.case_id)?.title || ''}`.toLowerCase().includes(query.toLowerCase())) continue;
    const groupingKey = profile.property_group_key ?? profile.property_key.toLowerCase();
    const existing = groups.get(groupingKey) || [];
    groups.set(groupingKey, [...existing, profile]);
  }
  return <section className={card} aria-labelledby="portfolio-history"><h2 id="portfolio-history" className="text-lg font-semibold">Property and asset history</h2><p className={`${muted} mt-1`}>A case history based on confirmed profiles and recorded dates. Repeated reports do not by themselves prove the same fault or a failed repair.</p>
    <div className="mt-4 max-w-xl"><Field label="Find a building, asset, trade or case"><input type="search" className={input} value={query} onChange={(event) => setQuery(event.target.value)} /></Field></div>
    <div className="mt-5 space-y-5">{!groups.size ? <Empty>No confirmed property profiles match. Add a case profile in Related incidents to start a history.</Empty> : [...groups.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([property, profiles]) => <section key={property} className="min-w-0 rounded-[var(--radius-sm)] border border-[var(--color-border)] p-4"><h3 className="break-words text-lg font-semibold">{profiles[0].property_key}</h3><p className={muted}>{profiles.length} linked case{profiles.length === 1 ? '' : 's'} · {new Set(profiles.map((profile) => profile.asset_group_key ?? profile.asset_ref.toLowerCase()).filter(Boolean)).size} identified asset{new Set(profiles.map((profile) => profile.asset_group_key ?? profile.asset_ref.toLowerCase()).filter(Boolean)).size === 1 ? '' : 's'}</p>
      <ol className="mt-4 space-y-4">{profiles.slice().sort((a, b) => (cases.find((item) => item.id === a.case_id)?.created_at || a.created_at).localeCompare(cases.find((item) => item.id === b.case_id)?.created_at || b.created_at)).map((profile) => {
        const item = cases.find((entry) => entry.id === profile.case_id);
        return <li key={profile.id} className="min-w-0 border-l-2 border-[var(--color-border)] pl-4"><div className="flex flex-wrap items-start justify-between gap-2"><button type="button" className="min-h-11 break-words text-left font-semibold text-[var(--color-primary)] underline underline-offset-4" onClick={() => onSelectCase(profile.case_id)}>{item?.title || profile.case_id}</button>{item && <StatusBadge status={item.outcome} />}</div><dl className="mt-2 grid gap-2 text-sm sm:grid-cols-2"><div><dt className="text-[var(--color-muted)]">Case recorded</dt><dd>{dateLabel(item?.created_at)}</dd></div><div><dt className="text-[var(--color-muted)]">Asset / trade</dt><dd className="break-words">{profile.asset_ref || 'Asset unknown'} / {profile.trade}</dd></div><div><dt className="text-[var(--color-muted)]">Original property reference</dt><dd className="break-words">{profile.original_property_ref}</dd></div><div><dt className="text-[var(--color-muted)]">Profile confirmed</dt><dd>{dateLabel(profile.created_at)}</dd></div></dl>{item?.next_step && <p className="mt-2 break-words text-sm">Next step: {item.next_step}</p>}<p className={`${muted} mt-2 break-words`}>Profile source: {profile.reason}</p></li>;
      })}</ol>
    </section>)}</div>
  </section>;
}
