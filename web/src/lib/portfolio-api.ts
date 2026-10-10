import type { Actor, Blocker, Check, Decision, Evidence, TimelineEvent } from './types';
import type { PolicyCollection } from './policies';

/** Staff-confirmed operational metadata. It never establishes case permission. */
export interface CaseProfile {
  id: string;
  case_id: string;
  original_property_ref: string;
  property_key: string;
  asset_ref: string;
  property_group_key?: string;
  asset_group_key?: string;
  trade: string;
  window_start: string | null;
  window_end: string | null;
  reason: string;
  actor: Actor;
  created_at: string;
  case_revision: number;
}

export interface ProfileInput {
  property_key: string;
  asset_ref: string;
  trade: string;
  window_start: string | null;
  window_end: string | null;
  reason: string;
}

export interface Contractor {
  id: string;
  name: string;
  trades: string[];
  available_from: string;
  available_until: string;
  reason: string;
  actor: Actor;
  created_at: string;
}

export interface IncidentSuggestion {
  id?: string;
  case_ids: string[];
  property_key: string;
  asset_ref?: string;
  reason?: string;
  reasons?: string[];
  time_basis?: string;
  window_days?: number;
  signals?: { case_id: string; title: string; category: string; work_item: string; reported_at: string; source_record_ids: string[] }[];
}

export interface Incident {
  id: string;
  case_ids: string[];
  title: string;
  reason: string;
  status: string;
  created_at: string;
  actor: Actor;
  stale?: boolean;
  warnings?: string[];
}

export interface VisitPlan {
  id: string;
  contractor_id: string;
  case_ids: string[];
  start: string;
  end: string;
  status: string;
  reason: string;
  created_at: string;
  stale: boolean;
  blockers: { case_id: string; key: string; status: string; reason: string; owner: string }[];
  warnings?: string[];
  planning_warning?: string;
  travel_checked?: boolean;
}

export interface Portfolio {
  profiles: CaseProfile[];
  contractors: Contractor[];
  incidents: Incident[];
  suggestions: IncidentSuggestion[];
  plans: VisitPlan[];
}

export interface InsightClaim {
  id: string;
  source_id: string;
  source_label: string;
  source_quote: string;
  value: unknown;
  verified: boolean;
  created_at: string;
  occurred_at: string;
  actor: Actor | null;
  applicability: string;
  superseded_by?: string;
  scope: Record<string, unknown>;
  expires_at?: string | null;
  verification?: string | null;
  verified_by?: Actor | null;
  party?: Record<string, unknown> | null;
  hearsay?: boolean;
}

export interface EvidenceComparison {
  key: string;
  scope: Record<string, unknown>;
  status: string;
  reason: string;
  claims: InsightClaim[];
  applies_to_current_action: boolean;
}

export interface PlaybackFrame {
  id: string;
  at: string;
  decision: Decision;
  evidence: Evidence[];
  events: TimelineEvent[];
}

export interface CaseInsights {
  case_id: string;
  as_of: string;
  comparisons: EvidenceComparison[];
  frames: PlaybackFrame[];
  playback_notice: string;
  comparison_notice: string;
}

export interface ComparedDecision {
  outcome: string;
  checks: Check[];
  blockers: Blocker[];
  owner?: string;
  next_step?: string;
  policy_version?: number;
  recorded_decision?: Decision;
}

export interface PolicyComparison {
  active_version: number;
  proposed_version: number;
  draft_id: string;
  stale_base: boolean;
  as_of: string;
  assumptions: string[];
  rows: {
    case_id: string;
    title: string;
    before: ComparedDecision;
    after: ComparedDecision;
    changes: { key: string; before: unknown; after: unknown; reason: string }[];
    completed: boolean;
    receipt?: Record<string, unknown>;
  }[];
}

async function request<T>(path: string, body?: unknown, signal?: AbortSignal): Promise<T> {
  const response = await fetch(path, {
    credentials: 'include', signal,
    ...(body === undefined ? {} : { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) }),
  });
  if (!response.ok) {
    let message = `Request failed (${response.status}). Please try again.`;
    try {
      const data = await response.json();
      if (typeof data.detail === 'string') message = data.detail;
      else if (Array.isArray(data.detail)) message = data.detail.map((item: { loc?: (string | number)[]; msg?: string }) => `${item.loc?.filter((part) => part !== 'body').join('.') || 'Input'}: ${item.msg || 'Check this value'}`).join('; ');
    } catch { /* Preserve the HTTP status when the response has no JSON detail. */ }
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

const pathId = (id: string) => encodeURIComponent(id);
export const getPortfolio = (signal?: AbortSignal) => request<Portfolio>('/api/portfolio', undefined, signal);
export const saveCaseProfile = (caseId: string, input: ProfileInput) => request<CaseProfile>(`/api/portfolio/cases/${pathId(caseId)}/profile`, input);
export const createContractor = (input: Pick<Contractor, 'name' | 'trades' | 'available_from' | 'available_until' | 'reason'>) => request<Contractor>('/api/portfolio/contractors', input);
export const createIncident = (case_ids: string[], title: string, reason: string) => request<Incident>('/api/portfolio/incidents', { case_ids, title, reason });
export const updateIncident = (id: string, status: 'resolved' | 'dismissed', reason: string) => request<Incident>(`/api/portfolio/incidents/${pathId(id)}/status`, { status, reason });
export const dismissSuggestion = (id: string, reason: string) => request<unknown>(`/api/portfolio/suggestions/${pathId(id)}/dismiss`, { reason });
export const createVisitPlan = (input: Pick<VisitPlan, 'contractor_id' | 'case_ids' | 'start' | 'end' | 'reason'>) => request<VisitPlan>('/api/portfolio/plans', input);
export const cancelVisitPlan = (id: string, reason: string) => request<VisitPlan>(`/api/portfolio/plans/${pathId(id)}/cancel`, { reason });
export const getCaseInsights = (caseId: string, signal?: AbortSignal) => request<CaseInsights>(`/api/cases/${pathId(caseId)}/insights`, undefined, signal);
export const getComparisonPolicies = (signal?: AbortSignal) => request<PolicyCollection>('/api/policies', undefined, signal);
export const comparePolicy = (draft_id: string, case_ids: string[], signal?: AbortSignal) => request<PolicyComparison>('/api/policy-comparison', { draft_id, case_ids }, signal);

/** An empty field remains unknown; never substitute the current time. */
export function localDateTimeToIso(value: string): string | null {
  if (!value) return null;
  const parts = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2}))?$/.exec(value);
  if (!parts) throw new Error('Enter a valid local date and time.');
  const date = new Date(value);
  if (!Number.isFinite(date.valueOf())) throw new Error('Enter a valid date and time.');
  const matchesWallTime = (candidate: Date) => candidate.getFullYear() === Number(parts[1]) && candidate.getMonth() + 1 === Number(parts[2]) && candidate.getDate() === Number(parts[3]) && candidate.getHours() === Number(parts[4]) && candidate.getMinutes() === Number(parts[5]) && candidate.getSeconds() === Number(parts[6] || 0);
  if (!matchesWallTime(date)) throw new Error('This local date or time does not exist, possibly because the clocks change. Choose a valid time in the displayed timezone.');
  // A repeated wall time has two valid UTC instants. Do not silently choose
  // one when the form does not have a control for its UTC offset.
  const offsets = new Set([-36, 36].map((hours) => new Date(date.valueOf() + hours * 3_600_000).getTimezoneOffset()));
  for (const offset of offsets) {
    const alternate = new Date(date.valueOf() + (offset - date.getTimezoneOffset()) * 60_000);
    if (alternate.valueOf() !== date.valueOf() && matchesWallTime(alternate)) throw new Error('This local time occurs twice when the clocks change. Choose a time outside that repeated hour; an explicit UTC-offset control is not available here.');
  }
  return date.toISOString();
}

export function isoToLocalInput(value: string | null | undefined): string {
  if (!value) return '';
  const date = new Date(value);
  if (!Number.isFinite(date.valueOf())) return '';
  const local = new Date(date.valueOf() - date.getTimezoneOffset() * 60_000);
  return local.toISOString().slice(0, 16);
}

export function readableValue(value: unknown): string {
  if (value === undefined || value === null || value === '') return 'Not recorded';
  if (typeof value === 'boolean') return value ? 'Yes' : 'No';
  if (typeof value === 'string' || typeof value === 'number') return String(value);
  return JSON.stringify(value);
}

export const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
export const errorText = (error: unknown) => error instanceof Error ? error.message : 'The request could not be completed. Please try again.';
export function dateLabel(value: string | null | undefined) {
  if (!value) return 'Not recorded';
  const date = new Date(value);
  return Number.isFinite(date.valueOf()) ? date.toLocaleString('en-GB', { dateStyle: 'medium', timeStyle: 'short' }) : value;
}
