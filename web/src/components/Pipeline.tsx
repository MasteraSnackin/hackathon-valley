import type { PipelineNode, NodeState } from './dashboard-types'

interface PipelineProps {
  nodes: PipelineNode[]
}

const NODE_CLASSES: Record<NodeState, string> = {
  completed: 'bg-[var(--color-surface)] border border-[var(--color-success)] text-[var(--color-ink)]',
  current: 'bg-[var(--color-primary)] text-white shadow-[0_0_12px_rgba(47,129,247,0.4)]',
  future: 'bg-[var(--color-canvas)] border border-[var(--color-border)] text-[var(--color-muted)]',
}

/** Small inline checkmark used inside completed stage nodes. */
function CheckIcon() {
  return (
    <svg
      viewBox="0 0 16 16"
      width="10"
      height="10"
      className="shrink-0 fill-none stroke-[var(--color-success)] stroke-2"
    >
      <path d="M3 8.5L6.5 12L13 4.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

/** Thin connector between two adjacent nodes, ending in a small arrowhead. */
function Connector() {
  return (
    <div className="flex h-[48px] w-4 shrink-0 items-center" aria-hidden="true">
      <div className="h-px flex-1 bg-[var(--color-border)]" />
      <svg viewBox="0 0 8 8" width="6" height="6" className="shrink-0 fill-[var(--color-border)]">
        <polygon points="0,0 8,4 0,8" />
      </svg>
    </div>
  )
}

/** One stage node plus its optional actor/time caption. */
function Node({ node }: { node: PipelineNode }) {
  const caption = node.actor && node.time ? `${node.actor} · ${node.time}` : null

  return (
    <div className="flex flex-col items-center gap-1.5">
      <div
        className={`flex h-[48px] w-[90px] shrink-0 items-center justify-center gap-1 rounded-[8px] px-2 text-[11px] font-medium ${NODE_CLASSES[node.state]}`}
      >
        {node.state === 'completed' && <CheckIcon />}
        <span className="truncate">{node.label}</span>
      </div>
      <div className="h-[13px] text-center text-[10px] leading-tight text-[var(--color-muted)]">
        {caption}
      </div>
    </div>
  )
}

/** Horizontal pipeline of connected stage nodes showing progress through the case lifecycle. */
export default function Pipeline({ nodes }: PipelineProps) {
  return (
    <div className="flex flex-wrap items-start gap-y-3">
      {nodes.map((node, index) => (
        <div key={node.key} className="flex items-start">
          <Node node={node} />
          {index < nodes.length - 1 && <Connector />}
        </div>
      ))}
    </div>
  )
}
