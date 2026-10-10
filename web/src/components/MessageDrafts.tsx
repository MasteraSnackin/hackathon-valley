import { useState } from 'react';
import type { TenantMessage } from '../lib/types';

interface MessageDraftsProps {
  messages: TenantMessage[];
  busy: boolean;
  onSend: (id: string, text: string) => void;
  onReject: (id: string, reason: string, redraft: boolean) => void;
}

const STATUS_LABEL: Record<string, string> = {
  awaiting_staff: 'Waiting for you',
  held: 'Held — contact route unverified',
  draft_failed: 'Claude could not draft',
};

/** Claude-drafted tenant messages the policy gate held back for a person. */
export default function MessageDrafts({ messages, busy, onSend, onReject }: MessageDraftsProps) {
  const open = messages.filter((m) => m.status in STATUS_LABEL);
  if (open.length === 0) return null;
  return (
    <div className="mb-5 flex flex-col gap-3">
      {open.map((m) => (
        <DraftCard key={m.id} message={m} busy={busy} onSend={onSend} onReject={onReject} />
      ))}
    </div>
  );
}

function DraftCard({
  message,
  busy,
  onSend,
  onReject,
}: {
  message: TenantMessage;
  busy: boolean;
  onSend: MessageDraftsProps['onSend'];
  onReject: MessageDraftsProps['onReject'];
}) {
  const [text, setText] = useState(message.text ?? '');
  const [rejecting, setRejecting] = useState(false);
  const [reason, setReason] = useState('');
  const reasons = message.gate?.reasons ?? [];

  return (
    <div
      className="rounded-[var(--radius-md)] border p-4"
      style={{ borderColor: 'var(--color-border)', background: 'var(--color-information-bg)' }}
    >
      <div className="flex items-center justify-between gap-3">
        <p className="text-[13px] font-semibold text-[var(--color-ink)]">
          Claude drafted a message to the tenant
        </p>
        <span className="shrink-0 rounded-full bg-[var(--color-surface)] px-2.5 py-0.5 text-[11px] font-medium text-[var(--color-information)]">
          {STATUS_LABEL[message.status]}
        </span>
      </div>
      {reasons.length > 0 && (
        <ul className="mt-1.5 list-disc pl-5 text-[12px] text-[var(--color-muted)]">
          {reasons.map((r) => (
            <li key={r}>{r}</li>
          ))}
        </ul>
      )}
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={4}
        placeholder="Write the message to the tenant…"
        className="mt-3 w-full resize-y rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] px-3.5 py-2.5 text-[13px] text-[var(--color-ink)] outline-none focus:border-[var(--color-primary)]"
      />
      {rejecting ? (
        <div className="mt-2 flex flex-wrap items-center gap-2">
          <input
            type="text"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="Why? Claude uses this for the redraft"
            className="min-w-[220px] flex-1 rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2 text-[13px] outline-none focus:border-[var(--color-primary)]"
          />
          <button
            type="button"
            disabled={busy || reason.trim().length < 5}
            onClick={() => onReject(message.id, reason.trim(), true)}
            className="rounded-[var(--radius-sm)] bg-[var(--color-primary)] px-4 py-2 text-[13px] font-semibold text-white hover:bg-[var(--color-primary-hover)] disabled:opacity-50"
          >
            Ask Claude to redraft
          </button>
          <button
            type="button"
            disabled={busy || reason.trim().length < 5}
            onClick={() => onReject(message.id, reason.trim(), false)}
            className="rounded-[var(--radius-sm)] border border-[var(--color-border)] px-4 py-2 text-[13px] font-medium text-[var(--color-ink)] hover:bg-[var(--color-canvas)] disabled:opacity-50"
          >
            Reject only
          </button>
        </div>
      ) : (
        <div className="mt-2 flex gap-2">
          <button
            type="button"
            disabled={busy || !text.trim() || message.status === 'held'}
            onClick={() => onSend(message.id, text.trim())}
            className="rounded-[var(--radius-sm)] bg-[var(--color-primary)] px-4 py-2 text-[13px] font-semibold text-white hover:bg-[var(--color-primary-hover)] disabled:opacity-50"
          >
            Send to tenant
          </button>
          <button
            type="button"
            disabled={busy}
            onClick={() => setRejecting(true)}
            className="rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-transparent px-4 py-2 text-[13px] font-medium text-[var(--color-ink)] hover:bg-[var(--color-canvas)]"
          >
            Reject
          </button>
        </div>
      )}
      <p className="mt-2 text-[11px] text-[var(--color-muted)]">
        Simulated delivery to the in-app tenant thread — no real message is sent.
      </p>
    </div>
  );
}
