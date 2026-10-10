import type { Check } from './types'
import StatusPill from './StatusPill'

interface CheckListProps {
  checks: Check[]
}

const READABLE_KEY: Record<string, string> = {
  identity: 'Identity & property',
  route: 'Route',
  access: 'Access permission',
  keys: 'Key handling',
  authority: 'Work authority',
  schedule: 'Appointment schedule',
  evidence: 'Supporting evidence',
  classification: 'Classification',
  completion: 'Completion evidence',
  commitments: 'Outstanding commitments',
  total: 'Full job cost',
  urgent: 'Urgency',
  supported: 'Supported',
}

/** Turns a check `key` into a readable label, falling back to a title-cased version. */
export function readableCheckKey(key: string): string {
  if (READABLE_KEY[key]) return READABLE_KEY[key]
  return key
    .split('_')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ')
}

/** Renders a list of checks as rows: status pill, readable name, and reason text. */
export default function CheckList({ checks }: CheckListProps) {
  if (checks.length === 0) {
    return <p className="text-sm text-[var(--color-muted)]">No checks recorded.</p>
  }

  return (
    <ul className="flex flex-col divide-y divide-[var(--color-border)]">
      {checks.map((check) => (
        <li key={check.key} className="flex flex-col gap-1 py-3 first:pt-0 last:pb-0">
          <div className="flex items-center justify-between gap-3">
            <span className="text-sm font-medium text-[var(--color-ink)]">
              {readableCheckKey(check.key)}
            </span>
            <StatusPill status={check.status} />
          </div>
          <p className="text-sm text-[var(--color-muted)]">{check.reason}</p>
        </li>
      ))}
    </ul>
  )
}
