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
    <div className="flex w-[56px] shrink-0 flex-col items-center gap-1.5">
      <div
        className={`flex h-5 w-5 items-center justify-center rounded-full ${DOT_CLASSES[node.state]} ${
          node.state === 'current' ? 'pulse-ring' : ''
        }`}
        style={node.state === 'current' ? { animation: 'dot-pulse 1.9s ease-out infinite' } : undefined}
      >
        {node.state === 'completed' && <CheckIcon />}
      </div>
      <span className={`max-w-[56px] text-center text-[9px] leading-tight ${LABEL_CLASSES[node.state]}`}>
        {node.label}
      </span>
      <span className="h-[11px] text-center text-[9px] leading-tight text-[var(--color-muted)]">
        {caption}
      </span>
    </div>
  )
}

/** Horizontal pipeline track: circular stage dots joined by thin connector lines. */
export default function Pipeline({ nodes }: PipelineProps) {
  return (
    <div className="flex items-start">
      {nodes.map((node, index) => (
        <div key={node.key} className="flex items-start">
          <Node node={node} />
          {index < nodes.length - 1 && (
            <div
              className="mt-2.5 h-px w-5 shrink-0 self-start bg-[var(--color-border)]"
              aria-hidden="true"
            />
          )}
        </div>
      ))}
    </div>
  )
}
