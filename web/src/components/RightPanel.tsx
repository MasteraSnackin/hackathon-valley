import type { CaseSummaryVM } from './dashboard-types'

interface RightPanelProps {
  stats: { active: number; escalations: number; resolvedToday: number }
  inProgress: CaseSummaryVM[]
  finishedToday: CaseSummaryVM[]
}

/** Simple inline checkmark icon used next to finished cases. No icon library dependency. */
function CheckIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      width="14"
      height="14"
      stroke="currentColor"
      fill="none"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="shrink-0 text-[var(--color-success)]"
    >
      <path d="M20 6 9 17l-5-5" />
    </svg>
  )
}

/** A big headline stat: a coloured indicator dot, a 28px number, and a label. */
function BigStat({ value, label, dot }: { value: number; label: string; dot: string }) {
  return (
    <div className="flex flex-col gap-1">
      <div className="flex items-center gap-2">
        <span className="h-1.5 w-1.5 rounded-full" style={{ background: dot }} />
        <span className="text-[11px] text-[var(--color-muted)]">{label}</span>
      </div>
      <span
        className="text-[28px] font-bold leading-none text-[var(--color-ink)]"
        style={{ fontVariantNumeric: 'tabular-nums' }}
      >
        {value}
      </span>
    </div>
  )
}

/** Right column: headline stats, in-progress cases, and finished-today list. */
export function RightPanel({ stats, inProgress, finishedToday }: RightPanelProps) {
  return (
    <div className="flex h-full flex-col gap-5 overflow-y-auto px-4 py-4">
      {/* Headline stats */}
      <div className="flex flex-col gap-4">
        <BigStat value={stats.active} label="Active" dot="#215848" />
        <BigStat value={stats.escalations} label="Escalations" dot="#A33B36" />
        <div className="flex items-center gap-2">
          <span className="h-1.5 w-1.5 rounded-full" style={{ background: '#215848' }} />
          <span className="text-[13px] font-medium text-[var(--color-primary)]">
            {stats.resolvedToday} Resolved today
          </span>
        </div>
      </div>

      {/* Going On */}
      <div className="flex flex-col gap-2">
        <span className="text-[11px] tracking-wide text-[var(--color-muted)] uppercase">
          Going On
        </span>
        {inProgress.length === 0 ? (
          <p className="text-xs text-[var(--color-muted)]">Nothing in progress</p>
        ) : (
          <div className="flex flex-col gap-2.5">
            {inProgress.slice(0, 6).map((c) => (
              <div key={c.id} className="flex min-h-[44px] flex-col justify-center gap-1">
                <span className="truncate text-xs text-[var(--color-ink)]">{c.address}</span>
                <div className="h-[4px] w-full overflow-hidden rounded-full bg-[var(--color-success-bg)]">
                  <div
                    className="h-full rounded-full bg-[var(--color-primary)]"
                    style={{ width: `${Math.min(100, Math.max(0, c.progressPct))}%` }}
                  />
                </div>
                <span className="truncate text-[11px] text-[var(--color-muted)]">
                  {c.stagePill}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Finished Today */}
      <div className="flex flex-col gap-2">
        <span className="text-[11px] tracking-wide text-[var(--color-muted)] uppercase">
          Finished
        </span>
        {finishedToday.length === 0 ? (
          <p className="text-xs text-[var(--color-muted)]">Nothing finished yet</p>
        ) : (
          <div className="flex flex-col gap-2">
            {finishedToday.slice(0, 5).map((c) => (
              <div key={c.id} className="flex items-center gap-2 opacity-80">
                <CheckIcon />
                <div className="flex min-w-0 flex-col">
                  <span className="truncate text-xs text-[var(--color-ink)]">{c.address}</span>
                  <span className="text-[11px] text-[var(--color-success)]">
                    Resolved in {c.resolvedInHours ?? 0}h
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default RightPanel
