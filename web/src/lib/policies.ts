/** Backend policy contracts. Only published server records are described as active. */
export interface PolicyRule {
  id: string;
  conditions: { key: string; status: string }[];
  match: 'all' | 'any';
  actions: string[];
  response: string;
  owner: string;
  required: boolean;
  property_ref?: string | null;
  category?: string | null;
}

export interface PolicySettings {
  access_immediate_review: boolean;
  reminder_hours: number;
  escalation_hours: number;
  reminder_limit: number;
  review_limit: number;
  approval_hours: number;
  [key: string]: unknown;
}

export interface PolicyDraftInput {
  base_version: number;
  settings: PolicySettings;
  rules: PolicyRule[];
  reason: string;
}

export interface PolicyRecord extends PolicyDraftInput {
  id: string;
  version: number;
  status: string;
  author: string;
  effective_at?: string;
}

export interface PolicyCollection {
  active: PolicyRecord;
  drafts: PolicyRecord[];
}

export interface PolicySuggestion {
  status: 'ready' | 'clarification' | 'unsupported';
  summary: string;
  questions: string[];
  warnings: string[];
  draft: PolicyDraftInput | null;
}

export interface PolicyPreview {
  preview_id: string;
  draft_id: string;
  active_version: number;
  affected: {
    case_id: string;
    title: string;
    before: string;
    after: string;
    blockers: string[];
    changed: boolean;
  }[];
}

export const POLICY_LABELS: Record<string, string> = {
  identity: 'Person and property identity', route: 'Contact route', access: 'Access permission',
  keys: 'Key custody', authority: 'Authority', schedule: 'Appointment', evidence: 'Supporting evidence',
  classification: 'Work category', completion: 'Completion evidence', commitments: 'Outstanding commitments',
  total: 'Total cost', finance: 'Financial review', urgent: 'Urgent hazard', supported: 'Supported action',
  clarify: 'Ask for clarification', request_quote: 'Request a quote', confirm_appointment: 'Confirm a visit',
  supply_keys: 'Supply keys', instruct_work: 'Instruct work', close_item: 'Close a repair', archive: 'Archive',
  case_manager: 'Property manager', access_officer: 'Access officer', approver: 'Approver',
  reviewer: 'Reviewer', policy_editor: 'Policy editor',
  PASS: 'confirmed', FAIL: 'refused or failed', UNKNOWN: 'missing or unverified', CONFLICT: 'conflicting',
  CLARIFY: 'Ask for clarification', WAIT: 'Wait', 'HUMAN REVIEW': 'Human review', 'STOP ACTION': 'Stop the action',
  ACT: 'Ready for an action', 'NO FURTHER ACTION': 'No further action',
};
export const policyLabel = (value: string) => POLICY_LABELS[value] ?? value.replaceAll('_', ' ');

export function draftFromPublished(policy: PolicyRecord): PolicyDraftInput {
  return { base_version: policy.version, settings: structuredClone(policy.settings),
    rules: structuredClone(policy.rules), reason: '' };
}
