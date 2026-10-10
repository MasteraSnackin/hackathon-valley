import type { ReactNode } from 'react';
import type { CaseListItem } from '../lib/types';
import { policyLabel } from '../lib/policies';

export const button = 'min-h-11 rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-2 text-sm font-medium text-[var(--color-ink)] hover:bg-[var(--color-canvas)] disabled:cursor-not-allowed disabled:opacity-50';
export const primary = 'min-h-11 rounded-[var(--radius-sm)] bg-[var(--color-primary)] px-4 py-2 text-sm font-semibold text-white hover:bg-[var(--color-primary-hover)] disabled:cursor-not-allowed disabled:opacity-50';
export const input = 'min-h-11 w-full min-w-0 rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] px-3 py-2 text-sm text-[var(--color-ink)]';
export const card = 'min-w-0 rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-surface)] p-4 sm:p-6';
export const muted = 'text-sm text-[var(--color-muted)]';
export function Badge({ children, tone = 'quiet' }: { children: ReactNode; tone?: 'quiet' | 'attention' | 'danger' | 'success' }) {
  const colour = tone === 'danger' ? 'bg-[var(--color-danger-bg)] text-[var(--color-danger)]' : tone === 'attention' ? 'bg-[var(--color-attention-bg)] text-[var(--color-attention)]' : tone === 'success' ? 'bg-[var(--color-success-bg)] text-[var(--color-success)]' : 'bg-[var(--color-information-bg)] text-[var(--color-information)]';
  return <span className={`inline-block max-w-full break-words rounded-full px-2.5 py-1 text-xs font-medium ${colour}`}>{children}</span>;
}

export function StatusBadge({ status }: { status: string }) {
  return <Badge tone={['CONFLICT', 'FAIL', 'STOP ACTION'].includes(status) ? 'danger' : ['UNKNOWN', 'HUMAN REVIEW', 'CLARIFY', 'WAIT'].includes(status) ? 'attention' : status === 'PASS' ? 'success' : 'quiet'}>{policyLabel(status)}</Badge>;
}

export function Empty({ children }: { children: ReactNode }) {
  return <p className="rounded-[var(--radius-sm)] border border-dashed border-[var(--color-border)] bg-[var(--color-canvas)] p-4 text-sm text-[var(--color-muted)]">{children}</p>;
}

export function Field({ label, children, hint }: { label: string; children: ReactNode; hint?: string }) {
  return <label className="block min-w-0 space-y-1.5 text-sm font-medium"><span>{label}</span>{children}{hint && <span className="block text-xs font-normal text-[var(--color-muted)]">{hint}</span>}</label>;
}

export function CaseSelection({ cases, ids, onChange, disabled = false, label = 'Cases to include' }: { cases: CaseListItem[]; ids: string[]; onChange: (ids: string[]) => void; disabled?: boolean; label?: string }) {
  return <fieldset disabled={disabled} className="min-w-0"><legend className="mb-2 text-sm font-medium">{label}</legend>
    {!cases.length ? <Empty>No cases are loaded. Use Cases to create or explicitly load a BUILD example.</Empty> : <div className="max-h-64 space-y-1 overflow-y-auto rounded-[var(--radius-sm)] border border-[var(--color-border)] p-2">{cases.map((item) => <label key={item.id} className="flex min-h-11 cursor-pointer items-start gap-3 rounded p-2 hover:bg-[var(--color-canvas)]">
      <input type="checkbox" className="mt-1 h-5 w-5 shrink-0 accent-[var(--color-primary)]" checked={ids.includes(item.id)} onChange={(event) => onChange(event.target.checked ? [...ids, item.id] : ids.filter((id) => id !== item.id))} />
      <span className="min-w-0 break-words text-sm"><span className="block font-medium">{item.title}</span><span className="block text-xs text-[var(--color-muted)]">{item.property_ref || 'Property unconfirmed'} · {item.id}</span></span>
    </label>)}</div>}
  </fieldset>;
}

export function CaseLinks({ ids, cases, onSelectCase }: { ids: string[]; cases: CaseListItem[]; onSelectCase: (id: string) => void }) {
  return <ul className="space-y-1">{ids.map((id) => <li key={id} className="min-w-0"><button type="button" onClick={() => onSelectCase(id)} className="min-h-11 break-words text-left text-sm text-[var(--color-primary)] underline underline-offset-4">{cases.find((item) => item.id === id)?.title || id}</button></li>)}</ul>;
}
