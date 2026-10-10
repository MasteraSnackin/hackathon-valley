import { policyLabel } from './policies.ts';

export interface PolicyChangePresentation {
  text?: string;
  fields: { label: string; value: string }[];
  metadata: Record<string, unknown>;
}

/** Keep internal rule identifiers out of the staff-facing change heading. */
export function policyChangeLabel(key: string): string {
  if (key === 'outcome') return 'Decision outcome';
  if (key.startsWith('blocker:')) return `${policyLabel(key.split(':')[1] || 'Case')} requirement`;
  return `${policyLabel(key)} check`;
}

function scalar(value: unknown): string | null {
  if (value === null || value === undefined || value === '') return 'Not recorded';
  if (typeof value === 'boolean') return value ? 'Yes' : 'No';
  if (typeof value === 'number') return value.toLocaleString('en-GB');
  if (typeof value === 'string') return value;
  return null;
}

/** Structured checks and blockers become labelled facts; identifiers remain inspectable. */
export function describePolicyChangeValue(value: unknown): PolicyChangePresentation {
  if (value === null || value === undefined) return { text: 'No requirement on this side.', fields: [], metadata: {} };
  if (typeof value !== 'object') return { text: typeof value === 'string' ? policyLabel(value) : scalar(value) || 'Not recorded', fields: [], metadata: {} };
  if (Array.isArray(value)) return { text: `${value.length} recorded values.`, fields: [], metadata: { values: value } };
  const record = value as Record<string, unknown>;
  const fields: PolicyChangePresentation['fields'] = [];
  const used = new Set<string>();
  const labels = [
    ['status', 'Status', true], ['response', 'Response', true], ['owner', 'Decision owner', true],
    ['reason', 'Reason', false], ['action', 'Action', true], ['next_step', 'Next step', false],
    ['rule_name', 'Rule', false], ['amount', 'Amount', false], ['total', 'Total', false],
    ['value', 'Value', false], ['limit', 'Limit', false], ['threshold', 'Threshold', false],
  ] as const;
  for (const [key, label, translate] of labels) {
    if (!(key in record)) continue;
    let display = scalar(record[key]);
    if (display === null) continue;
    if (translate && typeof record[key] === 'string') display = policyLabel(record[key]);
    if (['amount', 'total', 'limit', 'threshold'].includes(key) && typeof record[key] === 'number' && typeof record.currency === 'string' && /^[A-Z]{3}$/.test(record.currency)) {
      display = new Intl.NumberFormat('en-GB', { style: 'currency', currency: record.currency }).format(record[key]);
      used.add('currency');
    }
    fields.push({ label, value: display }); used.add(key);
  }
  return {
    ...(fields.length ? {} : { text: 'Recorded requirement details.' }),
    fields,
    metadata: Object.fromEntries(Object.entries(record).filter(([key]) => !used.has(key))),
  };
}
