export type Severity = 'red' | 'amber' | 'green'

export interface CaseSummaryVM {
  id: string
  address: string // e.g. "Flat 2, 42 Beacon Close, Bellmere"
  issueType: string // e.g. "Plumbing" or a short title
  stagePill: string // free text, e.g. "Verifying", "Scheduled", "Monitoring", "Blocked", "Done"
  severity: Severity
  timestamp: string // ISO datetime string — format it yourself for display
  progressPct: number // 0-100, how far through an 8-stage pipeline
  resolvedInHours?: number // only present for finished/done cases
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

export type ActionKey = 'approve' | 'reject' | 'more_evidence' | 'defer'

export interface StageAction {
  key: ActionKey
  label: string // e.g. "Approve", "Reject", "Request more information", "Defer"
  primary?: boolean // true = filled blue button, false/undefined = outlined secondary
}

export interface ActivityItem {
  id: string
  label: string // already translated to human language by the caller, e.g. "Tenant message received" — just render it, don't interpret raw event kinds yourself
  time: string // short formatted time
}
