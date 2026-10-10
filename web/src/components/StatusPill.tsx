import type { CheckStatus, BlockerResponse } from './types'

export type PillStatus = CheckStatus | BlockerResponse | 'ACT'

interface StatusPillProps {
  status: PillStatus
  label?: string
}

type Tone = 'success' | 'attention' | 'danger' | 'information'

const TONE_BY_STATUS: Record<PillStatus, Tone> = {
  PASS: 'success',
  ACT: 'success',
  UNKNOWN: 'attention',
  CLARIFY: 'attention',
  FAIL: 'danger',
  'STOP ACTION': 'danger',
  CONFLICT: 'danger',
  WAIT: 'information',
  'HUMAN REVIEW': 'information',
}

const DEFAULT_LABEL_BY_STATUS: Record<PillStatus, string> = {
  PASS: 'Confirmed',
  ACT: 'Ready to proceed',
  UNKNOWN: 'Unknown',
  CLARIFY: 'Needs clarification',
  FAIL: 'Failed',
  'STOP ACTION': 'Stopped',
  CONFLICT: 'Conflict',
  WAIT: 'Waiting',
  'HUMAN REVIEW': 'Needs review',
}

const TONE_CLASSES: Record<Tone, { text: string; bg: string }> = {
  success: { text: 'text-[var(--color-success)]', bg: 'bg-[var(--color-success-bg)]' },
  attention: { text: 'text-[var(--color-attention)]', bg: 'bg-[var(--color-attention-bg)]' },
  danger: { text: 'text-[var(--color-danger)]', bg: 'bg-[var(--color-danger-bg)]' },
  information: { text: 'text-[var(--color-information)]', bg: 'bg-[var(--color-information-bg)]' },
}

/** Small rounded status indicator: a colored dot plus a human-readable label. */
export default function StatusPill({ status, label }: StatusPillProps) {
  const tone = TONE_BY_STATUS[status] ?? 'information'
  const classes = TONE_CLASSES[tone]
  const text = label ?? DEFAULT_LABEL_BY_STATUS[status] ?? status

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${classes.text} ${classes.bg}`}
    >
      <span className={`h-1.5 w-1.5 shrink-0 rounded-full ${classes.text.replace('text-', 'bg-')}`} />
      {text}
    </span>
  )
}
