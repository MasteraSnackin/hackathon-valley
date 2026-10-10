export type Severity = 'red' | 'amber' | 'green'

export interface CaseSummaryVM {
  id: string
  outcome?: string // Backend outcome for filtering; ACT is open, even when displayed in green.
  address: string // e.g. "Flat 2, 42 Beacon Close, Bellmere"
  issueType: string // e.g. "Plumbing" or a short title
  stagePill: string // free text, e.g. "Verifying", "Scheduled", "Monitoring", "Blocked", "Done"
  severity: Severity
  timestamp: string // ISO datetime string — format it yourself for display
  progressPct: number // Compatibility value only; never present as measured repair progress.
  resolvedInHours?: number // Optional measured duration only; not derived from current clock.
}

export type NodeState = 'completed' | 'current' | 'future'

export interface PipelineNode {
  key: string
  label: string // e.g. "Intake", "Diagnosed", "Landlord OK", "Assigned", "Contacted", "Replied", "Scheduled", "Done"
  state: NodeState
  actor?: string // e.g. "AI" or "James Patel" or a role name — who acted at this stage
  time?: string // short formatted time, e.g. "09:15"
}

export interface StageDetailRow {
  label: string // e.g. "Assigned to", "Action taken", "Awaiting", "Next auto-action"
  value: string
}

export type ActionKey = 'approve' | 'verify' | 'reject' | 'more_evidence' | 'defer'

export interface StageAction {
  key: ActionKey
  label: string // e.g. "Approve", "Reject", "Request more information", "Defer"
  primary?: boolean // true = filled blue button, false/undefined = outlined secondary
}

export type ActivityTone = 'b' | 'g' | 'a' | 'r' // blue / green / amber / red dot

export interface ActivityItem {
  id: string
  label: string // already translated to human language by the caller, e.g. "Tenant message received" — just render it, don't interpret raw event kinds yourself
  time: string // short formatted time
  tone: ActivityTone
}

/** A suggested review response; choosing and checking the source stays explicit. */
export interface PrimaryResolution {
  key: 'approve' | 'verify'
  label: string
  explanation: string
  claim?: import('../lib/types').Claim
}
