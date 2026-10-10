/** Display the current proposed action and its recorded checks, not a guessed repair lifecycle. */
import type { Blocker, CaseDetail, CaseListItem, TimelineEvent } from './types';
import type { ActivityItem, ActivityTone, CaseSummaryVM, PipelineNode, Severity, StageDetailRow } from '../components/dashboard-types';

export function formatTime(iso?: string | null): string | undefined {
  if (!iso) return undefined;
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return undefined;
  return date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
}

export function severityOf(item: CaseListItem): Severity {
  return item.outcome === 'STOP ACTION' ? 'red' : ['ACT', 'NO FURTHER ACTION'].includes(item.outcome) ? 'green' : 'amber';
}

export function stagePillOf(item: CaseListItem): string {
  const labels: Record<string, string> = {
    'STOP ACTION': 'Action stopped', 'HUMAN REVIEW': 'Needs review', CLARIFY: 'Needs information',
    WAIT: 'Waiting', ACT: 'Ready to act', 'NO FURTHER ACTION': 'Action complete',
  };
  return labels[item.outcome] ?? 'Awaiting assessment';
}

export function toCaseSummaryVM(item: CaseListItem): CaseSummaryVM {
  return {
    id: item.id, outcome: item.outcome, address: item.property_ref,
    issueType: item.category.replace(/_/g, ' '), stagePill: stagePillOf(item), severity: severityOf(item),
    timestamp: item.last_assessed_at ?? item.created_at,
    // Retained for component compatibility; this is not a repair completion percentage.
    progressPct: item.outcome === 'NO FURTHER ACTION' ? 100 : 0,
  };
}

export function computeDetailedPipeline(detail: CaseDetail): PipelineNode[] {
  const decision = detail.decision;
  const checksSatisfied = Boolean(decision && !decision.blockers.length && ['ACT', 'NO FURTHER ACTION'].includes(decision.outcome));
  const receipt = decision?.completed_action_id && detail.actions.find((action) => action.id === decision.completed_action_id && action.status === 'succeeded' && action.simulated);
  return [
    { key: 'recorded', label: 'Request recorded', state: 'completed', time: formatTime(detail.case.created_at) },
    { key: 'assessed', label: 'Action assessed', state: decision ? 'completed' : 'current', time: formatTime(decision?.assessed_at) },
    { key: 'checks', label: 'Required checks', state: checksSatisfied ? 'completed' : decision ? 'current' : 'future', actor: decision?.owner },
    { key: 'result', label: 'Simulated result', state: receipt ? 'completed' : checksSatisfied ? 'current' : 'future', time: receipt ? formatTime(receipt.created_at) : undefined },
  ];
}

export function findReviewForBlocker(detail: CaseDetail, blocker: Blocker) {
  return detail.reviews.find((review) => review.key === blocker.key && review.rule_id === blocker.rule_id
    && ['open', 'deferred'].includes(review.status) && review.action_revision === detail.case.action_revision
    && review.policy_version === detail.decision?.policy_version);
}

const FACT_LABELS: Record<string, string> = {
  identity: 'Identity and property', route: 'Reply route', access: 'Access permission', keys: 'Key custody',
  authority: 'Work authority', finance: 'Spending approval', schedule: 'Appointment details', evidence: 'Supporting evidence',
  classification: 'Request category', completion: 'Completion evidence', commitments: 'Outstanding commitments',
  total: 'Full job cost', urgent: 'Urgent hazard check', supported: 'Supported action', triage: 'Message interpretation',
};
export function readableFactKey(key: string): string { return FACT_LABELS[key] ?? key; }
export function readableRole(role: string): string { return role.replace(/_/g, ' '); }

export function computeStageRows(detail: CaseDetail): StageDetailRow[] {
  const { case: item, decision } = detail;
  return [
    { label: 'Proposed action', value: item.proposal.action.replace(/_/g, ' ') },
    { label: 'Work item', value: item.proposal.work_item || 'Not specified' },
    { label: 'Provider', value: item.proposal.provider || 'Not established' },
    { label: 'Access method', value: item.proposal.access_method || 'Not established' },
    { label: 'Next step', value: decision?.next_step ?? 'Awaiting assessment.' },
    { label: 'Policy version', value: decision ? String(decision.policy_version) : 'Not assessed' },
  ];
}

const ACTIVITY_LABELS: Record<string, string> = {
  action: 'Action recorded', action_rejected: 'Proposed action rejected', approval: 'Scoped approval recorded',
  build_snapshot: 'BUILD prefix imported', claim: 'Source assertion recorded', cycle_checkpoint: 'Workflow checkpoint',
  decision: 'Action assessed', evidence: 'Evidence added', human_evidence_request: 'Information request recorded (simulated)',
  incoming_event: 'Incoming event recorded', intake_receipt: 'Request logged', interpretation: 'Message interpreted',
  policy: 'Policy recorded', policy_draft: 'Policy draft created', policy_preview: 'Policy preview generated',
  policy_reassessment: 'Case reassessed under new policy', question: 'Clarification question recorded (simulated)',
  question_closed: 'Question closed', question_escalated: 'Question escalated',
  rejected_review_response: 'Review response rejected', reminder: 'Reminder recorded (simulated)',
  review: 'Review requested', review_overdue: 'Review overdue', review_response: 'Review response recorded',
  review_superseded: 'Review superseded', signal_outbox: 'Workflow notified',
  simulated_clarification: 'Clarification recorded (simulated)', simulated_provider_receipt: 'Simulated action receipt recorded',
  evidence_received: 'Evidence received', explicit_reassessment: 'Case reassessed', intake: 'Case opened',
  policy_published: 'Policy published', proposal_changed: 'Proposed action changed', review_responded: 'Staff responded to review',
  simulated_action: 'Action attempted (simulated)', simulated_result_reconciled: 'Uncertain result reconciled',
  routing: 'Message routed', issue_split: 'Issue split into its own case', route_changed: 'Action route changed',
  triage_retry: 'Message reading retried', question_followup: 'Follow-up question needed',
  triage_confirmed: 'Message interpretation confirmed', tenant_message: 'Message draft recorded',
  tenant_message_drafted: 'Message draft recorded', tenant_message_sent: 'Message delivery recorded (simulated)',
  tenant_message_rejected: 'Message draft rejected',
  workflow_recovery: 'Workflow recovery recorded', workflow_receipt: 'Workflow step recorded', workflow_error: 'Workflow error recorded',
};
function activityTone(kind: string): ActivityTone {
  if (/(reject|overdue|error|escalat)/.test(kind)) return 'r';
  if (/(decision|approv|complet|reconcil|published|resolved)/.test(kind)) return 'g';
  if (/(review|question|human|reminder|clarif|proposal)/.test(kind)) return 'a';
  return 'b';
}
export function translateActivity(timeline: TimelineEvent[]): ActivityItem[] {
  return timeline.slice(-8).reverse().map((event) => ({
    id: event.id, label: ACTIVITY_LABELS[event.kind] ?? event.kind.replace(/_/g, ' '),
    time: formatTime(event.created_at) ?? '', tone: activityTone(event.kind),
  }));
}
