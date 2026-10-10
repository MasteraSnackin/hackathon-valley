import type { TimelineEvent } from './types'

interface ActivityTimelineProps {
  events: TimelineEvent[]
}

/** Maps a raw `kind` string to a plain-language verb for the main timeline. */
function friendlyKind(kind: string): string {
  const lower = kind.toLowerCase()
  if (lower.includes('evidence')) return 'Evidence added'
  if (lower.includes('review')) return 'Review requested or responded'
  if (lower.includes('action') || lower.includes('execute')) return 'Action attempted'
  return kind
}

function isTechnical(kind: string): boolean {
  const lower = kind.toLowerCase()
  return lower.includes('workflow') || lower.includes('checkpoint')
}

function formatTime(at: string): string {
  const date = new Date(at)
  if (Number.isNaN(date.getTime())) return at
  return date.toLocaleString(undefined, {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

/**
 * Vertical activity timeline in plain language. Raw workflow/checkpoint
 * records are kept out of the main list and tucked into a collapsed
 * "Show technical log" section instead.
 */
export default function ActivityTimeline({ events }: ActivityTimelineProps) {
  const mainEvents = events.filter((event) => !isTechnical(event.kind))
  const technicalEvents = events.filter((event) => isTechnical(event.kind))

  return (
    <div className="flex flex-col gap-4">
      {mainEvents.length === 0 ? (
        <p className="text-sm text-[var(--color-muted)]">No activity recorded yet.</p>
      ) : (
        <ul className="flex flex-col">
          {mainEvents.map((event, index) => (
            <li key={event.id} className="relative flex gap-3 pb-4 last:pb-0">
              <div className="flex flex-col items-center">
                <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-[var(--color-primary)]" />
                {index < mainEvents.length - 1 && (
                  <span className="mt-1 w-px flex-1 bg-[var(--color-border)]" />
                )}
              </div>
              <div className="flex flex-col gap-0.5 pb-1">
                <div className="flex items-baseline gap-2">
                  <span className="text-sm font-medium text-[var(--color-ink)]">
                    {friendlyKind(event.kind)}
                  </span>
                  <span className="text-xs text-[var(--color-muted)]">{formatTime(event.at)}</span>
                </div>
                {event.summary && (
                  <p className="text-sm text-[var(--color-muted)]">{event.summary}</p>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}

      {technicalEvents.length > 0 && (
        <details className="rounded-[var(--radius-md)] border border-[var(--color-border)] px-4 py-3">
          <summary className="cursor-pointer text-sm font-medium text-[var(--color-muted)]">
            Show technical log
          </summary>
          <ul className="mt-3 flex flex-col gap-2">
            {technicalEvents.map((event) => (
              <li key={event.id} className="text-xs text-[var(--color-muted)]">
                <span className="font-mono">{event.kind}</span> — {formatTime(event.at)}
                {event.summary ? ` · ${event.summary}` : ''}
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  )
}
