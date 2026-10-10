/**
 * Presentation-layer heuristics that turn real backend state (app/domain.py's
 * evaluate() outcome, per-fact checks, claims, evidence, timeline) into the
 * 8-stage visual pipeline for the ops-dashboard redesign. The backend has no
 * concept of "Intake/Diagnosed/.../Done" — that vocabulary is invented here
 * purely for display, derived from real fields (never fabricated), and kept
 * in one place so both the coarse (list/summary) and detailed (selected-case)
 * views stay consistent.
 */
import type { CaseDetail, CaseListItem, Claim, TimelineEvent } from './types';
import type {
  ActivityItem,
  CaseSummaryVM,
  PipelineNode,
  Severity,
  StageAction,
  StageDetailRow,
} from '../components/dashboard-types';

export const PIPELINE_STAGES = [
  { key: 'intake', label: 'Intake', facts: [] as string[] },
  // Identity/route/classification are all part of the agent "diagnosing" and
  // verifying who/what/where before anything downstream — grouping them here
  // means a case blocked on identity correctly shows "Diagnosed" as current,
  // rather than skipping ahead to an unrelated node.
  { key: 'diagnosed', label: 'Diagnosed', facts: ['identity', 'route', 'classification'] },
  { key: 'landlord_ok', label: 'Landlord OK', facts: ['authority'] },
  { key: 'assigned', label: 'Assigned', facts: ['access'] },
  { key: 'contacted', label: 'Contacted', facts: [] },
  { key: 'replied', label: 'Replied', facts: [] },
  { key: 'scheduled', label: 'Scheduled', facts: ['schedule'] },
  { key: 'done', label: 'Done', facts: ['completion'] },
] as const;

const LAST_STAGE_INDEX = PIPELINE_STAGES.length - 1;

/** Coarse "how far along is this action, roughly" baseline — used only for
 * the cheap list/summary views where we don't want to fetch full detail for
 * every case just to draw a progress bar. */
const ACTION_BASELINE_INDEX: Record<string, number> = {
  clarify: 0,
  request_quote: 1,
  confirm_appointment: 6,
  supply_keys: 3,
  instruct_work: 4,
  close_item: 7,
  archive: 7,
};

export function formatTime(iso?: string | null): string | undefined {
  if (!iso) return undefined;
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return undefined;
  return date.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
}

function relativeOrClock(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  const diffMs = Date.now() - date.getTime();
  const diffMin = Math.round(diffMs / 60000);
  if (diffMin < 1) return 'just now';
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffHr = Math.round(diffMin / 60);
  if (diffHr < 24) return `${diffHr}h ago`;
  return date.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
}

/** Coarse severity bucket for the three-colour left-border / stat-strip
 * scheme — collapses the backend's richer outcome vocabulary down to
 * red/amber/green. */
export function severityOf(item: CaseListItem): Severity {
  switch (item.outcome) {
    case 'STOP ACTION':
      return 'red';
    case 'ACT':
    case 'NO FURTHER ACTION':
      return 'green';
    default:
      return 'amber';
  }
}

export function stagePillOf(item: CaseListItem): string {
  switch (item.outcome) {
    case 'STOP ACTION':
      return 'Blocked';
    case 'HUMAN REVIEW':
      return 'Verifying';
    case 'CLARIFY':
      return 'Verifying';
    case 'WAIT':
      return 'Monitoring';
    case 'ACT':
      return 'On track';
    case 'NO FURTHER ACTION':
      return 'Done';
    default:
      return 'New';
  }
}

function approxStageIndex(item: CaseListItem): number {
  const baseline = ACTION_BASELINE_INDEX[item.proposal.action] ?? 0;
  if (item.outcome === 'NO FURTHER ACTION') return LAST_STAGE_INDEX;
  return baseline;
}

/** Shape a cheap case-list row into the dashboard's summary view model
 * (left column cards, right column mini rows/progress bars). */
export function toCaseSummaryVM(item: CaseListItem): CaseSummaryVM {
  const index = approxStageIndex(item);
  const timestamp = item.last_assessed_at ?? item.created_at;
  const vm: CaseSummaryVM = {
    id: item.id,
    address: item.property_ref,
    issueType: item.category
      .split('_')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' '),
    stagePill: stagePillOf(item),
    severity: severityOf(item),
    timestamp: relativeOrClock(timestamp),
    progressPct: Math.round((index / LAST_STAGE_INDEX) * 100),
  };
  if (item.outcome === 'NO FURTHER ACTION') {
    const hours = Math.max(
      1,
      Math.round(
        (new Date(timestamp).getTime() - new Date(item.created_at).getTime()) / 3600000,
      ),
    );
    vm.resolvedInHours = hours;
  }
  return vm;
}

/** Precise, per-fact pipeline for the currently-selected case's centre
 * column, using its full fetched detail (checks/claims/evidence/timeline)
 * rather than the coarse action-based guess above. A fact not required by
 * the case's current action is treated as trivially satisfied, so the
 * pipeline doesn't stall on a requirement that doesn't apply here. */
export function computeDetailedPipeline(detail: CaseDetail): PipelineNode[] {
  const { decision, evidence, timeline } = detail;
  const checksByKey = new Map((decision?.checks ?? []).map((c) => [c.key, c]));
  const latestVerifiedByKey = new Map<string, Claim>();
  for (const claim of detail.claims) {
    if (!claim.verified) continue;
    const existing = latestVerifiedByKey.get(claim.key);
    if (!existing || claim.created_at > existing.created_at) {
      latestVerifiedByKey.set(claim.key, claim);
    }
  }
  const contactedEvent = timeline.find((e) => e.kind === 'signal_outbox');
  const isDone = decision?.outcome === 'NO FURTHER ACTION';

  function completedFor(key: (typeof PIPELINE_STAGES)[number]['key']): boolean {
    if (isDone) return true;
    switch (key) {
      case 'intake':
        return evidence.length > 0;
      case 'contacted':
        return Boolean(contactedEvent);
      case 'replied':
        return Boolean(contactedEvent) && evidence.length > 2;
      case 'done':
        return checksByKey.get('completion')?.status === 'PASS';
      default: {
        const stage = PIPELINE_STAGES.find((s) => s.key === key);
        const facts = stage?.facts ?? [];
        if (facts.length === 0) return false;
        // A fact not required by this action's checks is trivially satisfied;
        // the stage is complete only when every one of its required facts is.
        return facts.every((fact) => {
          const check = checksByKey.get(fact);
          return !check || check.status === 'PASS';
        });
      }
    }
  }

  const completedFlags = PIPELINE_STAGES.map((s) => completedFor(s.key));
  const firstIncomplete = completedFlags.findIndex((done) => !done);
  const currentIndex = isDone ? LAST_STAGE_INDEX : firstIncomplete === -1 ? LAST_STAGE_INDEX : firstIncomplete;

  return PIPELINE_STAGES.map((stage, index) => {
    const state: PipelineNode['state'] = isDone
      ? 'completed'
      : index < currentIndex
        ? 'completed'
        : index === currentIndex
          ? 'current'
          : 'future';

    let actor: string | undefined;
    let time: string | undefined;
    if (stage.key === 'intake') {
      actor = evidence[0]?.actor?.role;
      time = formatTime(evidence[0]?.occurred_at);
    } else if (stage.key === 'contacted') {
      actor = 'System';
      time = formatTime(contactedEvent?.created_at);
    } else if (stage.key === 'replied') {
      const last = evidence[evidence.length - 1];
      actor = last?.actor?.role;
      time = formatTime(last?.occurred_at);
    } else if (stage.key === 'done') {
      actor = decision?.owner;
      time = formatTime(decision?.assessed_at);
    } else if (stage.facts.length > 0) {
      // Attribute the stage to the most recently verified of its facts.
      const claim = stage.facts
        .map((f) => latestVerifiedByKey.get(f))
        .filter((c): c is Claim => Boolean(c))
        .sort((a, b) => b.created_at.localeCompare(a.created_at))[0];
      actor = claim?.verified_by?.role ?? (state === 'current' ? decision?.owner : undefined);
      time = formatTime(claim?.created_at ?? (state === 'current' ? decision?.assessed_at : undefined));
    }

    return { key: stage.key, label: stage.label, state, actor, time };
  });
}

const FACT_LABELS: Record<string, string> = {
  identity: 'Identity & property',
  route: 'Route',
  access: 'Access permission',
  keys: 'Key custody',
  authority: 'Work authority',
  schedule: 'Appointment schedule',
  evidence: 'Supporting evidence',
  classification: 'Category match',
  completion: 'Completion evidence',
  commitments: 'Outstanding commitments',
  total: 'Full job cost',
  urgent: 'Urgent hazard check',
  supported: 'Supported action',
};

export function readableFactKey(key: string): string {
  return FACT_LABELS[key] ?? key;
}

/** Key-value rows for the centre-column stage detail card. */
export function computeStageRows(detail: CaseDetail): StageDetailRow[] {
  const { case: theCase, decision } = detail;
  const topBlocker = decision?.blockers[0];
  const assignedTo = topBlocker ? topBlocker.owner : theCase.owner;
  const actionTaken = decision?.next_step ?? 'No assessment recorded yet.';
  const awaiting = topBlocker
    ? `${readableFactKey(topBlocker.key)} — ${topBlocker.owner}`
    : 'Nothing — ready to proceed';
  let nextAuto = 'None';
  if (!topBlocker && decision?.outcome === 'ACT') {
    nextAuto = `Execute ${theCase.proposal.action.replace(/_/g, ' ')}`;
  } else if (topBlocker) {
    switch (topBlocker.response) {
      case 'CLARIFY':
        nextAuto = 'Waiting for a reply to the clarification question';
        break;
      case 'WAIT':
        nextAuto = 'Waiting on an external step';
        break;
      case 'HUMAN REVIEW':
        nextAuto = 'Waiting for staff review';
        break;
      case 'STOP ACTION':
        nextAuto = 'Stopped — no automatic next step';
        break;
    }
  }
  return [
    { label: 'Assigned to', value: assignedTo },
    { label: 'Action taken', value: actionTaken },
    { label: 'Awaiting', value: awaiting },
    { label: 'Next auto-action', value: nextAuto },
  ];
}

/** Which decision buttons are actually valid for the current top blocker,
 * mirroring app/service.py's respond() constraints (e.g. a generic "approve"
 * only applies to authority/finance reviews) so we never show a button that
 * is guaranteed to fail. */
export function computeActions(detail: CaseDetail): {
  actions: StageAction[];
  disabledNote?: string;
} {
  const topBlocker = detail.decision?.blockers[0];
  if (!topBlocker) return { actions: [] };

  if (topBlocker.response === 'HUMAN REVIEW') {
    const canApprove = topBlocker.key === 'authority' || topBlocker.key === 'finance';
    const actions: StageAction[] = [];
    if (canApprove) actions.push({ key: 'approve', label: 'Approve', primary: true });
    actions.push({ key: 'reject', label: 'Reject' });
    actions.push({ key: 'more_evidence', label: 'Request more information' });
    actions.push({ key: 'defer', label: 'Defer' });
    return {
      actions,
      disabledNote: canApprove
        ? undefined
        : "Approve isn't available here — this needs the underlying source corrected or verified, not a general approval.",
    };
  }
  if (topBlocker.response === 'CLARIFY') {
    return { actions: [{ key: 'more_evidence', label: 'Request more information', primary: true }] };
  }
  if (topBlocker.response === 'STOP ACTION') {
    return {
      actions: [{ key: 'reject', label: 'Reject' }],
      disabledNote: 'Other actions are unavailable while this is flagged as stopped.',
    };
  }
  // WAIT
  return {
    actions: [{ key: 'defer', label: 'Defer' }],
    disabledNote: 'This is waiting on an external step and does not need a decision yet.',
  };
}

const ACTIVITY_LABELS: Record<string, string> = {
  action: 'Action recorded',
  action_rejected: 'Action rejected',
  approval: 'Approval granted',
  build_snapshot: 'Case snapshot saved',
  claim: 'Fact recorded',
  cycle_checkpoint: 'Workflow checkpoint',
  decision: 'Agent decision made',
  evidence: 'Evidence added',
  human_evidence_request: 'More information requested',
  incoming_event: 'Tenant message received',
  intake_receipt: 'Request logged',
  interpretation: 'Agent interpreted report',
  policy: 'Policy applied',
  policy_draft: 'Policy draft created',
  policy_preview: 'Policy preview generated',
  policy_reassessment: 'Case reassessed under new policy',
  question: 'Question sent',
  question_closed: 'Question closed',
  question_escalated: 'Question escalated',
  rejected_review_response: 'Review response rejected (stale)',
  reminder: 'Reminder sent',
  review: 'Review requested',
  review_overdue: 'Review overdue',
  review_response: 'Review answered',
  review_superseded: 'Review superseded',
  signal_outbox: 'Email sent to landlord',
  simulated_clarification: 'Clarification sent (simulated)',
  simulated_provider_receipt: 'Provider receipt received (simulated)',
  evidence_received: 'Evidence received',
  explicit_reassessment: 'Case reassessed',
  intake: 'Case opened',
  policy_published: 'Policy published',
  proposal_changed: 'Action proposal changed',
  review_responded: 'Staff responded to review',
  simulated_action: 'Action attempted (simulated)',
  simulated_result_reconciled: 'Uncertain result reconciled',
  workflow_recovery: 'Workflow step recorded',
  workflow_receipt: 'Workflow step recorded',
  workflow_error: 'Workflow step recorded',
};

function titleCaseKind(kind: string): string {
  return kind
    .split('_')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

/** Translate raw timeline event kinds into the human-readable activity log,
 * newest first, capped to the last 5. */
export function translateActivity(timeline: TimelineEvent[]): ActivityItem[] {
  return timeline
    .slice(-5)
    .reverse()
    .map((event) => ({
      id: event.id,
      label: ACTIVITY_LABELS[event.kind] ?? titleCaseKind(event.kind),
      time: formatTime(event.created_at) ?? '',
    }));
}
