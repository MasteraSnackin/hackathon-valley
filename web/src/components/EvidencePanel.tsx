import type { EvidenceItem, EvidenceClaim } from './types'

interface EvidencePanelProps {
  evidence: EvidenceItem[]
}

function formatClaimValue(value: boolean | number): string {
  if (typeof value === 'boolean') return value ? 'Yes' : 'No'
  return String(value)
}

function ClaimRow({ claim }: { claim: EvidenceClaim }) {
  const verified = claim.verified
  const pillClasses = verified
    ? 'text-[var(--color-success)] bg-[var(--color-success-bg)]'
    : 'text-[var(--color-attention)] bg-[var(--color-attention-bg)]'

  return (
    <li className="flex flex-col gap-1 border-t border-[var(--color-border)] py-2 first:border-t-0 first:pt-0">
      <div className="flex items-center justify-between gap-3">
        <span className="text-sm font-medium text-[var(--color-ink)]">{claim.key}</span>
        <span className={`inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs font-medium ${pillClasses}`}>
          {verified ? 'Verified' : 'Unverified'}
        </span>
      </div>
      <p className="text-sm text-[var(--color-muted)]">
        Value: <span className="text-[var(--color-ink)]">{formatClaimValue(claim.value)}</span>
      </p>
      <p className="text-sm italic text-[var(--color-muted)]">"{claim.source_quote}"</p>
    </li>
  )
}

/**
 * Expandable list of evidence entries. Each entry shows its source, text,
 * and the claims extracted from it (with the exact supporting quote).
 */
export default function EvidencePanel({ evidence }: EvidencePanelProps) {
  if (evidence.length === 0) {
    return <p className="text-sm text-[var(--color-muted)]">No evidence recorded yet.</p>
  }

  return (
    <div className="flex flex-col gap-2">
      {evidence.map((item) => {
        const time = item.occurred_at ? new Date(item.occurred_at) : null
        const timeLabel =
          time && !Number.isNaN(time.getTime())
            ? time.toLocaleString(undefined, {
                day: 'numeric',
                month: 'short',
                hour: '2-digit',
                minute: '2-digit',
              })
            : null

        return (
          <details
            key={item.id}
            className="rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-3"
          >
            <summary className="flex cursor-pointer list-none items-center justify-between gap-3">
              <span className="text-sm font-medium text-[var(--color-ink)]">{item.source_label}</span>
              {timeLabel && <span className="text-xs text-[var(--color-muted)]">{timeLabel}</span>}
            </summary>
            <div className="mt-3 flex flex-col gap-3">
              <p className="text-sm text-[var(--color-ink)]">{item.text}</p>
              {item.claims.length > 0 && (
                <ul className="flex flex-col">
                  {item.claims.map((claim) => (
                    <ClaimRow key={claim.id} claim={claim} />
                  ))}
                </ul>
              )}
            </div>
          </details>
        )
      })}
    </div>
  )
}
