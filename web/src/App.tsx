import { useEffect, useState } from 'react';
import {
  createDemoSession,
  getCaseDetail,
  importBuildCase,
  respondToReview,
} from './lib/api';
import type { CaseDetail, Claim, Evidence, TimelineEvent as LibTimelineEvent } from './lib/types';
import Shell from './components/Shell';
import DecisionCard from './components/DecisionCard';
import ConversationThread from './components/ConversationThread';
import EvidencePanel from './components/EvidencePanel';
import ActivityTimeline from './components/ActivityTimeline';
import type {
  Decision as UiDecision,
  EvidenceItem as UiEvidenceItem,
  TimelineEvent as UiTimelineEvent,
} from './components/types';

const DEMO_BUILD_CASE_ID = '013';
const DEMO_EVENT_COUNT = 2;

/** Group claims by their source evidence id, and shape both into the
 * components' local (demo-friendly) prop types. */
function toEvidenceItems(evidence: Evidence[], claims: Claim[]): UiEvidenceItem[] {
  return evidence.map((item) => ({
    id: item.id,
    text: item.text,
    source_label: item.source_label,
    occurred_at: item.occurred_at,
    claims: claims
      .filter((claim) => claim.source_id === item.id)
      .map((claim) => ({
        id: claim.id,
        key: claim.key,
        value: claim.value,
        source_quote: claim.source_quote,
        verified: claim.verified,
      })),
  }));
}

/** The backend's `NO FURTHER ACTION` outcome means the same thing as `ACT`
 * for this screen (nothing further is held) — DecisionCard only distinguishes
 * ACT vs. the held states. */
function toUiDecision(decision: CaseDetail['decision']): UiDecision | null {
  if (!decision) return null;
  const outcome = decision.outcome === 'NO FURTHER ACTION' ? 'ACT' : decision.outcome;
  return { ...decision, outcome };
}

function toUiTimeline(timeline: LibTimelineEvent[]): UiTimelineEvent[] {
  return timeline.map((event) => ({
    id: event.id,
    kind: event.kind,
    at: event.created_at,
    detail: event.payload,
  }));
}

function App() {
  const [detail, setDetail] = useState<CaseDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [responding, setResponding] = useState(false);

  useEffect(() => {
    let cancelled = false;
    async function bootstrap() {
      try {
        await createDemoSession('case_manager');
        const { caseId } = await importBuildCase(DEMO_BUILD_CASE_ID, DEMO_EVENT_COUNT);
        const caseDetail = await getCaseDetail(caseId);
        if (!cancelled) setDetail(caseDetail);
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Unknown error');
      }
    }
    bootstrap();
    return () => {
      cancelled = true;
    };
  }, []);

  async function handleRespond(
    decisionValue: 'approve' | 'reject' | 'defer' | 'more_evidence',
    reason: string,
  ) {
    if (!detail?.decision || responding) return;
    const topBlocker = detail.decision.blockers[0];
    if (!topBlocker) return;
    // The decision card shows blockers; the corresponding open staff task
    // that actually accepts a response is a Review raised against the same
    // rule. Find it by rule_id (stable) rather than by position.
    const review = detail.reviews.find(
      (r) => r.rule_id === topBlocker.rule_id && r.status === 'open',
    );
    if (!review) {
      setError('No open review found for this blocker — it may already be resolved.');
      return;
    }
    setResponding(true);
    try {
      const updated = await respondToReview(review.id, { decision: decisionValue, reason });
      setDetail(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setResponding(false);
    }
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[var(--color-canvas)] p-6">
        <div className="mx-auto max-w-2xl rounded-[var(--radius-md)] border border-[var(--color-danger)] bg-[var(--color-danger-bg)] p-4 text-sm text-[var(--color-danger)]">
          {error}
        </div>
      </div>
    );
  }

  if (!detail) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[var(--color-canvas)]">
        <p className="text-sm text-[var(--color-muted)]">Loading demo case…</p>
      </div>
    );
  }

  const { case: theCase, evidence, claims, decision, timeline } = detail;
  const uiDecision = toUiDecision(decision);
  const uiEvidence = toEvidenceItems(evidence, claims);
  const uiTimeline = toUiTimeline(timeline);

  return (
    <Shell title={theCase.title} subtitle={`${theCase.property_ref} · ${theCase.category}`}>
      {uiDecision ? (
        <DecisionCard
          decision={uiDecision}
          caseTitle={theCase.title}
          propertyRef={theCase.property_ref}
          onRespond={handleRespond}
        />
      ) : (
        <p className="text-sm text-[var(--color-muted)]">
          No assessment recorded for this case yet.
        </p>
      )}

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <section className="flex flex-col gap-3">
          <h2 className="text-sm font-semibold text-[var(--color-ink)]">Conversation</h2>
          <ConversationThread evidence={uiEvidence} />
        </section>
        <section className="flex flex-col gap-3">
          <h2 className="text-sm font-semibold text-[var(--color-ink)]">Evidence</h2>
          <EvidencePanel evidence={uiEvidence} />
        </section>
      </div>

      <section className="flex flex-col gap-3">
        <h2 className="text-sm font-semibold text-[var(--color-ink)]">Activity</h2>
        <ActivityTimeline events={uiTimeline} />
      </section>
    </Shell>
  );
}

export default App;
