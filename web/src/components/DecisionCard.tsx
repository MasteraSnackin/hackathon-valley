import type { Decision, Blocker } from './types'
import StatusPill from './StatusPill'
import { readableCheckKey } from './CheckList'

interface DecisionCardProps {
  decision: Decision
  caseTitle: string
  propertyRef: string
  onRespond?: (decision: 'approve' | 'reject' | 'defer' | 'more_evidence', reason: string) => void
}

type Severity = 'attention' | 'danger' | 'success'

const HEADER_CLASSES: Record<Severity, { bg: string; text: string }> = {
  attention: { bg: 'bg-[var(--color-attention-bg)]', text: 'text-[var(--color-attention)]' },
  danger: { bg: 'bg-[var(--color-danger-bg)]', text: 'text-[var(--color-danger)]' },
  success: { bg: 'bg-[var(--color-success-bg)]', text: 'text-[var(--color-success)]' },
}

function severityFor(decision: Decision): Severity {
  if (decision.outcome === 'ACT') return 'success'
  if (decision.outcome === 'STOP ACTION') return 'danger'
  return 'attention'
}

function headerQuestion(decision: Decision): string {
  if (decision.outcome === 'ACT') return 'Ready to proceed'
  const top = decision.blockers[0]
  if (top) return top.reason
  return 'A decision is needed before this can continue.'
}

/** Button bar tailored to the top blocker's response type. */
function ActionButtons({
  topBlocker,
  onRespond,
}: {
  topBlocker: Blocker
  onRespond?: DecisionCardProps['onRespond']
}) {
  const call = (decision: 'approve' | 'reject' | 'defer' | 'more_evidence', reason: string) => {
    onRespond?.(decision, reason)
  }

  const primaryBtn =
    'rounded-[var(--radius-sm)] bg-[var(--color-primary)] px-4 py-2 text-sm font-medium text-white hover:bg-[var(--color-primary-hover)] transition-colors'
  const secondaryBtn =
    'rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-2 text-sm font-medium text-[var(--color-ink)] hover:bg-[var(--color-canvas)] transition-colors'
  const dangerBtn =
    'rounded-[var(--radius-sm)] border border-[var(--color-danger)] bg-[var(--color-surface)] px-4 py-2 text-sm font-medium text-[var(--color-danger)] hover:bg-[var(--color-danger-bg)] transition-colors'

  if (topBlocker.response === 'HUMAN REVIEW') {
    return (
      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          className={primaryBtn}
          onClick={() => call('approve', 'Approved via demo dashboard')}
        >
          Approve
        </button>
        <button
          type="button"
          className={dangerBtn}
          onClick={() => call('reject', 'Rejected via demo dashboard')}
        >
          Reject
        </button>
        <button
          type="button"
          className={secondaryBtn}
          onClick={() => call('more_evidence', 'Requested more information via demo dashboard')}
        >
          Request more information
        </button>
        <button
          type="button"
          className={secondaryBtn}
          onClick={() => call('defer', 'Deferred via demo dashboard')}
        >
          Defer
        </button>
      </div>
    )
  }

  if (topBlocker.response === 'CLARIFY') {
    return (
      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          className={primaryBtn}
          onClick={() => call('more_evidence', 'Requested more information via demo dashboard')}
        >
          Request more information
        </button>
      </div>
    )
  }

  if (topBlocker.response === 'STOP ACTION') {
    return (
      <div className="flex flex-col gap-2">
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            className={dangerBtn}
            onClick={() => call('reject', 'Rejected via demo dashboard')}
          >
            Reject
          </button>
        </div>
        <p className="text-xs text-[var(--color-muted)]">
          Other actions are unavailable while this is flagged as stopped.
        </p>
      </div>
    )
  }

  // WAIT
  return (
    <div className="flex flex-col gap-2">
      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          className={secondaryBtn}
          onClick={() => call('defer', 'Deferred via demo dashboard')}
        >
          Defer
        </button>
      </div>
      <p className="text-xs text-[var(--color-muted)]">
        This is waiting on an external step and does not need a decision yet.
      </p>
    </div>
  )
}

/** The centerpiece card: a decision summary, the blockers behind it, and action buttons. */
export default function DecisionCard({
  decision,
  caseTitle,
  propertyRef,
  onRespond,
}: DecisionCardProps) {
  const severity = severityFor(decision)
  const headerClasses = HEADER_CLASSES[severity]
  const topBlocker = decision.blockers[0]

  return (
    <div className="overflow-hidden rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-surface)]">
      <div className={`flex flex-col gap-1 px-5 py-4 ${headerClasses.bg}`}>
        <p className={`text-base font-semibold ${headerClasses.text}`}>{headerQuestion(decision)}</p>
        <p className="text-sm text-[var(--color-muted)]">
          {caseTitle} · {propertyRef}
        </p>
      </div>

      <div className="px-5 py-4">
        {decision.blockers.length > 0 ? (
          <ul className="flex flex-col divide-y divide-[var(--color-border)]">
            {decision.blockers.map((blocker) => (
              <li key={blocker.key} className="flex flex-col gap-1 py-3 first:pt-0 last:pb-0">
                <div className="flex items-center justify-between gap-3">
                  <span className="text-sm font-medium text-[var(--color-ink)]">
                    {readableCheckKey(blocker.key)}
                  </span>
                  <div className="flex items-center gap-2">
                    <span className="rounded-full bg-[var(--color-canvas)] px-2 py-0.5 text-xs text-[var(--color-muted)]">
                      {blocker.owner}
                    </span>
                    <StatusPill status={blocker.response} />
                  </div>
                </div>
                <p className="text-sm text-[var(--color-muted)]">{blocker.reason}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-[var(--color-muted)]">No outstanding blockers.</p>
        )}
      </div>

      <div className="border-t border-[var(--color-border)] px-5 py-4">
        {decision.outcome === 'ACT' || !topBlocker ? (
          <p className="text-sm font-medium text-[var(--color-success)]">
            Ready to proceed automatically — no decision needed.
          </p>
        ) : (
          <ActionButtons topBlocker={topBlocker} onRespond={onRespond} />
        )}
      </div>
    </div>
  )
}
