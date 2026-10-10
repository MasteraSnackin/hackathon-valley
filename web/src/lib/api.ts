/**
 * Small typed fetch client for the Property Workflow backend.
 * All requests go through the same-origin `/api/...` path (proxied by Vite in
 * dev) and include the httpOnly `pw_session` cookie set by createDemoSession.
 */
import type {
  BuildCaseSummary,
  CaseDetail,
  CaseListItem,
  ReviewResponseInput,
} from './types';

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
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

/** Create a loopback-only demo session cookie for the given role. */
export async function createDemoSession(role: string): Promise<void> {
  await request<{ actor: { id: string; role: string }; mode: string }>(
    '/api/demo-session',
    { method: 'POST', body: JSON.stringify({ role }) },
  );
}

/** List all live cases (cheap summary rows, not full detail). */
export async function listCases(): Promise<CaseListItem[]> {
  return request<CaseListItem[]>('/api/cases');
}

/** List the fixed BUILD catalogue of demo cases. */
export async function listBuildCases(): Promise<BuildCaseSummary[]> {
  return request<BuildCaseSummary[]>('/api/build-cases');
}

/** Import a chronological prefix of a BUILD case as a live case. Returns the new case id. */
export async function importBuildCase(
  id: string,
  eventCount: number,
): Promise<{ caseId: string }> {
  const detail = await request<CaseDetail>(`/api/build-cases/${id}/import`, {
    method: 'POST',
    body: JSON.stringify({ event_count: eventCount }),
  });
  return { caseId: detail.case.id };
}

/** Fetch the full detail of a live case. */
export async function getCaseDetail(id: string): Promise<CaseDetail> {
  return request<CaseDetail>(`/api/cases/${id}`);
}

/** Respond to an open review (approve/correct/reject/defer/more_evidence). */
export async function respondToReview(
  reviewId: string,
  body: ReviewResponseInput,
): Promise<CaseDetail> {
  return request<CaseDetail>(`/api/reviews/${reviewId}/respond`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}
