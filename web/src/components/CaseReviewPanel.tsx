import { useState } from 'react';
import type { Blocker, CaseDetail, Claim, Review, ReviewResponseInput } from '../lib/types';
import { findReviewForBlocker, readableFactKey, readableRole } from '../lib/pipeline';

const INPUT = 'mt-1 w-full rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] p-2.5 text-sm';
const BUTTON = 'rounded-[var(--radius-sm)] border border-[var(--color-border)] px-3 py-2 text-sm font-medium disabled:cursor-not-allowed disabled:opacity-50';
const CASE_MANAGER_FACTS = new Set(['identity', 'route', 'schedule', 'classification', 'commitments', 'urgent', 'supported', 'total', 'evidence']);

interface Props {
  detail: CaseDetail;
  sessionRole: string;
  checkedAt: number;
  busy: boolean;
  onRespond: (review: Review, response: ReviewResponseInput) => Promise<boolean>;
  onRefresh: () => void;
}

function validDeadline(date: Date, value: string): boolean {
  const now = Date.now();
  return Boolean(value) && !Number.isNaN(date.getTime()) && date.getTime() > now && date.getTime() <= now + 7 * 86400000;
}

function currentClaim(claim: Claim, review: Review): boolean {
  const entries = Object.entries(claim.scope);
  return entries.length > 0 && entries.every(([key, value]) => JSON.stringify(review.scope[key]) === JSON.stringify(value));
}

export default function CaseReviewPanel({ detail, sessionRole, checkedAt, busy, onRespond, onRefresh }: Props) {
  const [selectedKey, setSelectedKey] = useState<string | null>(null);
  const blockers = detail.decision?.blockers ?? [];
  const selected = blockers.find((blocker) => `${blocker.rule_id}:${blocker.key}` === selectedKey) ?? blockers[0];
  const review = selected && findReviewForBlocker(detail, selected);
  const questions = selected ? detail.questions.filter((question) => question.key === selected.key && question.status === 'open') : [];

  return (
    <section className="mt-5 rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-surface)] p-4 sm:p-5" aria-labelledby="review-heading">
      <h2 id="review-heading" className="text-base font-semibold">{blockers.length ? `What is holding this action? (${blockers.length})` : 'Required checks'}</h2>
      <p className="mt-1 text-sm text-[var(--color-muted)]">Each decision applies to the current proposed action. Other requirements stay in place.</p>
      {blockers.length === 0 ? (
        <p className="mt-3 text-sm">{detail.decision ? 'No blockers are recorded for this action.' : 'This request has not been assessed yet.'}</p>
      ) : (
        <>
          <div className="mt-4 flex flex-col gap-2" aria-label="Select a requirement">
            {blockers.map((blocker) => {
              const key = `${blocker.rule_id}:${blocker.key}`;
              const active = selected === blocker;
              return <button key={key} type="button" disabled={busy} aria-pressed={active} onClick={() => setSelectedKey(key)} className={`rounded-[var(--radius-sm)] border p-3 text-left ${active ? 'border-[var(--color-primary)] bg-[var(--color-success-bg)]' : 'border-[var(--color-border)]'}`}>
                <span className="flex flex-wrap justify-between gap-2 text-sm font-semibold"><span>{readableFactKey(blocker.key)}</span><span className="text-xs font-medium">{blocker.status} · {blocker.response.toLowerCase()}</span></span>
                <span className="mt-1 block text-sm">{blocker.reason}</span>
                <span className="mt-1 block text-xs text-[var(--color-muted)]">Decision owner: {readableRole(blocker.owner)}</span>
              </button>;
            })}
          </div>
          {selected && <div className="mt-4 border-t border-[var(--color-border)] pt-4">
            <h3 className="font-semibold text-sm">Review {readableFactKey(selected.key).toLowerCase()}</h3>
            <p className="mt-1 text-xs text-[var(--color-muted)]">Rule: {selected.rule_id} · Policy {detail.decision?.policy_version} · Action revision {detail.case.action_revision}</p>
            {review ? <ReviewForm key={review.id} review={review} blocker={selected} detail={detail} checkedAt={checkedAt} sessionRole={sessionRole} busy={busy} onRespond={onRespond} /> : <>
              <p className="mt-3 text-sm">There is no current staff review for this requirement. {questions.length ? 'The workflow is waiting on the question below.' : 'The affected action remains on hold; refresh to check for a new review.'}</p>
              {questions.map((question) => <div key={question.id} className="mt-2 rounded-[var(--radius-sm)] bg-[var(--color-canvas)] p-3 text-sm"><p>{question.question}</p><p className="mt-1 text-xs text-[var(--color-muted)]">Recorded question{question.simulated ? ' (simulated)' : ''} · {readableRole(question.owner)} · due {new Date(question.deadline).toLocaleString('en-GB')}</p></div>)}
              <button type="button" onClick={onRefresh} disabled={busy} className={`${BUTTON} mt-3`}>Refresh this case</button>
            </>}
          </div>}
        </>
      )}
      <details className="mt-4 border-t border-[var(--color-border)] pt-3">
        <summary className="cursor-pointer text-sm font-medium">Inspect source evidence ({detail.evidence.length}) and assertions ({detail.claims.length})</summary>
        <p className="mt-2 text-xs text-[var(--color-muted)]">Source text is a recorded assertion. It is not automatically verified permission or proof of completion.</p>
        <div className="mt-3 flex flex-col gap-3">
          {detail.evidence.map((source) => <details key={source.id} id={`source-${source.id}`} className="rounded-[var(--radius-sm)] border border-[var(--color-border)] p-3">
            <summary className="cursor-pointer break-words text-sm font-medium">{source.source_label || 'Source record'} · {new Date(source.occurred_at || source.created_at).toLocaleString('en-GB')}</summary>
            <p className="mt-2 break-all text-xs text-[var(--color-muted)]">{source.id} · Recorded by {readableRole(source.actor?.role ?? 'unknown')}</p>
            <pre className="mt-2 whitespace-pre-wrap [overflow-wrap:anywhere] font-[var(--font-body)] text-sm">{source.text}</pre>
            {detail.claims.filter((claim) => claim.source_id === source.id).map((claim) => <p key={claim.id} className="mt-2 border-t border-[var(--color-border)] pt-2 text-xs"><strong>{readableFactKey(claim.key)}: {String(claim.value)}</strong> · {claim.verified ? 'Verified assertion' : 'Unverified assertion'}{claim.superseded_by ? ' · superseded' : ''}{claim.expires_at && new Date(claim.expires_at).getTime() <= checkedAt ? ' · expired' : ''}<br />{claim.source_quote}</p>)}
          </details>)}
          {!detail.evidence.length && <p className="text-sm">No source evidence is attached.</p>}
        </div>
      </details>
    </section>
  );
}

function ReviewForm({ review, blocker, detail, checkedAt, sessionRole, busy, onRespond }: Omit<Props, 'onRefresh'> & { review: Review; blocker: Blocker }) {
  const [decision, setDecision] = useState<ReviewResponseInput['decision']>('more_evidence');
  const [reason, setReason] = useState('');
  const [claimId, setClaimId] = useState('');
  const [deadline, setDeadline] = useState('');
  const [confirmed, setConfirmed] = useState(false);
  const [validation, setValidation] = useState<string | null>(null);
  const ownReview = review.owner === sessionRole;
  const confirmTriage = review.key === 'triage' && detail.case.triage?.state === 'done' && sessionRole === 'case_manager';
  const canCorrect = sessionRole === 'case_manager' && CASE_MANAGER_FACTS.has(review.key);
  const candidates = detail.claims.filter((claim) => claim.key === review.key && currentClaim(claim, review) && !claim.superseded_by && (!claim.expires_at || new Date(claim.expires_at).getTime() > checkedAt));
  const chosenClaim = candidates.find((claim) => claim.id === claimId);
  const scopedApproval = ['authority', 'finance'].includes(review.key) || review.key.startsWith('rule:');

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setValidation(null);
    if (!ownReview || busy) return;
    if (reason.trim().length < 5) { setValidation('Explain the decision in at least five characters.'); return; }
    const response: ReviewResponseInput = { decision, reason: reason.trim() };
    if (decision === 'correct') {
      if (!chosenClaim || !confirmed) { setValidation('Choose a source assertion and confirm that you have checked the conflicting evidence.'); return; }
      response.claim_id = chosenClaim.id; response.source_id = chosenClaim.source_id; response.key = chosenClaim.key;
    }
    if (decision === 'reject' && !confirmed) { setValidation('Confirm that you intend to reject the current proposed action.'); return; }
    if (decision === 'defer') {
      const date = new Date(deadline);
      if (!validDeadline(date, deadline)) { setValidation('Choose a future deadline within seven days.'); return; }
      response.deadline = date.toISOString();
    }
    if (await onRespond(review, response)) { setReason(''); setClaimId(''); setConfirmed(false); setDeadline(''); }
  }

  return <form onSubmit={submit} className="mt-3">
    {!ownReview && <p className="mb-3 rounded-[var(--radius-sm)] bg-[var(--color-attention-bg)] p-3 text-sm">This review belongs to the {readableRole(review.owner)}. You are using the {readableRole(sessionRole)} demo role. No role is switched automatically.</p>}
    {scopedApproval && <p className="mb-3 text-sm text-[var(--color-muted)]">A scoped approval needs the authorised owner, an explicitly chosen source and an expiry within policy limits. Use the original staff workspace for that approval. A general approval cannot override {blocker.status === 'CONFLICT' ? 'conflicting evidence' : 'missing facts or permission'}.</p>}
    {review.key === 'triage' && !confirmTriage && <p className="mb-3 text-sm text-[var(--color-muted)]">This reading cannot be confirmed here. Use the original staff workspace to retry or choose the route manually.</p>}
    <fieldset disabled={busy || !ownReview} className="space-y-3 disabled:opacity-60">
      <label className="block text-sm font-medium">Response
        <select className={INPUT} value={decision} onChange={(event) => { setDecision(event.target.value as ReviewResponseInput['decision']); setConfirmed(false); setValidation(null); }}>
          <option value="more_evidence">Request more information (simulated)</option>
          {canCorrect && <option value="correct">Verify an existing source assertion</option>}
          {confirmTriage && <option value="approve">Confirm this interpretation</option>}
          <option value="defer">Wait until a deadline</option>
          <option value="reject">Reject the current proposed action</option>
        </select>
      </label>
      {decision === 'correct' && <div>
        <label className="block text-sm font-medium">Source assertion to verify
          <select className={INPUT} required value={claimId} onChange={(event) => { setClaimId(event.target.value); setConfirmed(false); }}>
            <option value="">Choose a source assertion</option>
            {candidates.map((claim) => <option key={claim.id} value={claim.id}>{String(claim.value)} · {detail.evidence.find((source) => source.id === claim.source_id)?.source_label ?? claim.source_id} · {claim.id.slice(-6)}</option>)}
          </select>
        </label>
        {!candidates.length && <p className="mt-2 text-sm">No source assertion matches this requirement and action. Add evidence in the original staff workspace first.</p>}
        {chosenClaim && <blockquote className="mt-2 whitespace-pre-wrap rounded-[var(--radius-sm)] bg-[var(--color-canvas)] p-3 text-sm">{chosenClaim.source_quote || 'No direct quote recorded.'}<br /><span className="text-xs">Source: {chosenClaim.source_id}</span></blockquote>}
        <div className="mt-2 text-xs text-[var(--color-muted)]">Current, unexpired assertions for this requirement: {candidates.map((claim) => `${String(claim.value)} (${claim.verified ? 'verified' : 'unverified'})`).join('; ') || 'none'}. Verification preserves the selected value and supersedes the matching assertions.</div>
      </div>}
      {decision === 'defer' && <label className="block text-sm font-medium">Resume review at (your local time)<input type="datetime-local" required className={INPUT} value={deadline} onChange={(event) => setDeadline(event.target.value)} /><span className="mt-1 block text-xs font-normal text-[var(--color-muted)]">Within seven days. The affected action stays on hold.</span></label>}
      <label className="block text-sm font-medium">{decision === 'more_evidence' ? 'What information is needed, and why?' : 'Reason for your decision'}
        <textarea required minLength={5} maxLength={3000} rows={3} className={INPUT} value={reason} onChange={(event) => setReason(event.target.value)} placeholder="Explain the evidence and what should happen next." />
      </label>
      {['reject', 'correct'].includes(decision) && <label className="flex items-start gap-2 text-sm"><input type="checkbox" required checked={confirmed} onChange={(event) => setConfirmed(event.target.checked)} className="mt-1" /><span>{decision === 'reject' ? 'Reject the current proposed action. This does not close the whole case.' : 'I have checked the source and opposing assertions. Verify this value and supersede the matching assertions.'}</span></label>}
      {validation && <p role="alert" className="text-sm text-[var(--color-danger)]">{validation}</p>}
      <button type="submit" disabled={busy || !ownReview || (decision === 'correct' && !chosenClaim)} className={`${BUTTON} bg-[var(--color-primary)] text-white`}>{busy ? 'Saving response…' : 'Record this response'}</button>
    </fieldset>
    <p className="mt-2 text-xs text-[var(--color-muted)]">The backend rechecks the current review and permissions before saving. Recording a request does not deliver a message.</p>
  </form>;
}
