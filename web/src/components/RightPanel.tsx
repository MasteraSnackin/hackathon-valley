import type { CaseSummaryVM } from './dashboard-types'

interface RightPanelProps {
  stats: { active: number; escalations: number; resolvedToday: number }
  inProgress: CaseSummaryVM[]
  finishedToday: CaseSummaryVM[]
  onSelect?: (id: string) => void
}

export function RightPanel({ stats, inProgress, finishedToday, onSelect }: RightPanelProps) {
  function requestList(items: CaseSummaryVM[], empty: string) {
    return items.length ? (
      <ul className="divide-y divide-[var(--color-border)]">
        {items.slice(0, 5).map((item) => (
          <li key={item.id}>
            <button type="button" disabled={!onSelect} onClick={() => onSelect?.(item.id)} className="w-full rounded-sm py-3 text-left hover:bg-[var(--color-canvas)]">
              <span className="line-clamp-2 block break-words text-xs font-medium">{item.address}</span>
              <span className="mt-1 block text-xs text-[var(--color-muted)]">{item.stagePill}</span>
            </button>
          </li>
        ))}
      </ul>
    ) : <p className="text-xs text-[var(--color-muted)]">{empty}</p>
  }

  return (
    <aside aria-label="Queue overview" className="flex h-full flex-col gap-6 overflow-y-auto px-4 py-5">
      <h2 className="text-sm font-semibold">Queue overview</h2>
      <dl className="grid gap-4">
        <div><dt className="text-xs text-[var(--color-muted)]">Open actions</dt><dd className="text-3xl font-semibold tabular-nums">{stats.active}</dd></div>
        <div><dt className="text-xs text-[var(--color-muted)]">Actions stopped</dt><dd className="text-3xl font-semibold tabular-nums text-[var(--color-danger)]">{stats.escalations}</dd></div>
        <div><dt className="text-xs text-[var(--color-muted)]">No further action</dt><dd className="text-3xl font-semibold tabular-nums text-[var(--color-primary)]">{stats.resolvedToday}</dd></div>
      </dl>
      <p className="rounded-[var(--radius-sm)] bg-[var(--color-canvas)] p-3 text-xs leading-relaxed text-[var(--color-muted)]">Counts describe the current proposed actions. They do not confirm completed repairs.</p>
      <section className="flex flex-col gap-2"><h3 className="text-xs font-semibold">Other open requests</h3>{requestList(inProgress, 'No other open requests.')}</section>
      <section className="flex flex-col gap-2"><h3 className="text-xs font-semibold">No further action needed</h3>{requestList(finishedToday, 'No completed actions recorded.')}</section>
    </aside>
  )
}

export default RightPanel
