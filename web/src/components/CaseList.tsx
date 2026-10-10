import type { CaseSummaryVM, Severity } from './dashboard-types'

interface CaseListProps {
  cases: CaseSummaryVM[]
  selectedId: string | null
  onSelect: (id: string) => void
}

/** Maps a case severity to the Tailwind border-color class used for the left accent bar. */
function severityBorderClass(severity: Severity): string {
  switch (severity) {
    case 'red':
      return 'border-l-[var(--color-danger)]'
    case 'amber':
      return 'border-l-[var(--color-attention)]'
    case 'green':
      return 'border-l-[var(--color-success)]'
  }
}

/** Formats an ISO timestamp as a short, human-friendly label (e.g. "2h ago", "09:15"). */
function formatTimestamp(iso: string): string {
  const date = new Date(iso)
  if (Number.isNaN(date.getTime())) return iso

  const diffMs = Date.now() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)

  if (diffMins < 1) return 'now'
  if (diffMins < 60) return `${diffMins}m ago`

  const diffHours = Math.floor(diffMins / 60)
  if (diffHours < 24) return `${diffHours}h ago`

  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

/** Left column of the ops dashboard: a scrollable, selectable list of case summaries. */
export function CaseList({ cases, selectedId, onSelect }: CaseListProps) {
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between px-3 py-3">
        <span className="text-sm font-bold text-[var(--color-ink)]">Cases</span>
        <div className="flex items-center gap-1.5">
          <span className="h-1.5 w-1.5 rounded-full bg-[var(--color-success)]" />
          <span className="text-[11px] text-[var(--color-muted)]">Agent active</span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-2 pb-2">
        {cases.length === 0 ? (
          <p className="px-2 py-4 text-xs text-[var(--color-muted)]">No cases yet</p>
        ) : (
          <div className="flex flex-col gap-1.5">
            {cases.map((c) => {
              const isSelected = c.id === selectedId
              return (
                <button
                  key={c.id}
                  type="button"
                  onClick={() => onSelect(c.id)}
                  style={isSelected ? { background: 'rgba(33,88,72,.08)' } : undefined}
                  className={`flex min-h-[72px] w-full cursor-pointer flex-col justify-center gap-1 rounded-sm border-l-4 px-3 py-2 text-left transition-colors ${
                    isSelected
                      ? 'border-l-[var(--color-primary)]'
                      : `${severityBorderClass(c.severity)} bg-transparent hover:bg-[var(--color-canvas)]`
                  }`}
                >
                  <span className="truncate text-[13px] font-bold text-[var(--color-ink)]">
                    {c.address}
                  </span>
                  <span className="truncate text-xs text-[var(--color-muted)]">{c.issueType}</span>
                  <div className="flex items-center justify-between gap-2">
                    <span className="truncate rounded-full bg-[var(--color-canvas)] px-[7px] py-[2px] text-[10px] text-[var(--color-muted)]">
                      {c.stagePill}
                    </span>
                    <span className="shrink-0 text-[11px] text-[var(--color-muted)]">
                      {formatTimestamp(c.timestamp)}
                    </span>
                  </div>
                </button>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

export default CaseList
