import type { ReactNode } from 'react'

interface ShellProps {
  title: string
  subtitle?: string
  children: ReactNode
}

/** Minimal single-screen app shell: header band, centered content container. */
export default function Shell({ title, subtitle, children }: ShellProps) {
  return (
    <div className="min-h-screen bg-[var(--color-canvas)]">
      <header className="border-b border-[var(--color-border)] bg-[var(--color-surface)]">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-6 py-4">
          <span className="text-sm font-semibold text-[var(--color-ink)]">Property Desk</span>
          <span className="rounded-full bg-[var(--color-canvas)] px-2.5 py-1 text-xs text-[var(--color-muted)]">
            Local demonstration — no real actions taken
          </span>
        </div>
      </header>

      <main className="mx-auto flex max-w-4xl flex-col gap-6 px-6 py-8">
        <div className="flex flex-col gap-1">
          <h1 className="text-xl font-semibold text-[var(--color-ink)]">{title}</h1>
          {subtitle && <p className="text-sm text-[var(--color-muted)]">{subtitle}</p>}
        </div>
        {children}
      </main>
    </div>
  )
}
