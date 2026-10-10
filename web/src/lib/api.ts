/**
 * Small typed fetch client for the Property Workflow backend.
 * All requests go through the same-origin `/api/...` path (proxied by Vite in
 * dev, served directly by FastAPI from /dashboard) and include the httpOnly
 * `pw_session` cookie set by a loopback demo session.
 *
 * The backend checks roles on every mutation (app/service.py Service.role), so
 * each mutation here names the role it acts as. Switching role replaces the
 * demo session cookie; it is demonstration navigation, not an authorisation
 * boundary — the backend still decides what each role may do.
 */
import type {
  AssistantResult,
  BuildCaseSummary,
  CaseDetail,
  CaseListItem,
  PoliciesResponse,
  PolicyDraft,
  PolicyInput,
  PolicyPreview,
  ReviewResponseInput,
  SessionInfo,
} from './types';

export type Role = 'case_manager' | 'policy_editor' | 'access_officer' | 'approver' | 'reviewer';

/** Readable labels for backend role ids. */
export const ROLE_LABELS: Record<string, string> = {
  case_manager: 'Case manager',
  policy_editor: 'Policy editor',
  access_officer: 'Access officer',
  approver: 'Approver',
  reviewer: 'Reviewer',
};

class ApiError extends Error {
  readonly status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    credentials: 'include',
    headers: { 'content-type': 'application/json' },
    ...init,
  });
  if (!response.ok) {
    let message = `Request failed: ${response.status} ${response.statusText}`;
    try {
      const body: unknown = await response.json();
      if (
        body &&
        typeof body === 'object' &&
        'detail' in body &&
        typeof (body as { detail?: unknown }).detail === 'string'
      ) {
        message = (body as { detail: string }).detail;
      }
    } catch {
      // Response body was not JSON; keep the status-based message.
    }
    throw new ApiError(message, response.status);
  }
  return response.json() as Promise<T>;
}

/** Create a loopback-only demo session cookie for the given role. */
export async function createDemoSession(role: Role): Promise<void> {
  await request<{ actor: { id: string; role: string }; mode: string }>(
    '/api/demo-session',
    { method: 'POST', body: JSON.stringify({ role }) },
  );
}

/** The role the current session cookie holds, as far as this tab knows. */
let currentRole: Role | null = null;

/** Make sure the demo session acts as `role`, then run `call`. Demo sessions
 * live in backend memory, so a backend restart drops them: on that 403 we
 * create a fresh session and retry once. */
export async function asRole<T>(role: Role, call: () => Promise<T>): Promise<T> {
  if (currentRole !== role) {
    await createDemoSession(role);
    currentRole = role;
  }
  try {
    return await call();
  } catch (err) {
    if (err instanceof ApiError && err.status === 403 && /demonstration session/i.test(err.message)) {
      await createDemoSession(role);
      currentRole = role;
      return call();
    }
    throw err;
  }
}

/** Reads work under any role; reuse whichever session is active. */
function read<T>(path: string): Promise<T> {
  return asRole(currentRole ?? 'case_manager', () => request<T>(path));
}

function post<T>(role: Role, path: string, body?: unknown): Promise<T> {
  return asRole(role, () =>
    request<T>(path, { method: 'POST', body: body === undefined ? undefined : JSON.stringify(body) }),
  );
}

/** Session, runtime mode and model configuration (never credentials). */
export async function getSession(): Promise<SessionInfo> {
  return request<SessionInfo>('/api/session');
}

/** List all live cases (cheap summary rows, not full detail). */
export async function listCases(): Promise<CaseListItem[]> {
  return read<CaseListItem[]>('/api/cases');
}

/** List the fixed BUILD catalogue of demo cases. */
export async function listBuildCases(): Promise<BuildCaseSummary[]> {
  return read<BuildCaseSummary[]>('/api/build-cases');
}

/** Import a chronological prefix of a BUILD case as a live case. Returns the new case id. */
export async function importBuildCase(
  id: string,
  eventCount: number,
): Promise<{ caseId: string }> {
  const detail = await post<CaseDetail>('case_manager', `/api/build-cases/${id}/import`, {
    event_count: eventCount,
  });
  return { caseId: detail.case.id };
}

/** Fetch the full detail of a live case. */
export async function getCaseDetail(id: string): Promise<CaseDetail> {
  return read<CaseDetail>(`/api/cases/${id}`);
}

/** Respond to an open review as the review's owning role
 * (approve/correct/reject/defer/more_evidence). */
export async function respondToReview(
  reviewId: string,
  role: Role,
  body: ReviewResponseInput,
): Promise<CaseDetail> {
  return post<CaseDetail>(role, `/api/reviews/${reviewId}/respond`, body);
}

/** Send a held Claude draft to the tenant (optionally edited). Simulated delivery. */
export async function approveMessage(messageId: string, text?: string): Promise<CaseDetail> {
  return post<CaseDetail>('case_manager', `/api/messages/${messageId}/approve`, text ? { text } : {});
}

/** Reject a held Claude draft; `redraft` asks Claude for another attempt. */
export async function rejectMessage(
  messageId: string,
  reason: string,
  redraft: boolean,
): Promise<CaseDetail> {
  return post<CaseDetail>('case_manager', `/api/messages/${messageId}/reject`, { reason, redraft });
}

/** Run the case's due reminders, escalations and review deadlines now. */
export async function runTimers(caseId: string): Promise<CaseDetail> {
  return post<CaseDetail>('case_manager', `/api/cases/${caseId}/tick`);
}

/** Active policy plus saved drafts. */
export async function getPolicies(): Promise<PoliciesResponse> {
  return read<PoliciesResponse>('/api/policies');
}

/** Turn plain English into a proposed policy draft. Never writes policy. */
export async function interpretPolicy(text: string, reviewId?: string): Promise<AssistantResult> {
  return post<AssistantResult>(currentRole ?? 'case_manager', '/api/policy-assistant/interpret', {
    text,
    ...(reviewId ? { review_id: reviewId } : {}),
  });
}

/** A conservative reusable-rule suggestion from a completed review decision. */
export async function reviewPolicySuggestion(reviewId: string): Promise<AssistantResult> {
  return read<AssistantResult>(`/api/policy-assistant/reviews/${reviewId}/suggestion`);
}

/** Save a draft and run its impact preview in one step (policy editor). */
export async function draftAndPreviewPolicy(
  input: PolicyInput,
): Promise<{ draft: PolicyDraft; preview: PolicyPreview }> {
  const draft = await post<PolicyDraft>('policy_editor', '/api/policies/draft', input);
  const preview = await post<PolicyPreview>('policy_editor', `/api/policies/${draft.id}/preview`);
  return { draft, preview };
}

/** Publish a previewed draft; every open case is reassessed by the workflow. */
export async function publishPolicy(draftId: string): Promise<void> {
  await post<unknown>('policy_editor', `/api/policies/${draftId}/publish`);
}
