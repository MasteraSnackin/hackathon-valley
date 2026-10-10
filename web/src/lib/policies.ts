/**
 * Plain-English view of the backend's structured policy (app/domain.py
 * DEFAULT_SETTINGS and Rule). The backend policy is the only source of truth:
 * these helpers describe it for operators and build PolicyInput drafts, which
 * the backend validates, previews and publishes.
 */
import type { ActivePolicy, PolicyInput, PolicyRule, PolicySettings } from './types';

export type PolicyCategory = 'Cost' | 'Escalation' | 'Access' | 'Comms' | 'Routing' | 'Rule';
export type PolicySource = 'Setting' | 'Manual rule' | 'AI-drafted rule';

export interface PolicyCardVM {
  id: string;
  text: string;
  category: PolicyCategory;
  threshold?: string;
  source: PolicySource;
  /** Set for structured rules, which can be removed through a new draft. */
  ruleId?: string;
}

/** The threshold sliders map onto these real settings. */
export interface Thresholds {
  review_limit: number; // £, financial review above this verified total
  reminder_hours: number; // working hours before a reminder
  escalation_hours: number; // working hours before escalation to a person
  reminder_limit: number; // reminders per question, 0–5
}

export function thresholdsOf(settings: PolicySettings): Thresholds {
  return {
    review_limit: settings.review_limit,
    reminder_hours: settings.reminder_hours,
    escalation_hours: settings.escalation_hours,
    reminder_limit: settings.reminder_limit,
  };
}

const ACTION_LABELS: Record<string, string> = {
  clarify: 'clarifications',
  request_quote: 'quote requests',
  confirm_appointment: 'appointment confirmations',
  supply_keys: 'key handovers',
  instruct_work: 'work instructions',
  close_item: 'closing a repair',
  archive: 'archiving',
};

const STATUS_LABELS: Record<string, string> = {
  UNKNOWN: 'missing or unverified',
  CONFLICT: 'conflicting',
  FAIL: 'refused',
  PASS: 'confirmed',
};

const RESPONSE_LABELS: Record<string, string> = {
  'HUMAN REVIEW': 'Send to human review',
  'STOP ACTION': 'Stop the action',
  CLARIFY: 'Ask for clarification',
  WAIT: 'Wait',
};

const OWNER_LABELS: Record<string, string> = {
  case_manager: 'a case manager',
  access_officer: 'an access officer',
  approver: 'an approver',
  reviewer: 'a reviewer',
  policy_editor: 'a policy editor',
};

const money = (n: number) => `£${n.toLocaleString('en-GB', { maximumFractionDigits: 2 })}`;
const hours = (n: number) => `${n} working ${n === 1 ? 'hour' : 'hours'}`;

export function describeRule(rule: PolicyRule): string {
  const when = rule.conditions
    .map((c) => `${c.key} is ${STATUS_LABELS[c.status] ?? c.status}`)
    .join(rule.match === 'any' ? ' or ' : ' and ');
  const scope = rule.actions.length
    ? rule.actions.map((a) => ACTION_LABELS[a] ?? a).join(', ')
    : 'all actions';
  const where = rule.property_ref ? ` at ${rule.property_ref}` : '';
  return `${RESPONSE_LABELS[rule.response] ?? rule.response} when ${when}, for ${scope}${where}. Owned by ${OWNER_LABELS[rule.owner] ?? rule.owner}.`;
}

/** Every operator-relevant part of the active policy as a readable card. */
export function describePolicy(policy: ActivePolicy): PolicyCardVM[] {
  const s = policy.settings;
  const tenantMessages: Record<string, string> = {
    claude_decides:
      'Claude may send routine tenant questions on its own; risky, urgent or unverified ones wait for a case manager.',
    staff_approval: 'Every tenant message Claude drafts waits for a case manager to send it.',
    off: 'Claude does not draft tenant messages.',
  };
  const triage: Record<string, string> = {
    high: "Claude's reading of a message is applied automatically only at high confidence; anything less waits for a case manager.",
    medium: "Claude's reading of a message is applied automatically at medium or high confidence.",
    never: "Every Claude reading of a message waits for a case manager to confirm it.",
  };
  const cards: PolicyCardVM[] = [
    {
      id: 'setting-review-limit',
      text: `Work instructions with a verified total above ${money(s.review_limit)} need a scoped approval from an approver before a contractor is instructed.`,
      category: 'Cost',
      threshold: `${money(s.review_limit)} limit`,
      source: 'Setting',
    },
    {
      id: 'setting-follow-up',
      text: `Unanswered questions get ${s.reminder_limit === 0 ? 'no reminders' : `up to ${s.reminder_limit} reminder${s.reminder_limit === 1 ? '' : 's'} after ${hours(s.reminder_hours)}`} and escalate to a person after ${hours(s.escalation_hours)}.`,
      category: 'Escalation',
      threshold: `${s.escalation_hours}h escalation`,
      source: 'Setting',
    },
    {
      id: 'setting-access',
      text: s.access_immediate_review
        ? 'Missing access permission goes straight to human review.'
        : 'Missing access permission is requested from the tenant before anyone enters the property.',
      category: 'Access',
      source: 'Setting',
    },
    {
      id: 'setting-approvals',
      text: `Approvals cover one exact action and expire after ${s.approval_hours} hours.`,
      category: 'Escalation',
      threshold: `${s.approval_hours}h expiry`,
      source: 'Setting',
    },
    {
      id: 'setting-tenant-messages',
      text: tenantMessages[s.tenant_messages] ?? `Tenant messages: ${s.tenant_messages}.`,
      category: 'Comms',
      source: 'Setting',
    },
    {
      id: 'setting-triage',
      text: triage[s.triage_auto_accept] ?? `Triage auto-accept: ${s.triage_auto_accept}.`,
      category: 'Routing',
      source: 'Setting',
    },
  ];
  const rules: PolicyCardVM[] = policy.rules.map((rule) => ({
    id: `rule-${rule.id}`,
    text: describeRule(rule),
    category: 'Rule',
    source: rule.id.startsWith('assistant-') ? 'AI-drafted rule' : 'Manual rule',
    ruleId: rule.id,
  }));
  return [...rules, ...cards];
}

/** A draft that keeps the active policy except for the given changes. */
export function draftFrom(
  policy: ActivePolicy,
  changes: { settings?: Partial<PolicySettings> | Thresholds; rules?: PolicyRule[] },
  reason: string,
): PolicyInput {
  return {
    base_version: policy.version,
    settings: { ...policy.settings, ...changes.settings },
    rules: changes.rules ?? policy.rules,
    reason,
  };
}

/** Human summary of staged threshold changes, or an empty list if none. */
export function thresholdChanges(before: Thresholds, after: Thresholds): string[] {
  const out: string[] = [];
  if (before.review_limit !== after.review_limit)
    out.push(`Financial review above ${money(after.review_limit)} (was ${money(before.review_limit)})`);
  if (before.reminder_hours !== after.reminder_hours)
    out.push(`Reminder after ${hours(after.reminder_hours)} (was ${before.reminder_hours})`);
  if (before.escalation_hours !== after.escalation_hours)
    out.push(`Escalate after ${hours(after.escalation_hours)} (was ${before.escalation_hours})`);
  if (before.reminder_limit !== after.reminder_limit)
    out.push(`At most ${after.reminder_limit} reminders (was ${before.reminder_limit})`);
  return out;
}
