import { request } from './api';
import type { PolicyCollection, PolicyDraft, PolicyDraftInput, PolicyPreview, PolicyRecord, PolicySuggestion } from './policies';

/** Use the selected staff session; these requests never switch roles. */
const post = <T>(path: string, body: unknown = {}) => request<T>(path, {
  method: 'POST', body: JSON.stringify(body),
});

export const getPolicies = (signal?: AbortSignal) => request<PolicyCollection>('/api/policies', { signal });
export const interpretPolicy = (text: string, reviewId?: string) => post<PolicySuggestion>('/api/policy-assistant/interpret', {
  text, ...(reviewId ? { review_id: reviewId } : {}),
});
export const reviewPolicySuggestion = (reviewId: string) => request<PolicySuggestion>(`/api/policy-assistant/reviews/${encodeURIComponent(reviewId)}/suggestion`);
export const savePolicyDraft = (draft: PolicyDraftInput) => post<PolicyDraft>('/api/policies/draft', draft);
export const previewPolicyDraft = (id: string) => post<PolicyPreview>(`/api/policies/${encodeURIComponent(id)}/preview`);
export const publishPolicyDraft = (id: string) => post<PolicyRecord>(`/api/policies/${encodeURIComponent(id)}/publish`);
