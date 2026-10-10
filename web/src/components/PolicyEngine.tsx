import { useState } from 'react';
import type { Policy, PolicyCategory, Thresholds } from '../lib/policies';

interface PolicyEngineProps {
  policies: Policy[];
  onAdd: (text: string) => void;
  onToggle: (id: string) => void;
  thresholds: Thresholds;
  onThresholdChange: (patch: Partial<Thresholds>) => void;
}

/** Category tag colour, drawn from the existing semantic status tokens. */
const CATEGORY_STYLE: Record<PolicyCategory, { bg: string; text: string }> = {
  Urgency: { bg: 'var(--color-danger-bg)', text: 'var(--color-danger)' },
  Cost: { bg: 'var(--color-information-bg)', text: 'var(--color-information)' },
  Escalation: { bg: 'var(--color-attention-bg)', text: 'var(--color-attention)' },
  Contractor: { bg: 'var(--color-success-bg)', text: 'var(--color-success)' },
  Comms: { bg: '#EEF1EE', text: 'var(--color-muted)' },
};

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

function Toggle({ on, onClick }: { on: boolean; onClick: () => void }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={on}
      onClick={onClick}
      className="relative h-[20px] w-[36px] shrink-0 rounded-full transition-colors"
      style={{ background: on ? 'var(--color-primary)' : 'var(--color-border)' }}
    >
      <span
        className="absolute top-[2px] h-4 w-4 rounded-full bg-white transition-all"
        style={{ left: on ? '18px' : '2px' }}
      />
    </button>
  );
}

function PolicyCard({ policy, onToggle }: { policy: Policy; onToggle: (id: string) => void }) {
  return (
    <div
      className="flex flex-col gap-3 rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] p-4"
      style={{ opacity: policy.enabled ? 1 : 0.6 }}
    >
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
        <Toggle on={policy.enabled} onClick={() => onToggle(policy.id)} />
      </div>
      <p className="text-[13px] leading-relaxed text-[var(--color-ink)]">{policy.text}</p>
      <div className="flex items-center gap-1.5">
        <span
          className="h-1.5 w-1.5 rounded-full"
          style={{
            background:
              policy.source === 'AI-learned' ? 'var(--color-information)' : 'var(--color-muted)',
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

function formatDuration(min: number): string {
  if (min < 60) return `${min} min`;
  const h = Math.floor(min / 60);
  const m = min % 60;
  return m === 0 ? `${h}h` : `${h}h ${m}m`;
}

export default function PolicyEngine({
  policies,
  onAdd,
  onToggle,
  thresholds,
  onThresholdChange,
}: PolicyEngineProps) {
  const [draft, setDraft] = useState('');

  function submit() {
    const text = draft.trim();
    if (!text) return;
    onAdd(text);
    setDraft('');
  }

  return (
    <div className="mx-auto flex w-full max-w-[860px] flex-col gap-8 px-6 py-8">
      {/* Add policy */}
      <section className="flex flex-col gap-3">
        <div>
          <h1 className="text-[22px] font-bold tracking-[-0.4px] text-[var(--color-ink)]">
            Policy engine
          </h1>
          <p className="text-[13px] text-[var(--color-muted)]">
            Plain-English rules the agent applies before it acts. Toggle any rule off to pause it.
          </p>
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') submit();
            }}
            placeholder="Type a policy in plain English…"
            className="flex-1 rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] px-3.5 py-2.5 text-[13px] text-[var(--color-ink)] outline-none placeholder:text-[var(--color-muted)] focus:border-[var(--color-primary)]"
          />
          <button
            type="button"
            onClick={submit}
            disabled={!draft.trim()}
            className="rounded-[var(--radius-sm)] bg-[var(--color-primary)] px-5 py-2.5 text-[13px] font-semibold text-white transition-colors hover:bg-[var(--color-primary-hover)] disabled:opacity-50"
          >
            Add
          </button>
        </div>
      </section>

      {/* Policy list */}
      <section className="flex flex-col gap-3">
        <h2 className="text-[11px] font-semibold uppercase tracking-wide text-[var(--color-muted)]">
          Active policies · {policies.filter((p) => p.enabled).length} of {policies.length} on
        </h2>
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
          {policies.map((p) => (
            <PolicyCard key={p.id} policy={p} onToggle={onToggle} />
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
            label="Emergency contractor approval limit"
            min={0}
            max={2000}
            step={50}
            value={thresholds.emergencyLimit}
            display={`£${thresholds.emergencyLimit.toLocaleString()}`}
            onChange={(v) => onThresholdChange({ emergencyLimit: v })}
          />
          <SliderRow
            label="Auto-escalate to manager after no reply"
            min={30}
            max={240}
            step={15}
            value={thresholds.escalateAfterMin}
            display={formatDuration(thresholds.escalateAfterMin)}
            onChange={(v) => onThresholdChange({ escalateAfterMin: v })}
          />
          <SliderRow
            label="Auto-ping contractor after silence"
            min={1}
            max={48}
            step={1}
            value={thresholds.pingAfterHr}
            display={`${thresholds.pingAfterHr} hr`}
            onChange={(v) => onThresholdChange({ pingAfterHr: v })}
          />
          <SliderRow
            label="Max days to resolve before escalation"
            min={1}
            max={14}
            step={1}
            value={thresholds.maxResolveDays}
            display={`${thresholds.maxResolveDays} ${thresholds.maxResolveDays === 1 ? 'day' : 'days'}`}
            onChange={(v) => onThresholdChange({ maxResolveDays: v })}
          />
        </div>
      </section>
    </div>
  );
}
