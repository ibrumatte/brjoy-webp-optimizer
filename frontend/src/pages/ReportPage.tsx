import { useMemo, useState } from 'react'
import type { HistoryEntry, LocaleCode, ReportSummary } from '../types'
import { t } from '../utils/i18n'

type ReportPageProps = {
  locale: LocaleCode
  reports: ReportSummary[]
  historyEntries: HistoryEntry[]
  selectedReportId: string | null
  preview: string
  onRefresh: () => void
  onClearHistory: () => void
  onSelectReport: (id: string) => void
  onOpenReport: (id: string, kind: 'html' | 'ai' | 'csv' | 'folder') => void
}

export function ReportPage({
  locale,
  reports,
  historyEntries,
  selectedReportId,
  preview,
  onRefresh,
  onClearHistory,
  onSelectReport,
  onOpenReport,
}: ReportPageProps) {
  const [search, setSearch] = useState('')
  const [date, setDate] = useState('')

  const selected = useMemo(() => reports.find((report) => report.id === selectedReportId) ?? null, [reports, selectedReportId])
  const filteredReports = useMemo(() => {
    const needle = search.trim().toLowerCase()
    return reports.filter((report) => {
      const generated = String(report.generated_at || report.generatedAt || '')
      const sources = report.source_folders || report.sourceFolders || []
      const haystack = `${report.id} ${generated} ${sources.join(' ')}`.toLowerCase()
      const matchesSearch = !needle || haystack.includes(needle)
      const matchesDate = !date || generated.startsWith(date)
      return matchesSearch && matchesDate
    })
  }, [reports, search, date])

  return (
    <div className="grid h-full grid-cols-[460px_minmax(0,1fr)] gap-5 p-6">
      <section className="flex min-h-0 flex-col rounded-2xl border border-border bg-surface-card shadow-soft">
        <div className="flex items-center justify-between border-b border-border px-5 py-4">
          <h2 className="text-lg font-semibold text-text-primary">{t(locale, 'labels.reports')}</h2>
          <div className="flex gap-2">
            <button onClick={onClearHistory} className="rounded-xl border border-border bg-white px-3 py-2 text-sm font-semibold text-text-primary">
              {t(locale, 'actions.clearHistory')}
            </button>
            <button onClick={onRefresh} className="rounded-xl border border-border bg-white px-3 py-2 text-sm font-semibold text-text-primary">
              {t(locale, 'actions.refresh')}
            </button>
          </div>
        </div>
        <div className="grid grid-cols-[minmax(0,1fr)_160px] gap-2 px-4 pt-4">
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={t(locale, 'reports.searchPlaceholder')}
            className="rounded-xl border border-border bg-white px-3 py-2 text-sm"
          />
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="rounded-xl border border-border bg-white px-3 py-2 text-sm"
          />
        </div>
        <div className="table-scroll min-h-0 flex-1 overflow-auto p-4">
          {filteredReports.length === 0 ? (
            <div className="mt-16 text-center text-text-secondary">{t(locale, 'state.noReports')}</div>
          ) : (
            <div className="space-y-2">
              {filteredReports.map((report) => {
                const isSelected = report.id === selectedReportId
                const date = report.generated_at || report.generatedAt || ''
                const sources = report.source_folders || report.sourceFolders || []
                const sourceText = locale === 'en-US'
                  ? (sources.length > 1 ? `${sources.length} folders` : (sources[0] || 'no source'))
                  : (sources.length > 1 ? `${sources.length} pastas` : (sources[0] || 'sem origem'))
                const resultText = locale === 'en-US'
                  ? `${report.success}/${report.total} ok • ${report.errors} errors`
                  : `${report.success}/${report.total} ok • ${report.errors} erros`
                return (
                  <button
                    key={report.id}
                    onClick={() => onSelectReport(report.id)}
                    className={`w-full rounded-xl border px-3 py-3 text-left ${isSelected ? 'border-brand-blue500 bg-blue-50' : 'border-border bg-white hover:bg-slate-50'}`}
                  >
                    <div className="text-sm font-semibold text-text-primary">{date || report.id}</div>
                    <div className="mt-1 text-xs text-text-secondary">{sourceText}</div>
                    <div className="mt-1 text-xs text-text-secondary">{resultText}</div>
                  </button>
                )
              })}
            </div>
          )}
        </div>
        <div className="border-t border-border p-4">
          <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-text-secondary">{t(locale, 'labels.history')}</h3>
          <div className="max-h-32 space-y-1 overflow-auto rounded-xl border border-border bg-slate-50 p-2 text-xs text-text-secondary">
            {historyEntries.length === 0 ? (
              <div className="px-1 py-1">{t(locale, 'state.emptyHistory')}</div>
            ) : (
              historyEntries.slice(0, 20).map((entry, idx) => (
                <div key={`${entry.raw}-${idx}`} className="rounded-md bg-white px-2 py-1">
                  {entry.raw}
                </div>
              ))
            )}
          </div>
        </div>
      </section>

      <section className="flex min-h-0 flex-col rounded-2xl border border-border bg-surface-card shadow-soft">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-border px-5 py-4">
          <h2 className="text-lg font-semibold text-text-primary">{t(locale, 'report.preview')}</h2>
          <div className="flex gap-2">
            <button disabled={!selected} onClick={() => selected && onOpenReport(selected.id, 'html')} className="rounded-xl border border-border bg-white px-3 py-2 text-sm font-semibold disabled:opacity-50">{t(locale, 'report.openHtml')}</button>
            <button disabled={!selected} onClick={() => selected && onOpenReport(selected.id, 'ai')} className="rounded-xl border border-border bg-white px-3 py-2 text-sm font-semibold disabled:opacity-50">{t(locale, 'report.openAi')}</button>
            <button disabled={!selected} onClick={() => selected && onOpenReport(selected.id, 'csv')} className="rounded-xl border border-border bg-white px-3 py-2 text-sm font-semibold disabled:opacity-50">{t(locale, 'report.openCsv')}</button>
            <button disabled={!selected} onClick={() => selected && onOpenReport(selected.id, 'folder')} className="rounded-xl border border-border bg-white px-3 py-2 text-sm font-semibold disabled:opacity-50">{t(locale, 'report.openFolder')}</button>
          </div>
        </div>
        <pre className="side-scroll min-h-0 flex-1 overflow-auto whitespace-pre-wrap bg-slate-950/95 p-5 text-xs leading-5 text-slate-100">
          {preview || t(locale, 'state.selectReport')}
        </pre>
      </section>
    </div>
  )
}
