import { useCallback, useEffect, useRef, useState } from 'react';
import type { CaseListItem } from '../lib/types';
import type { Portfolio } from '../lib/portfolio-api';
import { dateLabel, errorText, getPortfolio } from '../lib/portfolio-api';
import { policyLabel } from '../lib/policies';
import { CaseInsightsPanel, PolicyComparisonPanel } from './CaseInsightsPanels';
import { HistoryPanel, IncidentsPanel, PlanningPanel } from './PortfolioOperations';
import { Badge, Empty, Field, button, input, muted } from './PortfolioShared';

export interface PortfolioWorkspaceProps {
  cases: CaseListItem[];
  selectedCaseId: string | null;
  sessionRole: string;
  onSelectCase: (id: string) => void;
  onOpenPolicies?: () => void;
}

const sections = [
  ['incidents', 'Related incidents'], ['evidence', 'Evidence comparison'], ['planning', 'Visit planning'],
  ['history', 'Property history'], ['playback', 'Case playback'], ['comparison', 'Policy comparison'],
] as const;
type Section = typeof sections[number][0];

/** Reading this workspace never imports cases, changes roles or seeds decisions. */
export default function PortfolioWorkspace({ cases, selectedCaseId, sessionRole, onSelectCase, onOpenPolicies }: PortfolioWorkspaceProps) {
  const [section, setSection] = useState<Section>('incidents');
  const [visited, setVisited] = useState<Section[]>(['incidents']);
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [busy, setBusy] = useState('load');
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [loadedAt, setLoadedAt] = useState('');
  const [reload, setReload] = useState(0);
  const [chosenCase, setChosenCase] = useState(selectedCaseId || '');
  const mutationInProgress = useRef(false);
  const mounted = useRef(true);
  const requestId = useRef(0);
  const canManage = sessionRole === 'case_manager';
  const caseId = cases.some((item) => item.id === chosenCase) ? chosenCase : '';
  const caseRevisions = cases.map((item) => `${item.id}:${item.revision}`).join('|');
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  useEffect(() => {
    // The parent selection changes only when staff explicitly choose a case.
    // oxlint-disable-next-line react/set-state-in-effect
    setChosenCase(selectedCaseId || '');
  }, [selectedCaseId]);
  useEffect(() => {
    if (mutationInProgress.current) return;
    const controller = new AbortController();
    const id = ++requestId.current;
    getPortfolio(controller.signal).then((data) => {
      if (!controller.signal.aborted && id === requestId.current) { setPortfolio(data); setBusy(''); setError(''); setLoadedAt(new Date().toISOString()); }
    }).catch((failure) => { if (!controller.signal.aborted && id === requestId.current) { setBusy(''); setError(errorText(failure)); } });
    return () => controller.abort();
  }, [reload, sessionRole, caseRevisions]);

  const mutate = useCallback(async (work: () => Promise<unknown>, success: string): Promise<boolean> => {
    if (mutationInProgress.current || !canManage) return false;
    mutationInProgress.current = true;
    const id = ++requestId.current;
    setBusy('save'); setError(''); setNotice('');
    let saved = false;
    try {
      await work(); saved = true;
      if (mounted.current) setNotice(success);
      const next = await getPortfolio();
      if (mounted.current && id === requestId.current) { setPortfolio(next); setLoadedAt(new Date().toISOString()); }
    } catch (failure) {
      if (mounted.current) setError(`${saved ? 'The change was saved, but refreshing failed. Do not submit it again; refresh the workspace. ' : ''}${errorText(failure)}`);
    } finally {
      mutationInProgress.current = false;
      if (mounted.current) setBusy('');
    }
    return saved;
  }, [canManage]);
  const operationsProps = { cases, busy: !!busy, canManage, mutate, onSelectCase };
  return <div className="mx-auto w-full min-w-0 max-w-[1320px] space-y-5 px-3 py-5 sm:px-6 sm:py-6">
    <div className="flex flex-wrap items-start justify-between gap-3"><div className="min-w-0"><h1 className="text-2xl font-bold tracking-tight">Portfolio workspace</h1><p className={`${muted} mt-1 max-w-3xl`}>Connect related reports, inspect disagreements and plan the next step. Individual case permissions and evidence remain separate.</p></div><Badge>{policyLabel(sessionRole || 'No staff session')}</Badge></div>
    <nav aria-label="Portfolio tools" className="grid grid-cols-2 gap-2 rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-surface)] p-2 sm:grid-cols-3 xl:grid-cols-6">{sections.map(([key, label]) => <button key={key} type="button" aria-current={section === key ? 'page' : undefined} className={`min-h-11 rounded-[var(--radius-sm)] px-3 py-2 text-sm font-medium ${section === key ? 'bg-[var(--color-primary)] text-white' : 'text-[var(--color-muted)] hover:bg-[var(--color-canvas)]'}`} onClick={() => { setSection(key); setVisited((current) => current.includes(key) ? current : [...current, key]); }}>{label}</button>)}</nav>
    <div className="flex flex-wrap items-center justify-between gap-3"><p className={muted}>{loadedAt ? `Portfolio snapshot loaded ${dateLabel(loadedAt)}.` : 'Loading the portfolio snapshot.'} Refresh before relying on a tentative plan.</p><button type="button" className={button} disabled={!!busy} onClick={() => { setBusy('load'); setError(''); setReload((value) => value + 1); }}>{busy === 'load' ? 'Loading…' : 'Refresh workspace'}</button></div>
    {error && <p role="alert" className="break-words rounded-[var(--radius-sm)] border border-[var(--color-danger)] bg-[var(--color-danger-bg)] p-4 text-sm text-[var(--color-danger)]">{error}</p>}
    {notice && <p role="status" className="rounded-[var(--radius-sm)] bg-[var(--color-success-bg)] p-4 text-sm text-[var(--color-success)]">{notice}</p>}
    {busy === 'save' && <p role="status" className={muted}>Saving the staff decision…</p>}
    {!canManage && ['incidents', 'planning'].includes(section) && <p className="rounded-[var(--radius-sm)] bg-[var(--color-information-bg)] p-3 text-sm text-[var(--color-information)]">Your role can read these records. Use the property manager role to change profiles, incidents or tentative plans.</p>}
    {(section === 'evidence' || section === 'playback') && <div className="rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-surface)] p-4"><Field label="Choose a case from the current queue"><select className={input} value={caseId} onChange={(event) => setChosenCase(event.target.value)}><option value="">Choose a case</option>{cases.map((item) => <option key={item.id} value={item.id}>{item.title}</option>)}</select></Field>{section === 'playback' && <p className={`${muted} mt-2`}>This selector uses current queue titles for navigation only. Historical frames below use recorded information exclusively.</p>}</div>}
    {portfolio && <>
      <div hidden={section !== 'incidents'}><IncidentsPanel {...operationsProps} portfolio={portfolio} selectedCaseId={caseId || null} onChooseCase={setChosenCase} /></div>
      {visited.includes('planning') && <div hidden={section !== 'planning'}><PlanningPanel {...operationsProps} portfolio={portfolio} /></div>}
      {visited.includes('history') && <div hidden={section !== 'history'}><HistoryPanel {...operationsProps} portfolio={portfolio} /></div>}
    </>}
    {(section === 'evidence' || section === 'playback') && (caseId ? <CaseInsightsPanel key={`${caseId}:${section}`} caseId={caseId} mode={section} /> : <Empty>Select a case to inspect its {section === 'evidence' ? 'source evidence' : 'recorded decisions'}.</Empty>)}
    {visited.includes('comparison') && <div hidden={section !== 'comparison'}><PolicyComparisonPanel cases={cases} sessionRole={sessionRole} onSelectCase={onSelectCase} onOpenPolicies={onOpenPolicies} /></div>}
    {!portfolio && !busy && ['incidents', 'planning', 'history'].includes(section) && <Empty>The portfolio snapshot is unavailable. Refresh the workspace to retry.</Empty>}
  </div>;
}
