/// <reference types="node" />
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { comparePolicy, createVisitPlan, getCaseInsights, getPortfolio, isoToLocalInput, localDateTimeToIso, readableValue, saveCaseProfile } from './portfolio-api.ts';

test('unknown time and asset details remain unknown when saving a confirmed profile', async () => {
  const original = globalThis.fetch;
  let request: { path: unknown; init?: RequestInit } | undefined;
  globalThis.fetch = async (path, init) => { request = { path, init }; return new Response('{}', { status: 200 }); };
  try {
    await saveCaseProfile('fictional-case', { property_key: 'Fictional building', asset_ref: '', trade: 'plumbing', window_start: localDateTimeToIso(''), window_end: localDateTimeToIso(''), reason: 'Staff confirmed the fictional building' });
    assert.equal(request?.path, '/api/portfolio/cases/fictional-case/profile');
    assert.equal(request?.init?.credentials, 'include');
    assert.equal(request?.init?.method, 'POST');
    assert.deepEqual(JSON.parse(String(request?.init?.body)), { property_key: 'Fictional building', asset_ref: '', trade: 'plumbing', window_start: null, window_end: null, reason: 'Staff confirmed the fictional building' });
  } finally { globalThis.fetch = original; }
});

test('reading portfolio and historical frames never causes a POST or a case mutation', async () => {
  const original = globalThis.fetch;
  const requests: { path: unknown; init?: RequestInit }[] = [];
  globalThis.fetch = async (path, init) => { requests.push({ path, init }); return new Response('{}', { status: 200 }); };
  try {
    await getPortfolio(); await getCaseInsights('case/with space');
    assert.deepEqual(requests.map(({ path }) => path), ['/api/portfolio', '/api/cases/case%2Fwith%20space/insights']);
    for (const request of requests) { assert.equal(request.init?.method, undefined); assert.equal(request.init?.body, undefined); assert.equal(request.init?.credentials, 'include'); }
  } finally { globalThis.fetch = original; }
});

test('stale plan and policy permission errors are surfaced instead of claiming success', async () => {
  const original = globalThis.fetch;
  globalThis.fetch = async () => new Response(JSON.stringify({ detail: 'The plan is stale. Review the changed case.' }), { status: 409 });
  try {
    await assert.rejects(createVisitPlan({ contractor_id: 'fictional-contractor', case_ids: ['fictional-case'], start: '2026-10-10T09:00:00Z', end: '2026-10-10T10:00:00Z', reason: 'Fictional test' }), /plan is stale/);
    globalThis.fetch = async () => new Response(JSON.stringify({ detail: 'Role policy_editor required' }), { status: 403 });
    await assert.rejects(comparePolicy('fictional-draft', ['fictional-case']), /policy_editor required/);
  } finally { globalThis.fetch = original; }
});

test('date inputs preserve local wall time through an aware ISO round trip', () => {
  const local = '2026-10-10T11:30';
  assert.equal(isoToLocalInput(localDateTimeToIso(local)), local);
  assert.equal(localDateTimeToIso(''), null);
  assert.equal(isoToLocalInput(null), '');
  assert.throws(() => localDateTimeToIso('not a date'), /valid local date/);
  assert.equal(readableValue(false), 'No');
  assert.equal(readableValue(undefined), 'Not recorded');
});

test('London clock changes never silently shift or ambiguously choose a planned visit time', () => {
  const previousTimezone = process.env.TZ;
  process.env.TZ = 'Europe/London';
  try {
    assert.throws(() => localDateTimeToIso('2027-03-28T01:30'), /does not exist/);
    assert.throws(() => localDateTimeToIso('2026-10-25T01:30'), /occurs twice/);
    assert.throws(() => localDateTimeToIso('2026-02-30T12:00'), /does not exist/);
    assert.equal(localDateTimeToIso('2026-10-25T02:30'), '2026-10-25T02:30:00.000Z');
  } finally {
    if (previousTimezone === undefined) delete process.env.TZ;
    else process.env.TZ = previousTimezone;
  }
});
