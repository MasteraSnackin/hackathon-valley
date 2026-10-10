import type { StageDetailRow, StageAction, ActionKey, ActivityItem, ActivityTone } from './dashboard-types'

const TONE_COLOR: Record<ActivityTone, string> = {
  b: '#355C85',
  g: '#215848',
  a: '#865719',
  r: '#A33B36',
}

interface StageDetailCardProps {
  stageTitle: string
  rows: StageDetailRow[]
  actions?: StageAction[]
  onAction?: (key: ActionKey) => void
  disabledNote?: string
  activity: ActivityItem[]
}

const PRIMARY_BTN =
  'rounded-[var(--radius-sm)] bg-[var(--color-primary)] px-4 py-2 text-sm font-medium text-white hover:bg-[var(--color-primary-hover)] transition-colors'
const SECONDARY_BTN =
  'rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-transparent px-4 py-2 text-sm font-medium text-[var(--color-ink)] hover:bg-[var(--color-canvas)] transition-colors'

/** Compact card showing a single pipeline stage's details, actions, and recent activity. */
export default function StageDetailCard({
  stageTitle,
  rows,
  actions,
  onAction,
  disabledNote,
  activity,
}: StageDetailCardProps) {
  return (
    <div className="rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5">
      <h2 className="text-[15px] font-bold text-[var(--color-ink)]">{stageTitle}</h2>

      {rows.length > 0 && (
        <div className="mt-3 grid grid-cols-[120px_1fr] gap-x-3 gap-y-2 text-sm">
          {rows.map((row) => (
            <div key={row.label} className="contents">
              <span className="text-[var(--color-muted)]">{row.label}</span>
              <span className="text-[var(--color-ink)]">{row.value}</span>
            </div>
          ))}
        </div>
      )}

      {actions && actions.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-2">
          {actions.map((action) => (
            <button
              key={action.key}
              type="button"
              className={action.primary ? PRIMARY_BTN : SECONDARY_BTN}
              onClick={() => onAction?.(action.key)}
            >
              {action.label}
            </button>
          ))}
        </div>
      )}

      {disabledNote && (
        <p className="mt-2 text-[11px] italic text-[var(--color-muted)]">{disabledNote}</p>
      )}

      <div className="mt-4 border-t border-[var(--color-border)] pt-3">
        <p className="text-[11px] font-medium uppercase tracking-wide text-[var(--color-muted)]">
          Activity log
        </p>
        {activity.length > 0 ? (
          <ul className="mt-2 flex flex-col gap-1.5">
            {activity.map((item) => (
              <li
                key={item.id}
                className="flex items-baseline justify-between gap-3 text-xs text-[var(--color-muted)]"
              >
                <span className="flex min-w-0 items-baseline gap-2">
                  <span
                    className="mt-[1px] h-1.5 w-1.5 shrink-0 translate-y-[2px] rounded-full"
                    style={{ background: TONE_COLOR[item.tone] }}
                  />
                  <span className="truncate">{item.label}</span>
                </span>
                <span className="shrink-0">{item.time}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-2 text-xs text-[var(--color-muted)]">No recent activity</p>
        )}
      </div>
    </div>
  )
}
