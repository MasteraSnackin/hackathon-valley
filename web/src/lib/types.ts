/**
 * TypeScript mirrors of the FastAPI backend response shapes.
 * Source of truth: app/domain.py (evaluate(), ReviewResponse), app/service.py
 * (Service.detail_tx, Service.reviews, Service.questions, Service.action_states),
 * app/build_data.py (list_build, import_case), app/store.py (unpack/payload).
 */

/** Who performed an action: a demo session actor. */
export interface Actor {
  id: string;
  role: string;
}

/** The current proposed action for a case (app/domain.py ProposalInput / intake defaults). */
export interface Proposal {
  action: string;
  category?: string | null;
  work_item: string;
  provider: string;
  access_method: string;
  scope: Record<string, unknown>;
}

/** Case projection row (app/service.py Service.intake / store.py cases table). */
export interface Case {
  id: string;
  title: string;
  property_ref: string;
  category: string;
  profile: string;
  revision: number;
  action_revision: number;
  proposal: Proposal;
  status: string;
  owner: string;
  next_step: string;
  policy_pending: boolean;
  created_at: string;
  interpretation?: unknown;
  triage?: { state?: string; confirmed?: boolean; [key: string]: unknown };
  stage?: string;
  rejected_action_revision?: number;
  last_assessed_at?: string;
  completion_state?: string;
  last_verified_action?: string;
}

/** A single fact assertion extracted from evidence (app/domain.py ClaimInput + service annotations). */
export interface Claim {
  id: string;
  created_at: string;
  key: string;
  value: boolean | number;
  scope: Record<string, unknown>;
  scope_origin?: string;
  scope_valid?: boolean;
  source_quote: string;
  source_id: string;
  verified: boolean;
  verification?: string;
  verified_by?: Actor;
  expires_at?: string | null;
  supersedes: string[];
  superseded_by?: string;
}

/** A source document attached to a case (app/service.py 'evidence' records). */
export interface Evidence {
  id: string;
  created_at: string;
  text: string;
  source_label: string;
  actor: Actor;
  occurred_at: string;
  input_hash?: string;
}

/** One requirement row evaluated against current claims (app/domain.py evaluate()). */
export interface Check {
  key: string;
  status: 'PASS' | 'FAIL' | 'UNKNOWN' | 'CONFLICT';
  reason: string;
  source_ids: string[];
  claim_ids: string[];
}

/** A Check that is not satisfied, with an owner and required response (app/domain.py evaluate()). */
export interface Blocker extends Check {
  response: 'CLARIFY' | 'WAIT' | 'HUMAN REVIEW' | 'STOP ACTION';
  owner: string;
  rule_id: string;
}

/** Full policy evaluation result for a case (app/domain.py evaluate() + service.assess()). */
export interface Decision {
  id: string;
  created_at: string;
  outcome: 'ACT' | 'CLARIFY' | 'WAIT' | 'HUMAN REVIEW' | 'STOP ACTION' | 'NO FURTHER ACTION';
  checks: Check[];
  blockers: Blocker[];
  owner: string;
  next_step: string;
  policy_version: number;
  case_revision: number;
  action_revision: number;
  scope: Record<string, unknown>;
  assessed_at: string;
  claim_snapshot?: string[];
  policy_id?: string;
  completed_action_id?: string;
}

/** A review responder's recorded answer (app/domain.py ReviewResponse, embedded in review.response). */
export interface ReviewResponseRecord {
  id: string;
  created_at: string;
  review_id: string;
  actor: Actor;
  decision: 'approve' | 'correct' | 'reject' | 'defer' | 'more_evidence';
  reason: string;
  source_id?: string | null;
  claim_id?: string | null;
  key?: string | null;
  value?: boolean | number | null;
  expires_at?: string | null;
  deadline?: string | null;
  scope?: Record<string, unknown> | null;
}

/** A staff task raised against a blocker (app/service.py Service.create_review / reviews()). */
export interface Review {
  id: string;
  created_at: string;
  key: string;
  signature: string;
  question: string;
  owner: string;
  rule_id: string;
  policy_version: number;
  action_revision: number;
  scope: Record<string, unknown>;
  source_ids: string[];
  claim_ids: string[];
  other_blockers: string[];
  expires_at: string;
  next_step: string;
  status: 'open' | 'deferred' | 'resolved' | 'superseded' | 'expired';
  response: ReviewResponseRecord | null;
}

/** A simulated clarification question asked of an external party (app/service.py questions()). */
export interface Question {
  id: string;
  created_at: string;
  key: string;
  question: string;
  scope: Record<string, unknown>;
  action_revision: number;
  policy_version: number;
  opened_at: string;
  reminder_at: string;
  deadline: string;
  simulated: boolean;
  owner: string;
  status: 'open' | 'closed';
  reminders: number;
  escalated: boolean;
}

/** A simulated external action attempt against the current business action (app/service.py action_states()). */
export interface ActionState {
  id: string;
  created_at: string;
  business_id: string;
  status: 'intent' | 'succeeded' | 'uncertain';
  scope: Record<string, unknown>;
  decision_id: string;
  simulated: boolean;
  actor: Actor;
  receipt_id?: string | null;
  reconciled_by?: Actor;
}

/** A raw append-only audit record (app/store.py unpack()). Payload shape varies by `kind`. */
export interface TimelineEvent {
  id: string;
  kind: string;
  case_id: string | null;
  created_at: string;
  payload: Record<string, unknown>;
}

/** Full response of GET /api/cases/{id} (app/service.py Service.detail_tx). */
export interface CaseDetail {
  case: Case;
  claims: Claim[];
  evidence: Evidence[];
  decision: Decision | null;
  reviews: Review[];
  questions: Question[];
  actions: ActionState[];
  timeline: TimelineEvent[];
}

/** One row from GET /api/cases (app/service.py Service.list_cases()): a Case
 * plus a cheap-to-compute `outcome` (mirrors case.stage, or 'unassessed') and
 * `open_reviews` count — enough for list/summary views without a full detail
 * fetch per case. */
export interface CaseListItem extends Case {
  outcome: string;
  open_reviews: number;
}

/** One catalogue entry from GET /api/build-cases (app/build_data.py list_build()). */
export interface BuildCaseSummary {
  case_id: string;
  partition: string;
  title: string;
  whole_case_complexity: string;
  task_family: string;
  history_events: number;
  attachment_count: number;
  source_directory: string;
  source_url: string;
  preview: string;
  snapshot_event_count: number;
}

/** Request body for POST /api/reviews/{id}/respond (app/domain.py ReviewResponse). */
export interface ReviewResponseInput {
  decision: 'approve' | 'correct' | 'reject' | 'defer' | 'more_evidence';
  reason: string;
  source_id?: string;
  claim_id?: string;
  key?: string;
  value?: boolean | number;
  expires_at?: string;
  deadline?: string;
  scope?: Record<string, unknown>;
}
