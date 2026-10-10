/// <reference types="node" />
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { describePolicyChangeValue, policyChangeLabel } from './portfolio-presentation.ts';
import { policyLabel } from './policies.ts';

test('changed blocker headings describe the requirement without exposing its internal rule key', () => {
  assert.equal(policyChangeLabel('blocker:access:require-access'), 'Access permission requirement');
  assert.equal(policyChangeLabel('outcome'), 'Decision outcome');
  assert.equal(policyChangeLabel('identity'), 'Person and property identity check');
});

test('blockers present status, response, owner and reason while preserving source identifiers as metadata', () => {
  const presentation = describePolicyChangeValue({ key: 'access', status: 'UNKNOWN', response: 'HUMAN REVIEW', owner: 'case_manager', reason: 'Permission has not been confirmed.', rule_id: 'require-access', source_ids: ['source-1'], claim_ids: [] });
  assert.deepEqual(presentation.fields, [
    { label: 'Status', value: 'missing or unverified' }, { label: 'Response', value: 'Human review' },
    { label: 'Decision owner', value: policyLabel('case_manager') }, { label: 'Reason', value: 'Permission has not been confirmed.' },
  ]);
  assert.equal(presentation.metadata.rule_id, 'require-access');
  assert.deepEqual(presentation.metadata.source_ids, ['source-1']);
  assert.equal(presentation.metadata.reason, undefined);
});

test('simple values and missing requirements remain distinct; amounts use only recorded currency', () => {
  assert.equal(describePolicyChangeValue('ACT').text, policyLabel('ACT'));
  assert.equal(describePolicyChangeValue(false).text, 'No');
  assert.equal(describePolicyChangeValue(0).text, '0');
  assert.equal(describePolicyChangeValue(null).text, 'No requirement on this side.');
  assert.deepEqual(describePolicyChangeValue({ amount: 100 }).fields, [{ label: 'Amount', value: '100' }]);
  assert.deepEqual(describePolicyChangeValue({ amount: 100, currency: 'GBP' }).fields, [{ label: 'Amount', value: '£100.00' }]);
});
