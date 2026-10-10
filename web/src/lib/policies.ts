/**
 * Front-end-only policy model for the Policy Engine panel. This is a
 * presentation/demo layer: policies live in React state, are seeded with
 * plausible examples, and category detection is keyword-based. No backend
 * call is involved (the real policy engine in app/ has its own structured
 * rule format; this panel is the plain-English operator view on top).
 */

export type PolicyCategory = 'Urgency' | 'Cost' | 'Escalation' | 'Contractor' | 'Comms';
export type PolicySource = 'Manual' | 'AI-learned';

export const POLICY_CATEGORIES: PolicyCategory[] = [
  'Urgency',
  'Cost',
  'Escalation',
  'Contractor',
  'Comms',
];

export interface Policy {
  id: string;
  text: string;
  category: PolicyCategory;
  threshold?: string;
  enabled: boolean;
  source: PolicySource;
}

export interface Thresholds {
  emergencyLimit: number; // £, 0–2000
  escalateAfterMin: number; // minutes, 30–240
  pingAfterHr: number; // hours, 1–48
  maxResolveDays: number; // days, 1–14
}

export const DEFAULT_THRESHOLDS: Thresholds = {
  emergencyLimit: 500,
  escalateAfterMin: 120,
  pingAfterHr: 24,
  maxResolveDays: 7,
};

/** Keyword buckets, checked in priority order so a cost+urgency sentence
 * lands on the most operationally specific category. */
const CATEGORY_KEYWORDS: [PolicyCategory, RegExp][] = [
  ['Cost', /\b(£|\$|cost|budget|limit|spend|spending|quote|price|invoice|approv\w* spend|sign-?off)\b/i],
  ['Urgency', /\b(emergency|urgent|hazard|immediat\w*|safety|danger|leak|flood|gas|fire|no (hot water|heating))\b/i],
  ['Escalation', /\b(escalat\w*|manager|overdue|no reply|no response|deadline|breach|SLA|within \d)\b/i],
  ['Contractor', /\b(contractor|provider|engineer|dispatch|assign|vetted|directory|trade|plumber|electrician)\b/i],
  ['Comms', /\b(remind\w*|message|contact|notify|notif\w*|email|call|chase|ping|update the tenant|keep .* informed)\b/i],
];

/** Best-guess category for a free-text policy. Falls back to Comms when
 * nothing matches, since an un-categorised rule is usually a notification. */
export function detectCategory(text: string): PolicyCategory {
  for (const [category, pattern] of CATEGORY_KEYWORDS) {
    if (pattern.test(text)) return category;
  }
  return 'Comms';
}

/** Pull a human threshold badge out of free text if one is stated, e.g.
 * "£500", "2 working days", "48 hours". Returns undefined when none found. */
export function detectThreshold(text: string): string | undefined {
  const money = text.match(/£\s?\d[\d,]*/);
  if (money) return `${money[0].replace(/\s/g, '')} limit`;
  const duration = text.match(/\b(\d+)\s?(working day|day|days|hour|hours|hr|hrs|min|minute|minutes)\b/i);
  if (duration) return `${duration[1]} ${duration[2].replace(/s$/, '')} limit`;
  return undefined;
}

let seq = 0;
export function newPolicyId(): string {
  seq += 1;
  return `pol-${Date.now()}-${seq}`;
}

export const SEED_POLICIES: Policy[] = [
  {
    id: 'seed-1',
    text: 'Emergency repairs affecting safety (gas, flooding, no heating in winter) are dispatched immediately without waiting for landlord approval.',
    category: 'Urgency',
    enabled: true,
    source: 'Manual',
  },
  {
    id: 'seed-2',
    text: 'Any repair quoted above £500 requires landlord sign-off before a contractor is instructed.',
    category: 'Cost',
    threshold: '£500 limit',
    enabled: true,
    source: 'Manual',
  },
  {
    id: 'seed-3',
    text: "If the landlord hasn't replied within 2 working days, escalate the case to a property manager.",
    category: 'Escalation',
    threshold: '2 working day limit',
    enabled: true,
    source: 'Manual',
  },
  {
    id: 'seed-4',
    text: 'Only instruct vetted contractors from the approved directory for gas and electrical work.',
    category: 'Contractor',
    enabled: false,
    source: 'AI-learned',
  },
];
