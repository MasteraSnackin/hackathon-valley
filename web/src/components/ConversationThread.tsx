import type { EvidenceItem } from './types'

interface ConversationThreadProps {
  evidence: EvidenceItem[]
}

function isTenant(sourceLabel: string): boolean {
  return sourceLabel.toLowerCase().includes('tenant')
}

function formatTime(occurredAt?: string | null): string | null {
  if (!occurredAt) return null
  const date = new Date(occurredAt)
  if (Number.isNaN(date.getTime())) return null
  return date.toLocaleString(undefined, {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

/**
 * Read-only, WhatsApp-style view of evidence items. Tenant messages align left
 * in a grey bubble; staff/agent/system entries align right in a green-tinted
 * bubble. There is no input box — the real conversation happens in WhatsApp.
 */
export default function ConversationThread({ evidence }: ConversationThreadProps) {
  if (evidence.length === 0) {
    return <p className="text-sm text-[var(--color-muted)]">No conversation recorded yet.</p>
  }

  return (
    <div className="flex flex-col gap-3">
      {evidence.map((item) => {
        const tenant = isTenant(item.source_label)
        const time = formatTime(item.occurred_at)

        return (
          <div key={item.id} className={`flex flex-col ${tenant ? 'items-start' : 'items-end'}`}>
            <span className="mb-1 px-1 text-xs text-[var(--color-muted)]">{item.source_label}</span>
            <div
              className={`max-w-[80%] rounded-[var(--radius-md)] px-3 py-2 text-sm ${
                tenant
                  ? 'bg-[var(--color-canvas)] text-[var(--color-ink)]'
                  : 'bg-[var(--color-success-bg)] text-[var(--color-ink)]'
              }`}
            >
              <p className="whitespace-pre-wrap">{item.text}</p>
            </div>
            {time && <span className="mt-1 px-1 text-xs text-[var(--color-muted)]">{time}</span>}
          </div>
        )
      })}
    </div>
  )
}
