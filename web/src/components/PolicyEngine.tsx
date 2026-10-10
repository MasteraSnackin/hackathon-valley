import { useEffect, useRef, useState } from 'react';
import { ApiError, createDemoSession, getSession } from '../lib/api';
import { getPolicies, interpretPolicy, previewPolicyDraft, publishPolicyDraft, savePolicyDraft } from '../lib/policy-api';
import { describePolicy, draftFromPublished, policyLabel } from '../lib/policies';
import type { PolicyCollection, PolicyDraft, PolicyDraftInput, PolicyPreview, PolicyRule, PolicySettings, PolicySuggestion } from '../lib/policies';

/** A distinct case-review handoff, including repeated wording from a new decision. */
export interface PolicyRequest {
  text: string;
  reviewId?: string;
  nonce: number;
}

interface PolicyEngineProps {
  request?: PolicyRequest | null;
  initialText?: string;
  onDraftConsumed?: () => void;
  onPublished?: () => void;
  sessionRole: string;
  onRoleChange: (role: string) => void;
}

const button = 'min-h-11 rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-2 text-sm font-medium text-[var(--color-ink)] hover:bg-[var(--color-canvas)] disabled:cursor-not-allowed disabled:opacity-50';
const primary = 'min-h-11 rounded-[var(--radius-sm)] bg-[var(--color-primary)] px-4 py-2 text-sm font-semibold text-white hover:bg-[var(--color-primary-hover)] disabled:cursor-not-allowed disabled:opacity-50';
const input = 'min-h-11 w-full rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2 text-sm text-[var(--color-ink)]';
const card = 'rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-surface)] p-4 sm:p-6';
const numberFields = [
  { key: 'review_limit', label: 'Review work costing more than (£)', min: 0, max: 1000000, step: 0.01, hint: 'Uses the verified total, including tax. Existing authority is still required.' },
  { key: 'approval_hours', label: 'Approval validity (hours)', min: 0.1, max: 720, step: 0.1, hint: 'How long a scoped approval remains valid.' },
  { key: 'reminder_hours', label: 'First reminder (working hours)', min: 0.1, max: 720, step: 0.1, hint: 'Measured from the original question.' },
  { key: 'escalation_hours', label: 'Escalation (working hours)', min: 0.1, max: 720, step: 0.1, hint: 'Also measured from the original question, after the first reminder.' },
  { key: 'reminder_limit', label: 'Maximum reminders per question', min: 0, max: 5, step: 1, hint: 'Zero disables reminders. It does not resolve the missing information.' },
] as const;
const examples = [
  ['Missing access', 'Escalate missing access permission immediately'],
  ['Follow-up timing', 'Remind after 4 working hours and escalate after 12 working hours'],
  ['Completion evidence', 'Require human review when completion is missing for closing a repair'],
] as const;
const tenantMessageModes: { value: PolicySettings['tenant_messages']; label: string }[] = [
  { value: 'claude_decides', label: 'Routine questions may send after policy checks' },
  { value: 'staff_approval', label: 'Every message needs staff approval' },
  { value: 'off', label: 'Do not draft tenant messages' },
];
const triageModes: { value: PolicySettings['triage_auto_accept']; label: string }[] = [
  { value: 'high', label: 'High confidence only' },
  { value: 'medium', label: 'Medium or high confidence' },
  { value: 'never', label: 'Every interpretation needs staff confirmation' },
];

function RuleSummary({ rule }: { rule: PolicyRule }) {
  return <div className="rounded-[var(--radius-sm)] border border-[var(--color-border)] p-3 text-sm">
    <p className="font-semibold">{policyLabel(rule.response)}</p>
    <p className="mt-1">When {rule.conditions.map((condition) => `${policyLabel(condition.key).toLowerCase()} is ${policyLabel(condition.status)}`).join(rule.match === 'any' ? ' or ' : ' and ')}.</p>
    <p className="mt-2 text-xs text-[var(--color-muted)]">Applies to: {rule.actions.length ? rule.actions.map(policyLabel).join(', ') : 'All actions'}{rule.property_ref ? ` at ${rule.property_ref}` : ' across all properties'}. Owner: {policyLabel(rule.owner)}.{rule.category ? ` Category: ${policyLabel(rule.category)}.` : ''}</p>
  </div>;
}

const errorText = (error: unknown) => error instanceof Error ? error.message : 'The request could not be completed. Please try again.';

export default function PolicyEngine({ request, initialText, onDraftConsumed, onPublished, sessionRole, onRoleChange }: PolicyEngineProps) {
  const [collection, setCollection] = useState<PolicyCollection | null>(null);
  const [working, setWorking] = useState<PolicyDraftInput | null>(null);
  const [saved, setSaved] = useState<PolicyDraft | null>(null);
  const [preview, setPreview] = useState<PolicyPreview | null>(null);
  const [text, setText] = useState(initialText ?? '');
  const [suggestion, setSuggestion] = useState<PolicySuggestion | null>(null);
  const [busy, setBusy] = useState<string | null>('load');
  const [error, setError] = useState('');
  const [notice, setNotice] = useState(initialText ? 'Review the proposed wording below. A case decision does not change the published policy.' : '');
  const [mode, setMode] = useState('');
  const [approved, setApproved] = useState(false);
  const [sourceReviewId, setSourceReviewId] = useState<string | undefined>();
  const composerRevision = useRef(0);
  const handledRequest = useRef<number | null>(null);
  const handledInitialText = useRef<string | null>(null);
  const canEdit = sessionRole === 'policy_editor';
  const previewCurrent = !!(saved && preview && working && preview.draft_id === saved.id
    && preview.active_version === working.base_version && saved.base_version === working.base_version);

  useEffect(() => {
    let active = true;
    Promise.all([getPolicies(), getSession()]).then(([policies, session]) => {
      if (!active) return;
      setCollection(policies); setWorking(draftFromPublished(policies.active));
      setMode(session.mode); setBusy(null);
    }).catch((failure) => { if (active) { setError(errorText(failure)); setBusy(null); } });
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!request && !initialText) return;
    if (request) {
      if (handledRequest.current === request.nonce) return;
      handledRequest.current = request.nonce;
    } else {
      if (handledInitialText.current === initialText) return;
      handledInitialText.current = initialText!;
    }
    // The panel stays mounted between tabs. A review handoff is an explicit
    // external event: replace only its composer text, preserving the policy
    // draft, saved comparison and publication state until the user adopts it.
    // oxlint-disable-next-line react/set-state-in-effect
    setText(request?.text ?? initialText!);
    setSourceReviewId(request?.reviewId);
    composerRevision.current += 1;
    setSuggestion(null);
    setNotice('New review wording is ready to edit. Your existing policy draft is unchanged until you use a suggestion.');
    onDraftConsumed?.();
  }, [request, initialText, onDraftConsumed]);

  useEffect(() => {
    // Publication confirmation belongs to the selected staff role.
    // oxlint-disable-next-line react/set-state-in-effect
    setApproved(false);
  }, [sessionRole]);

  useEffect(() => {
    if (preview) document.getElementById('policy-preview-heading')?.focus();
  }, [preview]);

  useEffect(() => {
    if (error) document.getElementById('policy-error')?.focus();
  }, [error]);

  function invalidatePreview() {
    setSaved(null); setPreview(null); setApproved(false);
    setNotice('Unsaved changes. Save and compare before publishing.'); setError('');
  }

  async function reload() {
    setBusy('load'); setError('');
    try {
      const [policies, session] = await Promise.all([getPolicies(), getSession()]);
      setMode(session.mode);
      setCollection(policies); setWorking(draftFromPublished(policies.active));
      setSaved(null); setPreview(null); setApproved(false); setSuggestion(null);
      setNotice('Loaded the current published policy.');
    } catch (failure) { setError(errorText(failure)); }
    finally { setBusy(null); }
  }

  async function prepareSuggestion() {
    if (!text.trim() || busy) return;
    const revision = composerRevision.current;
    setBusy('interpret'); setError(''); setSuggestion(null);
    try {
      const result = await interpretPolicy(text.trim(), sourceReviewId);
      if (revision === composerRevision.current) setSuggestion(result);
    } catch (failure) {
      if (revision === composerRevision.current) setError(errorText(failure));
    }
    finally { setBusy(null); }
  }

  async function switchRole() {
    setBusy('role'); setError('');
    try {
      await createDemoSession('policy_editor'); onRoleChange('policy_editor');
      setNotice('Policy editor demo role selected. You can now save, preview and publish a policy.');
    } catch (failure) { setError(errorText(failure)); }
    finally { setBusy(null); }
  }

  async function compare() {
    if (!working || !canEdit || busy) return;
    setError(''); setSaved(null); setPreview(null); setApproved(false);
    if (numberFields.some(({ key, min, max }) => !Number.isFinite(working.settings[key]) || working.settings[key] < min || working.settings[key] > max)) {
      setError('Enter a valid number for every threshold.'); return;
    }
    if (working.settings.escalation_hours <= working.settings.reminder_hours) {
      setError('Escalation must be later than the first reminder. Both delays start from the original question.'); return;
    }
    if (working.reason.trim().length < 3) { setError('Add a reason for the policy change.'); return; }
    setBusy('preview');
    try {
      const draft = await savePolicyDraft(working); setSaved(draft);
      setPreview(await previewPolicyDraft(draft.id));
      setNotice('Draft saved and compared with the current cases. Review the effect below before publishing.');
    } catch (failure) { setError(errorText(failure)); }
    finally { setBusy(null); }
  }

  async function publish() {
    if (!saved || !previewCurrent || !approved || !canEdit || busy) return;
    setBusy('publish'); setError('');
    try {
      const published = await publishPolicyDraft(saved.id);
      setCollection((current) => current ? { ...current, active: published } : null);
      setWorking(draftFromPublished(published)); setSaved(null); setPreview(null); setApproved(false); setSuggestion(null);
      setNotice(`Version ${published.version} published. Cases must be reassessed under this version before further action; the configured workflow handles reassessment.`);
      onPublished?.();
    } catch (failure) {
      setError(errorText(failure)); setApproved(false);
      if (failure instanceof ApiError && failure.status === 409) {
        setSaved(null); setPreview(null);
        setNotice('The comparison is no longer current. Your draft settings are preserved. Compare again, or reload the published policy if its version has changed.');
      }
    }
    finally { setBusy(null); }
  }

  return <div className="mx-auto w-full max-w-[1080px] space-y-6 px-4 py-6 sm:px-6">
    <div className="flex flex-wrap items-start justify-between gap-3">
      <div><h1 className="text-2xl font-bold tracking-tight">Policy settings</h1>
        <p className="mt-1 max-w-2xl text-sm text-[var(--color-muted)]">Decide when the agent asks for information, waits or needs a person. Check the effect on saved cases before publishing.</p>
      </div>
      <span className="rounded-full bg-[var(--color-information-bg)] px-3 py-1.5 text-xs font-medium text-[var(--color-information)]">{policyLabel(sessionRole || 'No staff session')}{mode === 'demo' ? ' · Demo' : ''}</span>
    </div>
    {error && <div id="policy-error" role="alert" tabIndex={-1} className="rounded-[var(--radius-sm)] border border-[var(--color-danger)] bg-[var(--color-danger-bg)] p-4 text-sm text-[var(--color-danger)]">{error}
      {!collection && <button type="button" className={`${button} ml-3`} disabled={!!busy} onClick={reload}>Retry</button>}
    </div>}
    {notice && <p role="status" className="rounded-[var(--radius-sm)] bg-[var(--color-information-bg)] p-3 text-sm text-[var(--color-information)]">{notice}</p>}
    {busy === 'load' && <p role="status" className="text-sm text-[var(--color-muted)]">Loading the published policy…</p>}

    {collection && working && <>
      <div className="grid gap-5 lg:grid-cols-[1fr_300px]">
        <section className={card} aria-labelledby="policy-composer-heading">
          <h2 id="policy-composer-heading" className="text-base font-semibold">Describe a change</h2>
          <p id="policy-composer-help" className="mt-1 text-sm text-[var(--color-muted)]">Supported wording becomes a draft suggestion. If the request is unclear, the service asks for more detail.</p>
          {sourceReviewId && <p className="mt-2 break-words text-xs text-[var(--color-muted)]">Source review: {sourceReviewId}. This decision applies to one case; its permissions do not transfer to other cases.</p>}
          <form className="mt-4 space-y-3" onSubmit={(event) => { event.preventDefault(); void prepareSuggestion(); }}>
            <label className="block text-sm font-medium" htmlFor="policy-description">What should happen, and when?</label>
            <textarea id="policy-description" className={`${input} min-h-28 resize-y`} value={text} required maxLength={4000} disabled={!!busy}
              aria-describedby="policy-composer-help" placeholder="For example: require human review when completion is missing for closing a repair."
              onChange={(event) => { composerRevision.current += 1; setText(event.target.value); setSuggestion(null); }} />
            <div className="flex flex-wrap gap-2" aria-label="Policy wording examples">{examples.map(([label, value]) => <button key={label} type="button" className={`${button} text-xs`} disabled={!!busy} onClick={() => { composerRevision.current += 1; setText(value); setSourceReviewId(undefined); setSuggestion(null); }}>{label}</button>)}</div>
            <button className={primary} type="submit" disabled={!!busy || !text.trim()}>{busy === 'interpret' ? 'Checking wording…' : 'Prepare suggestion'}</button>
          </form>
          {suggestion && <div className="mt-4 space-y-3 rounded-[var(--radius-sm)] bg-[var(--color-canvas)] p-4" aria-live="polite">
            <h3 className="font-semibold">{suggestion.status === 'ready' ? 'Suggested change' : suggestion.status === 'clarification' ? 'More detail needed' : 'Wording needs revision'}</h3>
            <p className="text-sm">{suggestion.summary}</p>
            {!!suggestion.questions.length && <ul className="list-disc space-y-1 pl-5 text-sm">{suggestion.questions.map((question) => <li key={question}>{question}</li>)}</ul>}
            {!!suggestion.warnings.length && <details className="text-sm text-[var(--color-muted)]"><summary className="cursor-pointer font-medium">Scope and safeguards</summary><ul className="mt-2 list-disc space-y-1 pl-5">{suggestion.warnings.map((warning) => <li key={warning}>{warning}</li>)}</ul></details>}
            {suggestion.status === 'ready' && suggestion.draft && <p className="text-xs text-[var(--color-muted)]">Using this suggestion replaces any unsaved changes in the draft below.</p>}
            {suggestion.status === 'ready' && suggestion.draft && <button className={button} type="button" disabled={!!busy} onClick={() => {
              setWorking(structuredClone(suggestion.draft!)); invalidatePreview();
              setNotice('Suggestion loaded into the draft below. This replaces any unsaved draft changes; nothing is published.');
              document.getElementById('policy-draft-heading')?.focus();
            }}>Use suggestion as draft</button>}
          </div>}
        </section>
        <aside className={card} aria-labelledby="policy-published-heading">
          <p className="text-xs font-semibold uppercase tracking-wide text-[var(--color-muted)]">Published policy</p>
          <h2 id="policy-published-heading" className="mt-2 text-2xl font-semibold">Version {collection.active.version}</h2>
          <dl className="mt-5 space-y-4 text-sm">
            <div><dt className="text-[var(--color-muted)]">Financial review</dt><dd className="font-medium">Above £{collection.active.settings.review_limit.toLocaleString('en-GB')}</dd></div>
            <div><dt className="text-[var(--color-muted)]">Missing access permission</dt><dd className="font-medium">{collection.active.settings.access_immediate_review ? 'Human review first' : 'Request permission first'}</dd></div>
            <div><dt className="text-[var(--color-muted)]">First reminder / escalation</dt><dd className="font-medium">{collection.active.settings.reminder_hours} / {collection.active.settings.escalation_hours} working hours</dd></div>
            <div><dt className="text-[var(--color-muted)]">Additional rules</dt><dd className="font-medium">{collection.active.rules.length}</dd></div>
            <div><dt className="text-[var(--color-muted)]">Tenant messages</dt><dd className="font-medium">{tenantMessageModes.find((mode) => mode.value === collection.active.settings.tenant_messages)?.label ?? collection.active.settings.tenant_messages}</dd></div>
            <div><dt className="text-[var(--color-muted)]">Automatic triage acceptance</dt><dd className="font-medium">{triageModes.find((mode) => mode.value === collection.active.settings.triage_auto_accept)?.label ?? collection.active.settings.triage_auto_accept}</dd></div>
            <div><dt className="text-[var(--color-muted)]">Published by</dt><dd className="break-words font-medium">{collection.active.author}</dd></div>
            <div><dt className="text-[var(--color-muted)]">Effective from</dt><dd className="font-medium"><time dateTime={collection.active.effective_at}>{new Date(collection.active.effective_at).toLocaleString('en-GB')}</time></dd></div>
            <div><dt className="text-[var(--color-muted)]">Reason</dt><dd className="break-words">{collection.active.reason}</dd></div>
          </dl>
          <details className="mt-4 text-sm"><summary className="cursor-pointer font-medium">Read the published rules</summary><ul className="mt-3 list-disc space-y-3 pl-5 text-xs text-[var(--color-muted)]">{describePolicy(collection.active).map((item) => <li key={item.id}>{item.text}</li>)}</ul></details>
          <p className="mt-5 border-t border-[var(--color-border)] pt-4 text-xs text-[var(--color-muted)]">Identity, consent and authority checks still apply. Changing a policy does not grant permission to enter a property.</p>
        </aside>
      </div>

      {!canEdit && <section className="flex flex-wrap items-center justify-between gap-3 rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-information-bg)] p-4" aria-label="Policy editing role">
        <div><h2 className="text-sm font-semibold">A policy editor must save and publish changes</h2><p className="mt-1 text-sm">Your current role can read policies and explore a suggestion.</p></div>
        {mode === 'demo' && <button className={button} type="button" disabled={!!busy} onClick={switchRole}>{busy === 'role' ? 'Changing demo role…' : 'Use policy editor demo role'}</button>}
      </section>}

      <section className={card} aria-labelledby="policy-draft-heading">
        <div className="flex flex-wrap items-start justify-between gap-3"><div>
          <h2 id="policy-draft-heading" tabIndex={-1} className="text-lg font-semibold">Review draft settings</h2>
          <p className="mt-1 text-sm text-[var(--color-muted)]">Based on version {working.base_version}. Changes apply only after a preview and explicit publication.</p>
        </div><button className={button} type="button" disabled={!!busy} onClick={reload}>Discard draft & reload published</button></div>
        <form className="mt-5" onSubmit={(event) => { event.preventDefault(); void compare(); }}>
          <fieldset disabled={!canEdit || !!busy} className="space-y-5 disabled:opacity-70">
            <legend className="sr-only">Proposed policy settings</legend>
            <div className="flex items-start gap-3 rounded-[var(--radius-sm)] bg-[var(--color-canvas)] p-4">
              <input id="policy-immediate-access" type="checkbox" className="mt-1 h-5 w-5 accent-[var(--color-primary)]" checked={working.settings.access_immediate_review}
                onChange={(event) => { setWorking({ ...working, settings: { ...working.settings, access_immediate_review: event.target.checked } }); invalidatePreview(); }} aria-describedby="policy-access-help" />
              <div><label htmlFor="policy-immediate-access" className="text-sm font-medium">Send missing access permission straight to human review</label>
                <p id="policy-access-help" className="mt-1 text-xs text-[var(--color-muted)]">When off, ask for permission through a verified contact route first. Entry stays blocked until permission is established.</p></div>
            </div>
            <div className="grid gap-5 sm:grid-cols-2">{numberFields.map((field) => <div key={field.key}>
              <label className="mb-1.5 block text-sm font-medium" htmlFor={`policy-${field.key}`}>{field.label}</label>
              <input id={`policy-${field.key}`} type="number" className={input} min={field.min} max={field.max} step={field.step} required
                value={Number.isNaN(working.settings[field.key]) ? '' : working.settings[field.key]} aria-describedby={`policy-${field.key}-help`}
                onChange={(event) => { setWorking({ ...working, settings: { ...working.settings, [field.key]: event.target.value === '' ? NaN : Number(event.target.value) } }); invalidatePreview(); }} />
              <p id={`policy-${field.key}-help`} className="mt-1.5 text-xs text-[var(--color-muted)]">{field.hint}</p>
            </div>)}</div>
            <div className="grid gap-5 sm:grid-cols-2">
              <div><label className="mb-1.5 block text-sm font-medium" htmlFor="policy-tenant-messages">Tenant-message mode</label>
                <select id="policy-tenant-messages" className={input} value={working.settings.tenant_messages} aria-describedby="policy-tenant-messages-help"
                  onChange={(event) => { setWorking({ ...working, settings: { ...working.settings, tenant_messages: event.target.value as PolicySettings['tenant_messages'] } }); invalidatePreview(); }}>
                  {tenantMessageModes.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
                </select>
                <p id="policy-tenant-messages-help" className="mt-1.5 text-xs text-[var(--color-muted)]">Identity, contact-route and risk checks still apply. External delivery is simulated in this build.</p>
              </div>
              <div><label className="mb-1.5 block text-sm font-medium" htmlFor="policy-triage-auto-accept">Accept message interpretations automatically</label>
                <select id="policy-triage-auto-accept" className={input} value={working.settings.triage_auto_accept} aria-describedby="policy-triage-auto-accept-help"
                  onChange={(event) => { setWorking({ ...working, settings: { ...working.settings, triage_auto_accept: event.target.value as PolicySettings['triage_auto_accept'] } }); invalidatePreview(); }}>
                  {triageModes.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
                </select>
                <p id="policy-triage-auto-accept-help" className="mt-1.5 text-xs text-[var(--color-muted)]">Lower-confidence interpretations require staff confirmation. Accepted interpretations do not override consent or authority checks.</p>
              </div>
            </div>
            <p className="text-xs text-[var(--color-muted)]">Working hours are Monday to Friday, 09:00 to 17:00 Europe/London, excluding the policy’s configured holidays. An unanswered question keeps its original deadline.</p>
            <div><label className="mb-1.5 block text-sm font-medium" htmlFor="policy-reason">Reason for this change</label>
              <textarea id="policy-reason" className={`${input} min-h-20`} value={working.reason} required minLength={3} maxLength={1000}
                placeholder="Explain the intended change for the version history."
                onChange={(event) => { setWorking({ ...working, reason: event.target.value }); invalidatePreview(); }} /></div>
            <div className="space-y-2"><h3 className="text-sm font-semibold">Additional rules in this draft ({working.rules.length})</h3>
              {working.rules.length ? <div className="grid gap-3 sm:grid-cols-2">{working.rules.map((rule) => <div key={rule.id} className="space-y-2"><RuleSummary rule={rule} /><button type="button" className={`${button} text-xs`} aria-label={`Remove rule ${rule.id} from draft`} onClick={() => {
                setWorking({ ...working, rules: working.rules.filter((candidate) => candidate.id !== rule.id) }); invalidatePreview();
              }}>Remove from draft</button></div>)}</div> : <p className="text-sm text-[var(--color-muted)]">No additional rules. The required identity, permission, authority and evidence checks still apply.</p>}
            </div>
            <details className="text-sm text-[var(--color-muted)]"><summary className="cursor-pointer">View all draft settings</summary><p className="mt-2">Other settings are preserved. This editor changes the fields above and supported plain-English conditions.</p><pre className="mt-3 max-h-64 overflow-auto rounded-[var(--radius-sm)] bg-[var(--color-canvas)] p-3 text-xs">{JSON.stringify(working.settings, null, 2)}</pre></details>
            <button className={primary} type="submit">{busy === 'preview' ? 'Saving and comparing…' : 'Save draft & compare cases'}</button>
          </fieldset>
        </form>
      </section>

      {previewCurrent && preview && saved && <section className={card} aria-labelledby="policy-preview-heading">
        <h2 id="policy-preview-heading" tabIndex={-1} className="text-lg font-semibold">Review the effect</h2>
        <p className="mt-1 text-sm text-[var(--color-muted)]">{preview.affected.length} saved cases compared; {preview.affected.filter((item) => item.changed).length} have different blockers. This preview does not execute actions.</p>
        {preview.affected.length ? <div className="mt-4 space-y-3">{preview.affected.map((item) => <div key={item.case_id} className="rounded-[var(--radius-sm)] border border-[var(--color-border)] p-3">
          <div className="flex flex-wrap items-center justify-between gap-2"><h3 className="text-sm font-medium">{item.title}</h3><span className={`rounded-full px-2 py-1 text-xs ${item.changed ? 'bg-[var(--color-attention-bg)] text-[var(--color-attention)]' : 'bg-[var(--color-canvas)] text-[var(--color-muted)]'}`}>{item.changed ? 'Blockers changed' : 'No change'}</span></div>
          <p className="mt-1 text-sm">{policyLabel(item.before)} → {policyLabel(item.after)}</p>
          {!!item.blockers.length && <p className="mt-1 text-xs text-[var(--color-muted)]">Still needs: {item.blockers.map(policyLabel).join(', ')}.</p>}
        </div>)}</div> : <p className="mt-4 text-sm text-[var(--color-attention)]">There are no saved cases to compare. This preview has not tested the policy against any cases.</p>}
        <div className="mt-5 space-y-4 border-t border-[var(--color-border)] pt-5">
          <label className="flex items-start gap-3 text-sm"><input type="checkbox" className="mt-0.5 h-5 w-5 shrink-0 accent-[var(--color-primary)]" checked={approved} disabled={!!busy || !canEdit} onChange={(event) => setApproved(event.target.checked)} /><span>I have reviewed the settings and case comparison. Publish this policy for future assessments and reassessment of existing cases.</span></label>
          <button className={primary} type="button" disabled={!!busy || !canEdit || !approved || !previewCurrent} onClick={publish}>{busy === 'publish' ? 'Publishing…' : 'Publish previewed policy'}</button>
        </div>
      </section>}
    </>}
  </div>;
}
