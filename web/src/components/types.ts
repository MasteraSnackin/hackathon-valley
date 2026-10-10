/** Shared local TypeScript types for the request-detail / decision-card screen.
 * These are intentionally duplicated here (not imported from src/lib) so this
 * component set has no dependency on in-progress sibling work.
 */

export type CheckStatus = 'PASS' | 'FAIL' | 'UNKNOWN' | 'CONFLICT'
export type BlockerResponse = 'CLARIFY' | 'WAIT' | 'HUMAN REVIEW' | 'STOP ACTION'

export interface Check {
  key: string
  status: CheckStatus
  reason: string
  source_ids: string[]
  claim_ids: string[]
}

export interface Blocker extends Check {
  response: BlockerResponse
  owner: string
  rule_id: string
}

export interface Decision {
  outcome: BlockerResponse | 'ACT'
  checks: Check[]
  blockers: Blocker[]
  owner: string
  next_step: string
  assessed_at: string
}

export interface EvidenceClaim {
  id: string
  key: string
  value: boolean | number
  source_quote: string
  verified?: boolean
}

export interface EvidenceItem {
  id: string
  text: string
  source_label: string
  occurred_at?: string | null
  claims: EvidenceClaim[]
}

export interface TimelineEvent {
  id: string
  kind: string
  at: string
  summary?: string
  detail?: Record<string, unknown>
}
