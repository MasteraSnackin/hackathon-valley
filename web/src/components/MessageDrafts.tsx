import { useState } from 'react';
import type { TenantMessage } from '../lib/types';

interface MessageDraftsProps {
  messages: TenantMessage[];
  actionRevision: number;
  busy: boolean;
  canManage: boolean;
  onSend: (id: string, text: string) => void;
  onReject: (id: string, reason: string, redraft: boolean) => void;
}

const STATUS_LABEL: Record<string, string> = {
  awaiting_staff: 'Awaiting staff review',
  held: 'Held: contact route unverified',
  draft_failed: 'Model draft failed',
};
const RECIPIENT_LABEL: Record<string, string> = {
  tenant: 'tenant', landlord: 'landlord', agency: 'letting agency', contractor: 'contractor', other: 'recipient',
};
const BUTTON = 'rounded-[var(--radius-sm)] border border-[var(--color-border)] px-3 py-2 text-sm font-medium disabled:cursor-not-allowed disabled:opacity-50';

/** Held model drafts; every send is a simulated adapter operation. */
export default function MessageDrafts({ messages, ...props }: MessageDraftsProps) {
  const open = messages.filter((message) => message.status in STATUS_LABEL);
  if (!open.length) return null;
  return <section aria-label="Message drafts" className="mb-5 flex flex-col gap-3">
    {open.map((message) => <DraftCard key={message.id} message={message} {...props} />)}
  </section>;
}

function DraftCard({ message, actionRevision, busy, canManage, onSend, onReject }: Omit<MessageDraftsProps, 'messages'> & { message: TenantMessage }) {
  const [text, setText] = useState(message.text ?? '');
  const [rejecting, setRejecting] = useState(false);
  const [reason, setReason] = useState('');
  const reasons = message.gate?.reasons ?? [];
  const recipient = RECIPIENT_LABEL[message.recipient?.kind ?? 'tenant'] ?? 'recipient';
  const stale = message.action_revision !== actionRevision;
  const disabled = busy || !canManage;
  const canSend = !disabled && !stale && message.status !== 'held' && Boolean(text.trim());

  return <div className="rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-information-bg)] p-4">
    <div className="flex flex-wrap items-center justify-between gap-3">
      <h2 className="text-sm font-semibold">{message.status === 'draft_failed' ? 'Write a message' : 'Review message draft'} to the {recipient}</h2>
      <span className="rounded-full bg-[var(--color-surface)] px-3 py-1 text-xs">{STATUS_LABEL[message.status]}</span>
    </div>
    {reasons.length > 0 && <ul className="mt-2 list-disc pl-5 text-xs text-[var(--color-muted)]">{reasons.map((reason) => <li key={reason}>{reason}</li>)}</ul>}
    {stale && <p className="mt-2 text-sm">The proposed action changed after this draft. This draft cannot be sent; reject it and request a new draft if needed.</p>}
    {!canManage && <p className="mt-2 text-sm">Only the case manager can send or reject drafts. Use the case manager demo role explicitly to continue.</p>}
    <label className="mt-3 block text-sm font-medium">Message to the {recipient}
      <textarea value={text} disabled={disabled} onChange={(event) => setText(event.target.value)} rows={4} className="mt-1 w-full resize-y rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] p-3 font-normal disabled:opacity-60" />
    </label>
    {rejecting ? <div className="mt-3">
      <label className="block text-sm font-medium">Reason for rejection
        <input type="text" value={reason} disabled={disabled} onChange={(event) => setReason(event.target.value)} className="mt-1 w-full rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] p-3 font-normal" />
      </label>
      <p className="mt-1 text-xs text-[var(--color-muted)]">At least five characters. The model uses this reason if you request a redraft.</p>
      <div className="mt-2 flex flex-wrap gap-2">
        <button type="button" className={BUTTON} disabled={disabled || reason.trim().length < 5} onClick={() => onReject(message.id, reason.trim(), true)}>Reject and request redraft</button>
        <button type="button" className={BUTTON} disabled={disabled || reason.trim().length < 5} onClick={() => onReject(message.id, reason.trim(), false)}>Reject only</button>
        <button type="button" className={BUTTON} disabled={busy} onClick={() => setRejecting(false)}>Cancel rejection</button>
      </div>
    </div> : <div className="mt-3 flex flex-wrap gap-2">
      <button type="button" className={BUTTON} disabled={!canSend} onClick={() => onSend(message.id, text.trim())}>Send to {recipient} (simulated)</button>
      <button type="button" className={BUTTON} disabled={disabled} onClick={() => setRejecting(true)}>Reject draft</button>
    </div>}
    <p className="mt-2 text-xs text-[var(--color-muted)]">Simulated delivery is recorded in the case. No real message is sent.</p>
  </div>;
}
