/// <reference types="node" />
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { computeDetailedPipeline, findReviewForBlocker, stagePillOf, toCaseSummaryVM, translateActivity } from './pipeline.ts';
import type { ActionState, Blocker, CaseDetail, CaseListItem, Review } from './types.ts';

const timestamp = '2026-10-10T11:00:00Z';
const blocker: Blocker = { key: 'identity', status: 'UNKNOWN', reason: 'Confirm the property', source_ids: [], claim_ids: [], response: 'HUMAN REVIEW', owner: 'case_manager', rule_id: 'required.identity' };
function fixture(): CaseDetail {
  return {
    case: { id: 'fictional-case', title: 'Fictional request', property_ref: 'Example Flat', category: 'plumbing', profile: 'default', revision: 1, action_revision: 1, proposal: { action: 'request_quote', work_item: 'Tap', provider: '', access_method: '', scope: {} }, status: 'open', owner: 'case_manager', next_step: 'Check identity', policy_pending: false, created_at: timestamp },
    claims: [], evidence: [], reviews: [], questions: [], actions: [], timeline: [],
    decision: { id: 'decision-1', created_at: timestamp, outcome: 'HUMAN REVIEW', checks: [blocker], blockers: [blocker], owner: 'case_manager', next_step: 'Check identity', policy_version: 1, case_revision: 1, action_revision: 1, scope: {}, assessed_at: timestamp },
  };
}
function receipt(status: ActionState['status'] = 'succeeded'): ActionState {
  return { id: 'action-1', created_at: timestamp, business_id: 'current-action', status, scope: {}, decision_id: 'decision-1', simulated: true, actor: { id: 'system', role: 'system' } };
}
function review(patch: Partial<Review> = {}): Review {
  return { id: 'review-1', created_at: timestamp, key: blocker.key, signature: 'test', question: blocker.reason, owner: blocker.owner, rule_id: blocker.rule_id, policy_version: 1, action_revision: 1, scope: {}, source_ids: [], claim_ids: [], other_blockers: [], expires_at: '2026-10-11T11:00:00Z', next_step: 'Recheck', status: 'open', response: null, ...patch };
}

test('an internal wake signal never claims an email was delivered', () => {
  const [activity] = translateActivity([{ id: 'signal', kind: 'signal_outbox', case_id: 'fictional-case', created_at: timestamp, payload: {} }]);
  assert.equal(activity.label, 'Workflow notified');
  assert.doesNotMatch(activity.label, /email|landlord|sent/i);
});

test('missing checks do not invent contractor contact, scheduling or repair completion', () => {
  const detail = fixture();
  const nodes = computeDetailedPipeline(detail);
  assert.equal(nodes.find((node) => node.key === 'checks')?.state, 'current');
  assert.equal(nodes.find((node) => node.key === 'result')?.state, 'future');
  assert.ok(nodes.every((node) => !/assigned|contacted|replied|scheduled|done|repair finished/i.test(node.label)));
});

test('ready action has no completed result without its current successful simulated receipt', () => {
  const detail = fixture();
  detail.decision = { ...detail.decision!, outcome: 'ACT', blockers: [] };
  assert.equal(computeDetailedPipeline(detail).at(-1)?.state, 'current');
  detail.decision = { ...detail.decision, outcome: 'NO FURTHER ACTION' };
  assert.notEqual(computeDetailedPipeline(detail).at(-1)?.state, 'completed');
  detail.actions = [receipt()];
  detail.decision.completed_action_id = 'another-action';
  assert.notEqual(computeDetailedPipeline(detail).at(-1)?.state, 'completed');
  detail.decision.completed_action_id = 'action-1';
  assert.equal(computeDetailedPipeline(detail).at(-1)?.state, 'completed');
});

test('uncertain and non-simulated receipts do not count as successful simulated results', () => {
  const detail = fixture();
  detail.decision = { ...detail.decision!, outcome: 'NO FURTHER ACTION', blockers: [], completed_action_id: 'action-1' };
  detail.actions = [receipt('uncertain')];
  assert.notEqual(computeDetailedPipeline(detail).at(-1)?.state, 'completed');
  detail.actions = [{ ...receipt(), simulated: false }];
  assert.notEqual(computeDetailedPipeline(detail).at(-1)?.state, 'completed');
});

test('queue keeps timestamps sortable and ready actions distinct from complete actions', () => {
  const item: CaseListItem = { ...fixture().case, outcome: 'ACT', open_reviews: 0, last_assessed_at: timestamp };
  const ready = toCaseSummaryVM(item);
  assert.equal(ready.timestamp, timestamp);
  assert.equal(ready.outcome, 'ACT');
  assert.equal(ready.resolvedInHours, undefined);
  assert.equal(stagePillOf(item), 'Ready to act');
  const complete = toCaseSummaryVM({ ...item, outcome: 'NO FURTHER ACTION' });
  assert.equal(complete.stagePill, 'Action complete');
  assert.equal(complete.resolvedInHours, undefined);
});

test('review selection matches the fact and rule in the current action and policy', () => {
  const detail = fixture();
  detail.reviews = [review({ id: 'wrong-key', key: 'authority' }), review({ id: 'wrong-rule', rule_id: 'custom-rule' }), review({ id: 'old-action', action_revision: 0 }), review({ id: 'old-policy', policy_version: 0 }), review({ id: 'expired', status: 'expired' }), review({ id: 'current', status: 'deferred' })];
  assert.equal(findReviewForBlocker(detail, blocker)?.id, 'current');
  detail.reviews.pop();
  assert.equal(findReviewForBlocker(detail, blocker), undefined);
});
