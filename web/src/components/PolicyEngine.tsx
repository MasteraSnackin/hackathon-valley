import { useCallback, useEffect, useState } from 'react';
import {
  draftAndPreviewPolicy,
  getPolicies,
  interpretPolicy,
  publishPolicy,
} from '../lib/api';
import {
  describePolicy,
  draftFrom,
  thresholdChanges,
  thresholdsOf,
  type PolicyCardVM,
  type PolicyCategory,
  type Thresholds,
} from '../lib/policies';
import type {
  AssistantResult,
  PoliciesResponse,
  PolicyDraft,
  PolicyInput,
  PolicyPreview,
} from '../lib/types';

/** Text handed over from a case decision ("Add this as a policy?"). The nonce
 * makes the same text re-trigger interpretation. */
export interface PolicyRequest {
  text: string;
  reviewId?: string;
  nonce: number;
}

interface PolicyEngineProps {
  request: PolicyRequest | null;
  /** Called after publication so the dashboard can refresh reassessed cases. */
  onPublished: () => void;
}

/** A proposed change waiting for impact preview and publication. */
interface Pending {
  input: PolicyInput;
  summary: string;
  warnings: string[];
}

/** Category tag colour, drawn from the existing semantic status tokens. */
const CATEGORY_STYLE: Record<PolicyCategory, { bg: string; text: string }> = {
  Cost: { bg: 'var(--color-information-bg)', text: 'var(--color-information)' },
  Escalation: { bg: 'var(--color-attention-bg)', text: 'var(--color-attention)' },
  Access: { bg: 'var(--color-danger-bg)', text: 'var(--color-danger)' },
  Comms: { bg: '#EEF1EE', text: 'var(--color-muted)' },
  Routing: { bg: 'var(--color-success-bg)', text: 'var(--color-success)' },
  Rule: { bg: 'var(--color-attention-bg)', text: 'var(--color-attention)' },
};

const PRIMARY_BTN =
  'rounded-[var(--radius-sm)] bg-[var(--color-primary)] px-4 py-2 text-[13px] font-semibold text-white transition-colors hover:bg-[var(--color-primary-hover)] disabled:opacity-50';
const SECONDARY_BTN =
  'rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-transparent px-4 py-2 text-[13px] font-medium text-[var(--color-ink)] transition-colors hover:bg-[var(--color-canvas)] disabled:opacity-50';

function Tag({ category }: { category: PolicyCategory }) {
  const s = CATEGORY_STYLE[category];
  return (
    <span
      className="rounded-full px-2.5 py-0.5 text-[11px] font-medium"
      style={{ background: s.bg, color: s.text }}
    >
      {category}
    </span>
  );
}

function PolicyCard({
  policy,
  onRemove,
  disabled,
}: {
  policy: PolicyCardVM;
  onRemove?: () => void;
  disabled: boolean;
}) {
  return (
    <div className="flex flex-col gap-3 rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
      <div className="flex items-start justify-between gap-3">
        <div className="flex flex-wrap items-center gap-2">
          <Tag category={policy.category} />
          {policy.threshold && (
            <span
              className="rounded-full border px-2 py-0.5 text-[11px] font-medium"
              style={{
                borderColor: 'var(--color-border)',
                color: 'var(--color-ink)',
                fontVariantNumeric: 'tabular-nums',
              }}
            >
              {policy.threshold}
            </span>
          )}
        </div>
        {onRemove && (
          <button
            type="button"
            onClick={onRemove}
            disabled={disabled}
            className="text-[11px] font-medium text-[var(--color-danger)] hover:underline disabled:opacity-50"
          >
            Remove
          </button>
        )}
      </div>
      <p className="text-[13px] leading-relaxed text-[var(--color-ink)]">{policy.text}</p>
      <div className="flex items-center gap-1.5">
        <span
          className="h-1.5 w-1.5 rounded-full"
          style={{
            background:
              policy.source === 'AI-drafted rule' ? 'var(--color-information)' : 'var(--color-muted)',
          }}
        />
        <span className="text-[11px] text-[var(--color-muted)]">{policy.source}</span>
      </div>
    </div>
  );
}

interface SliderRowProps {
  label: string;
  min: number;
  max: number;
  step: number;
  value: number;
  display: string;
  onChange: (v: number) => void;
}

function SliderRow({ label, min, max, step, value, display, onChange }: SliderRowProps) {
  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-baseline justify-between">
        <label className="text-[13px] text-[var(--color-ink)]">{label}</label>
        <span
          className="text-[13px] font-semibold text-[var(--color-primary)]"
          style={{ fontVariantNumeric: 'tabular-nums' }}
        >
          {display}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full accent-[var(--color-primary)]"
      />
    </div>
  );
}

function AssistantPanel({ result }: { result: AssistantResult }) {
  const tone =
    result.status === 'ready'
      ? { bg: 'var(--color-success-bg)', text: 'var(--color-success)', label: 'Draft ready' }
      : result.status === 'clarification'
        ? { bg: 'var(--color-attention-bg)', text: 'var(--color-attention)', label: 'Needs detail' }
        : { bg: 'var(--color-danger-bg)', text: 'var(--color-danger)', label: 'Not supported' };
  return (
    <div className="rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] p-4">
      <span
        className="rounded-full px-2.5 py-0.5 text-[11px] font-semibold"
        style={{ background: tone.bg, color: tone.text }}
      >
        {tone.label}
      </span>
      <p className="mt-2 text-[13px] text-[var(--color-ink)]">{result.summary}</p>
      {result.questions.length > 0 && (
        <ul className="mt-2 list-disc pl-5 text-[12px] text-[var(--color-attention)]">
          {result.questions.map((q) => (
            <li key={q}>{q}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default function PolicyEngine({ request, onPublished }: PolicyEngineProps) {
  const [policies, setPolicies] = useState<PoliciesResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [text, setText] = useState('');
  const [assistant, setAssistant] = useState<AssistantResult | null>(null);
  const [pending, setPending] = useState<Pending | null>(null);
  const [preview, setPreview] = useState<{ draft: PolicyDraft; preview: PolicyPreview } | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [thresholds, setThresholds] = useState<Thresholds | null>(null);

  const load = useCallback(async () => {
    const result = await getPolicies();
    setPolicies(result);
    setThresholds(thresholdsOf(result.active.settings));
    return result;
  }, []);

  useEffect(() => {
    load().catch((err) => setError(err instanceof Error ? err.message : 'Could not load policy'));
  }, [load]);

  function propose(next: Pending) {
    setPending(next);
    setPreview(null);
    setNotice(null);
    setError(null);
  }

  const interpret = useCallback(async (value: string, reviewId?: string) => {
    if (!value.trim()) return;
    setBusy(true);
    setError(null);
    setNotice(null);
    try {
      const result = await interpretPolicy(value.trim(), reviewId);
      setAssistant(result);
      if (result.status === 'ready' && result.draft) {
        setPending({ input: result.draft, summary: result.summary, warnings: result.warnings });
        setPreview(null);
      } else {
        setPending(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not interpret this policy');
    } finally {
      setBusy(false);
    }
  }, []);

  // A decision on a case can hand over suggested policy text.
  useEffect(() => {
    if (!request) return;
    setText(request.text);
    void interpret(request.text, request.reviewId);
  }, [request, interpret]);

  async function runPreview() {
    if (!pending) return;
    setBusy(true);
    setError(null);
    try {
      setPreview(await draftAndPreviewPolicy(pending.input));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not preview this draft');
    } finally {
      setBusy(false);
    }
  }

  async function publish() {
    if (!preview) return;
    setBusy(true);
    setError(null);
    try {
      await publishPolicy(preview.draft.id);
      const fresh = await load();
      setNotice(
        `Version ${fresh.active.version} is live. The workflow is reassessing every open case under it.`,
      );
      setPending(null);
      setPreview(null);
      setAssistant(null);
      setText('');
      onPublished();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not publish this draft');
    } finally {
      setBusy(false);
    }
  }

  if (!policies || !thresholds) {
    return (
      <div className="mx-auto w-full max-w-[860px] px-6 py-8 text-sm text-[var(--color-muted)]">
        {error ?? 'Loading policy…'}
      </div>
    );
  }

  const active = policies.active;
  const cards = describePolicy(active);
  const staged = thresholdChanges(thresholdsOf(active.settings), thresholds);
  const changed = preview?.preview.affected.filter((a) => a.changed) ?? [];

  return (
    <div className="mx-auto flex w-full max-w-[860px] flex-col gap-8 px-6 py-8">
      {/* Add policy */}
      <section className="flex flex-col gap-3">
        <div>
          <div className="flex items-baseline justify-between">
            <h1 className="text-[22px] font-bold tracking-[-0.4px] text-[var(--color-ink)]">
              Policy engine
            </h1>
            <span className="text-[12px] text-[var(--color-muted)]">
              Active version {active.version} · {active.reason}
            </span>
          </div>
          <p className="text-[13px] text-[var(--color-muted)]">
            Rules the workflow checks before it acts. Describe a change in plain English; it becomes
            a draft you preview against every live case before publishing. Policy can add
            safeguards but never creates authority on its own.
          </p>
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') void interpret(text);
            }}
            placeholder="e.g. Require human review for spending over £250"
            className="flex-1 rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] px-3.5 py-2.5 text-[13px] text-[var(--color-ink)] outline-none placeholder:text-[var(--color-muted)] focus:border-[var(--color-primary)]"
          />
          <button
            type="button"
            onClick={() => void interpret(text)}
            disabled={!text.trim() || busy}
            className="rounded-[var(--radius-sm)] bg-[var(--color-primary)] px-5 py-2.5 text-[13px] font-semibold text-white transition-colors hover:bg-[var(--color-primary-hover)] disabled:opacity-50"
          >
            Draft
          </button>
        </div>
        {assistant && <AssistantPanel result={assistant} />}
      </section>

      {error && (
        <div className="rounded-[var(--radius-md)] border border-[var(--color-danger)] bg-[var(--color-danger-bg)] px-4 py-3 text-sm text-[var(--color-danger)]">
          {error}
        </div>
      )}
      {notice && (
        <div className="rounded-[var(--radius-md)] border border-[var(--color-success)] bg-[var(--color-success-bg)] px-4 py-3 text-sm text-[var(--color-success)]">
          {notice}
        </div>
      )}

      {/* Pending change: preview, then publish */}
      {pending && (
        <section
          className="flex flex-col gap-3 rounded-[var(--radius-md)] border p-5"
          style={{ borderColor: 'var(--color-attention)', background: 'var(--color-attention-bg)' }}
        >
          <p className="text-[11px] font-bold uppercase tracking-wide text-[var(--color-attention)]">
            Proposed change · version {active.version + 1}
          </p>
          <p className="text-[14px] font-semibold text-[var(--color-ink)]">{pending.summary}</p>
          {pending.warnings.length > 0 && (
            <ul className="list-disc pl-5 text-[12px] text-[var(--color-ink)]/80">
              {pending.warnings.map((w) => (
                <li key={w}>{w}</li>
              ))}
            </ul>
          )}
          {preview && (
            <div className="rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] p-3 text-[12px]">
              <p className="font-semibold text-[var(--color-ink)]">
                Impact: {changed.length} of {preview.preview.affected.length} live cases change
              </p>
              {changed.length > 0 && (
                <ul className="mt-1.5 flex flex-col gap-1">
                  {changed.map((a) => (
                    <li key={a.case_id} className="flex justify-between gap-3 text-[var(--color-muted)]">
                      <span className="truncate">{a.title}</span>
                      <span className="shrink-0 text-[var(--color-ink)]">
                        {a.before} → {a.after}
                      </span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
          <div className="flex gap-2">
            {preview ? (
              <button type="button" onClick={() => void publish()} disabled={busy} className={PRIMARY_BTN}>
                Publish version {active.version + 1}
              </button>
            ) : (
              <button type="button" onClick={() => void runPreview()} disabled={busy} className={PRIMARY_BTN}>
                Preview impact
              </button>
            )}
            <button
              type="button"
              onClick={() => {
                setPending(null);
                setPreview(null);
                setThresholds(thresholdsOf(active.settings));
              }}
              disabled={busy}
              className={SECONDARY_BTN}
            >
              Discard
            </button>
          </div>
          <p className="text-[11px] text-[var(--color-muted)]">
            Saving, previewing and publishing act as the policy editor demo role.
          </p>
        </section>
      )}

      {/* Policy list */}
      <section className="flex flex-col gap-3">
        <h2 className="text-[11px] font-semibold uppercase tracking-wide text-[var(--color-muted)]">
          Active policy · {active.rules.length} custom {active.rules.length === 1 ? 'rule' : 'rules'}{' '}
          on top of the built-in checks
        </h2>
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
          {cards.map((p) => (
            <PolicyCard
              key={p.id}
              policy={p}
              disabled={busy}
              onRemove={
                p.ruleId
                  ? () =>
                      propose({
                        input: draftFrom(
                          active,
                          { rules: active.rules.filter((r) => r.id !== p.ruleId) },
                          'Rule removed via staff dashboard',
                        ),
                        summary: `Remove rule: ${p.text}`,
                        warnings: [],
                      })
                  : undefined
              }
            />
          ))}
        </div>
      </section>

      {/* Thresholds */}
      <section className="flex flex-col gap-4">
        <h2 className="text-[11px] font-semibold uppercase tracking-wide text-[var(--color-muted)]">
          Thresholds
        </h2>
        <div className="flex flex-col gap-5 rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5">
          <SliderRow
            label="Financial review above"
            min={0}
            max={2000}
            step={10}
            value={thresholds.review_limit}
            display={`£${thresholds.review_limit.toLocaleString('en-GB')}`}
            onChange={(v) => setThresholds({ ...thresholds, review_limit: v })}
          />
          <SliderRow
            label="Remind after no reply"
            min={1}
            max={48}
            step={1}
            value={thresholds.reminder_hours}
            display={`${thresholds.reminder_hours} working h`}
            onChange={(v) => setThresholds({ ...thresholds, reminder_hours: v })}
          />
          <SliderRow
            label="Escalate to a person after"
            min={2}
            max={96}
            step={1}
            value={thresholds.escalation_hours}
            display={`${thresholds.escalation_hours} working h`}
            onChange={(v) => setThresholds({ ...thresholds, escalation_hours: v })}
          />
          <SliderRow
            label="Reminders per question"
            min={0}
            max={5}
            step={1}
            value={thresholds.reminder_limit}
            display={`${thresholds.reminder_limit}`}
            onChange={(v) => setThresholds({ ...thresholds, reminder_limit: v })}
          />
          <div className="flex items-center justify-between gap-3">
            <p className="text-[12px] text-[var(--color-muted)]">
              {staged.length ? staged.join(' · ') : 'Move a slider to stage a change.'}
            </p>
            <button
              type="button"
              disabled={!staged.length || busy}
              onClick={() =>
                propose({
                  input: draftFrom(active, { settings: thresholds }, 'Threshold change via staff dashboard'),
                  summary: staged.join('; ') + '.',
                  warnings: ['These settings apply to every case under the active policy.'],
                })
              }
              className={PRIMARY_BTN}
            >
              Stage changes
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
