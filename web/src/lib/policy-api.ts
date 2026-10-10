import type { PolicyCollection, PolicyDraftInput, PolicyPreview, PolicyRecord, PolicySuggestion } from './policies';

async function policyRequest<T>(path: string, body?: unknown): Promise<T> {
  const response = await fetch(path, {
    credentials: 'include',
    ...(body === undefined ? {} : {
      method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body),
    }),
  });
  if (!response.ok) {
    let message = `The policy service returned ${response.status}. Please try again.`;
    try {
      const data = await response.json();
      if (typeof data.detail === 'string') message = data.detail;
      else if (Array.isArray(data.detail)) {
        message = data.detail.map((item: { msg?: string }) => item.msg ?? 'Check the submitted values.').join(' ');
      }
    } catch { /* Keep the status message if the response was not JSON. */ }
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

export const getPolicies = () => policyRequest<PolicyCollection>('/api/policies');
export const interpretPolicy = (text: string) => policyRequest<PolicySuggestion>('/api/policy-assistant/interpret', { text });
export const savePolicyDraft = (draft: PolicyDraftInput) => policyRequest<PolicyRecord>('/api/policies/draft', draft);
export const previewPolicyDraft = (id: string) => policyRequest<PolicyPreview>(`/api/policies/${encodeURIComponent(id)}/preview`, {});
export const publishPolicyDraft = (id: string) => policyRequest<PolicyRecord>(`/api/policies/${encodeURIComponent(id)}/publish`, {});
