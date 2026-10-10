import type { PipelineNode, NodeState } from './dashboard-types'

interface PipelineProps {
  nodes: PipelineNode[]
}

const DOT_CLASSES: Record<NodeState, string> = {
  completed: 'bg-[var(--color-primary)] border-2 border-[var(--color-primary)]',
  current: 'bg-[var(--color-surface)] border-2 border-[var(--color-primary)]',
  future: 'bg-[var(--color-border)] border-2 border-[var(--color-border)]',
}

const LABEL_CLASSES: Record<NodeState, string> = {
  completed: 'text-[var(--color-primary)]',
  current: 'font-semibold text-[var(--color-ink)]',
  future: 'text-[var(--color-muted)]',
}

/** Small inline checkmark shown inside completed dots. */
function CheckIcon() {
  return (
    <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="#fff" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  )
}

/** One circular stage dot plus its label and optional actor/time caption. */
function Node({ node }: { node: PipelineNode }) {
  const caption = node.actor && node.time ? `${node.actor} · ${node.time}` : null
  return (
    <div className="flex min-w-0 flex-1 flex-col items-center gap-2" aria-current={node.state === 'current' ? 'step' : undefined}>
      <div
        className={`flex h-6 w-6 items-center justify-center rounded-full ${DOT_CLASSES[node.state]}`}
        aria-hidden="true"
      >
        {node.state === 'completed' && <CheckIcon />}
      </div>
      <span className={`text-center text-xs leading-snug ${LABEL_CLASSES[node.state]}`}>
        {node.label}
        <span className="sr-only">: {node.state === 'completed' ? 'complete' : node.state === 'current' ? 'current step' : 'not reached'}</span>
      </span>
      {caption && <span className="break-words text-center text-xs text-[var(--color-muted)]">{caption}</span>}
    </div>
  )
}

/** Horizontal pipeline track: circular stage dots joined by thin connector lines. */
export default function Pipeline({ nodes }: PipelineProps) {
  return (
    <ol aria-label="Current action progress" className="flex w-full max-w-2xl items-start">
      {nodes.map((node, index) => (
        <li key={node.key} className="flex min-w-0 flex-1 items-start">
          <Node node={node} />
          {index < nodes.length - 1 && (
            <div
              className="mx-1 mt-3 h-px w-3 shrink-0 self-start bg-[var(--color-border)] sm:w-6"
              aria-hidden="true"
            />
          )}
        </li>
      ))}
    </ol>
  )
}
