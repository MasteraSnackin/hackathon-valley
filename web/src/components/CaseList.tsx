import { useState } from 'react'
import type { CaseSummaryVM, Severity } from './dashboard-types'

interface CaseListProps {
  cases: CaseSummaryVM[]
  selectedId: string | null
  onSelect: (id: string) => void
}

const severityStyle: Record<Severity, string> = {
  red: 'border-l-[var(--color-danger)]',
  amber: 'border-l-[var(--color-attention)]',
  green: 'border-l-[var(--color-success)]',
}

function formatTimestamp(iso: string): string {
  const date = new Date(iso)
  if (Number.isNaN(date.getTime())) return 'Date unavailable'
  const minutes = Math.floor((Date.now() - date.getTime()) / 60000)
  if (minutes >= 0 && minutes < 1) return 'Just now'
  if (minutes >= 1 && minutes < 60) return `${minutes}m ago`
  if (minutes >= 60 && minutes < 1440) return `${Math.floor(minutes / 60)}h ago`
  return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
}

export function CaseList({ cases, selectedId, onSelect }: CaseListProps) {
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState('all')
  const query = search.trim().toLocaleLowerCase('en-GB')
  const priority = { red: 0, amber: 1, green: 2 }
  const filtered = cases.filter((item) => {
    const matchesText = `${item.address} ${item.issueType} ${item.stagePill}`.toLocaleLowerCase('en-GB').includes(query)
    const matchesFilter = filter === 'all' || (filter === 'open' ? item.outcome !== 'NO FURTHER ACTION' : item.outcome === 'NO FURTHER ACTION')
    return matchesText && matchesFilter
  }).sort((a, b) => priority[a.severity] - priority[b.severity] || b.timestamp.localeCompare(a.timestamp))

  return (
    <section aria-label="Case queue" className="flex h-full min-h-0 flex-col">
      <div className="flex flex-col gap-3 border-b border-[var(--color-border)] px-4 py-4">
        <div className="flex items-baseline justify-between gap-2">
          <h2 className="text-base font-semibold">Requests</h2>
          <span className="text-xs text-[var(--color-muted)]">{cases.length} total</span>
        </div>
        <label htmlFor="case-search" className="sr-only">Search requests</label>
        <input id="case-search" type="search" value={search} onChange={(event) => setSearch(event.target.value)}
          placeholder="Search property or request"
          className="w-full rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-canvas)] px-3 py-2 text-sm" />
        <label htmlFor="case-filter" className="sr-only">Filter requests</label>
        <select id="case-filter" value={filter} onChange={(event) => setFilter(event.target.value)}
          className="w-full rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-white px-3 py-2 text-sm">
          <option value="all">All requests</option>
          <option value="open">Open actions</option>
          <option value="complete">No further action</option>
        </select>
        <p className="text-xs text-[var(--color-muted)]" aria-live="polite">{filtered.length} shown · Stopped actions first</p>
      </div>
      <div className="min-h-0 flex-1 overflow-y-auto px-2 py-2">
        {filtered.length === 0 ? (
          <div className="px-2 py-5 text-sm text-[var(--color-muted)]">
            <p>{cases.length === 0 ? 'Your request queue is empty. Load demo cases to explore the workflow.' : 'No requests match these filters.'}</p>
            {(search || filter !== 'all') && <button type="button" onClick={() => { setSearch(''); setFilter('all') }} className="mt-3 font-semibold text-[var(--color-primary)] underline">Clear filters</button>}
          </div>
        ) : (
          <ul className="flex flex-col gap-2">
            {filtered.map((item) => (
              <li key={item.id}>
                <button type="button" onClick={() => onSelect(item.id)} aria-current={item.id === selectedId ? 'true' : undefined}
                  className={`flex min-h-[100px] w-full cursor-pointer flex-col justify-center gap-1.5 rounded-[var(--radius-sm)] border border-l-4 border-[var(--color-border)] px-3 py-3 text-left transition-colors ${severityStyle[item.severity]} ${item.id === selectedId ? 'bg-[var(--color-success-bg)] ring-1 ring-[var(--color-primary)]' : 'bg-white hover:bg-[var(--color-canvas)]'}`}>
                  <span className="line-clamp-2 break-words text-sm font-semibold">{item.address}</span>
                  <span className="line-clamp-2 text-xs text-[var(--color-muted)]">{item.issueType}</span>
                  <span className="flex w-full flex-wrap items-center justify-between gap-1 text-xs">
                    <span className="rounded-full bg-[var(--color-canvas)] px-2 py-1">{item.stagePill}</span>
                    <time dateTime={item.timestamp} title={new Date(item.timestamp).toLocaleString('en-GB')} className="text-[var(--color-muted)]">{formatTimestamp(item.timestamp)}</time>
                  </span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  )
}

export default CaseList
