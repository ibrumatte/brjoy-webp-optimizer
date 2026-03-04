import { useEffect, useMemo, useState } from 'react'
import { TopBar } from './components/TopBar'
import { ConverterPage } from './pages/ConverterPage'
import { ReportPage } from './pages/ReportPage'
import { desktopApi } from './services/desktopApi'
import { t } from './utils/i18n'
import type {
  AppBootstrap,
  ConversionConfig,
  ConversionStatus,
  FileItem,
  HistoryEntry,
  LocaleCode,
  ReportSummary,
  ThemeMode,
} from './types'

type NoticeTone = 'info' | 'success' | 'error'
type NoticeState = { message: string; tone: NoticeTone } | null

const defaultConfig: ConversionConfig = {
  formato: 'webp',
  redimensionar: false,
  largura_max: 1920,
  altura_max: null,
  recorte_1x1: false,
  qualidade: 85,
  sharpen: false,
  brightness: 100,
  batch_sizes_enabled: false,
  batch_sizes: [800, 1200, 1920],
  substituir_no_lugar: false,
  manter_estrutura: true,
  output_folder: '',
}

export default function App() {
  const [tab, setTab] = useState<'converter' | 'report'>('converter')
  const [bootstrap, setBootstrap] = useState<AppBootstrap | null>(null)
  const [locale, setLocale] = useState<LocaleCode>('pt-BR')
  const [theme, setTheme] = useState<ThemeMode>('system')
  const [systemPrefersDark, setSystemPrefersDark] = useState(false)
  const [files, setFiles] = useState<FileItem[]>([])
  const [config, setConfig] = useState<ConversionConfig>(defaultConfig)
  const [selectedPreset, setSelectedPreset] = useState('')
  const [status, setStatus] = useState<ConversionStatus | null>(null)
  const [jobId, setJobId] = useState<string | null>(null)
  const [reports, setReports] = useState<ReportSummary[]>([])
  const [selectedReportId, setSelectedReportId] = useState<string | null>(null)
  const [reportPreview, setReportPreview] = useState('')
  const [history, setHistory] = useState<HistoryEntry[]>([])
  const [dropHintKey, setDropHintKey] = useState<'drop.zoneHint' | 'drop.zoneNoPath'>('drop.zoneHint')
  const [notice, setNotice] = useState<NoticeState>(null)

  function notify(message: string, tone: NoticeTone = 'info') {
    setNotice({ message, tone })
  }

  function describeError(error: unknown): string {
    if (error instanceof Error && error.message) return error.message
    if (typeof error === 'string' && error.trim()) return error
    try {
      const value = JSON.stringify(error)
      return value === '{}' ? '' : value
    } catch {
      return ''
    }
  }

  function notifyError(key: string, error: unknown) {
    const detail = describeError(error)
    const message = detail ? `${t(locale, key)} (${detail})` : t(locale, key)
    notify(message, 'error')
  }

  useEffect(() => {
    ;(async () => {
      try {
        const data = await desktopApi.getBootstrap()
        setBootstrap(data)
        setLocale(data.preferences.locale || data.locale)
        setTheme(data.preferences.theme || 'system')
        const presetFromPrefs = data.preferences.lastPreset || ''
        setSelectedPreset(presetFromPrefs)
        if (presetFromPrefs && data.presets[presetFromPrefs]) {
          const preset = data.presets[presetFromPrefs]
          setConfig((prev) => ({
            ...prev,
            redimensionar: preset.resize,
            largura_max: preset.width,
            altura_max: preset.height,
            recorte_1x1: preset.crop,
            qualidade: preset.quality,
          }))
        }
        await Promise.all([refreshReports(), refreshHistory()])
      } catch (error) {
        notifyError('notice.bootstrapFailed', error)
      }
    })()
  }, [])

  useEffect(() => {
    if (!notice) return
    const timer = window.setTimeout(() => setNotice(null), 4000)
    return () => window.clearTimeout(timer)
  }, [notice])

  useEffect(() => {
    const media = window.matchMedia('(prefers-color-scheme: dark)')
    const sync = () => setSystemPrefersDark(media.matches)
    sync()
    if (typeof media.addEventListener === 'function') {
      media.addEventListener('change', sync)
      return () => media.removeEventListener('change', sync)
    }
    media.addListener(sync)
    return () => media.removeListener(sync)
  }, [])

  useEffect(() => {
    if (!jobId) return

    const timer = window.setInterval(async () => {
      try {
        const next = await desktopApi.getConversionStatus(jobId)
        setStatus(next)

        if (['done', 'canceled', 'error'].includes(next.phase)) {
          window.clearInterval(timer)
          setJobId(null)
          await refreshReports()
          await refreshHistory()
          if (next.reportId) {
            setTab('report')
            setSelectedReportId(next.reportId)
          }
        }
      } catch (error) {
        window.clearInterval(timer)
        setJobId(null)
        notifyError('notice.statusFailed', error)
      }
    }, 500)

    return () => window.clearInterval(timer)
  }, [jobId])

  useEffect(() => {
    if (!selectedReportId) {
      setReportPreview('')
      return
    }

    ;(async () => {
      try {
        const preview = await desktopApi.getReportPreview(selectedReportId)
        setReportPreview(preview)
      } catch (error) {
        setReportPreview('')
        notifyError('notice.previewFailed', error)
      }
    })()
  }, [selectedReportId])

  const presets = useMemo(() => bootstrap?.presets ?? {}, [bootstrap])

  async function refreshReports() {
    try {
      const list = await desktopApi.listReports()
      setReports(list)
    } catch (error) {
      setReports([])
      notifyError('notice.reportsRefreshFailed', error)
    }
  }

  async function refreshHistory() {
    try {
      const entries = await desktopApi.listHistory()
      setHistory(entries)
    } catch (error) {
      setHistory([])
      notifyError('notice.historyRefreshFailed', error)
    }
  }

  async function handleAddFiles() {
    try {
      const selected = await desktopApi.pickFiles()
      await handleCollectPaths(selected)
    } catch (error) {
      notifyError('notice.addFilesFailed', error)
    }
  }

  async function handleScanFolder() {
    try {
      const folder = await desktopApi.pickFolder()
      if (!folder) return
      const items = await desktopApi.scanFolder(folder)
      setFiles(dedupeFiles(items))
    } catch (error) {
      notifyError('notice.scanFailed', error)
    }
  }

  function handleClearFiles() {
    setFiles([])
    setStatus(null)
  }

  async function handlePickOutputFolder() {
    try {
      const folder = await desktopApi.pickFolder()
      if (!folder) return
      setConfig((prev) => ({ ...prev, output_folder: folder }))
    } catch (error) {
      notifyError('notice.pickFolderFailed', error)
    }
  }

  async function handleConvert() {
    if (!files.length || jobId) return
    try {
      const response = await desktopApi.startConversion({ files, config })
      setJobId(response.job_id)
      setStatus(null)
      notify(t(locale, 'notice.conversionStarted'), 'success')
    } catch (error) {
      notifyError('notice.conversionStartFailed', error)
    }
  }

  async function handleCancel() {
    if (!jobId) return
    try {
      await desktopApi.cancelConversion(jobId)
      notify(t(locale, 'notice.cancelRequested'), 'info')
    } catch (error) {
      notifyError('notice.cancelFailed', error)
    }
  }

  function handleConfigChange(next: Partial<ConversionConfig>) {
    setConfig((prev) => ({ ...prev, ...next }))
  }

  function handleApplyPreset(name: string) {
    setSelectedPreset(name)
    void desktopApi.setPreferences({ lastPreset: name }).catch((error) => {
      notifyError('notice.preferencesSaveFailed', error)
    })
    if (!name) return
    const preset = presets[name]
    if (!preset) return
    setConfig((prev) => ({
      ...prev,
      redimensionar: preset.resize,
      largura_max: preset.width,
      altura_max: preset.height,
      recorte_1x1: preset.crop,
      qualidade: preset.quality,
    }))
  }

  async function handleLocaleChange(nextLocale: LocaleCode) {
    setLocale(nextLocale)
    try {
      await desktopApi.setPreferences({ locale: nextLocale })
    } catch (error) {
      notifyError('notice.preferencesSaveFailed', error)
    }
  }

  async function handleThemeChange(nextTheme: ThemeMode) {
    setTheme(nextTheme)
    try {
      await desktopApi.setPreferences({ theme: nextTheme })
    } catch (error) {
      notifyError('notice.preferencesSaveFailed', error)
    }
  }

  async function handleCollectPaths(paths: string[]) {
    if (!paths.length) return
    try {
      const items = await desktopApi.collectPaths(paths)
      setFiles((prev) => dedupeFiles([...prev, ...items]))
    } catch (error) {
      notifyError('notice.collectPathsFailed', error)
    }
  }

  async function handleDropPaths(paths: string[]) {
    if (!paths.length) {
      setDropHintKey('drop.zoneNoPath')
      window.setTimeout(() => setDropHintKey('drop.zoneHint'), 3000)
      return
    }
    try {
      await handleCollectPaths(paths)
      setDropHintKey('drop.zoneHint')
    } catch {
      setDropHintKey('drop.zoneNoPath')
      window.setTimeout(() => setDropHintKey('drop.zoneHint'), 3000)
    }
  }

  useEffect(() => {
    const handler = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && jobId) {
        event.preventDefault()
        void handleCancel()
        return
      }

      if (!(event.ctrlKey || event.metaKey)) return
      const key = event.key.toLowerCase()
      if (key === 'o') {
        event.preventDefault()
        void handleAddFiles()
      } else if (key === 'enter') {
        event.preventDefault()
        void handleConvert()
      } else if (key === 'l') {
        event.preventDefault()
        handleClearFiles()
      }
    }

    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [jobId, files, config])

  async function handleClearHistory() {
    try {
      await desktopApi.clearHistory()
      await refreshHistory()
      notify(t(locale, 'notice.historyCleared'), 'success')
    } catch (error) {
      notifyError('notice.historyClearFailed', error)
    }
  }

  async function handleOpenReport(id: string, kind: 'html' | 'ai' | 'csv' | 'folder') {
    try {
      const result = await desktopApi.openReport(id, kind)
      if (!result.ok) {
        notify(t(locale, 'notice.openReportFailed'), 'error')
      }
    } catch (error) {
      notifyError('notice.openReportFailed', error)
    }
  }

  const isDark = theme === 'dark' || (theme === 'system' && systemPrefersDark)
  const appClass = isDark
    ? 'app-shell h-full bg-slate-900 text-slate-100'
    : 'app-shell h-full text-text-primary'
  const densityClass = 'density-compact'

  return (
    <div className={`${appClass} ${densityClass}`}>
      <TopBar
        locale={locale}
        theme={theme}
        currentTab={tab}
        onTabChange={setTab}
        onLocaleChange={handleLocaleChange}
        onThemeChange={handleThemeChange}
      />

      {notice && (
        <div className={`mx-6 mt-4 rounded-xl border px-4 py-2 text-sm ${
          notice.tone === 'error'
            ? 'border-red-300 bg-red-50 text-red-700'
            : notice.tone === 'success'
              ? 'border-emerald-300 bg-emerald-50 text-emerald-700'
              : 'border-brand-blue500/30 bg-blue-50 text-brand-blue600'
        }`}>
          {notice.message}
        </div>
      )}

      <main className={`h-[calc(100%-84px)] ${notice ? 'mt-3' : ''}`}>
        {tab === 'converter' ? (
          <ConverterPage
            locale={locale}
            files={files}
            config={config}
            presets={presets}
            selectedPreset={selectedPreset}
            status={status}
            historyCount={history.length}
            dropHintKey={dropHintKey}
            onAddFiles={handleAddFiles}
            onScanFolder={handleScanFolder}
            onClearFiles={handleClearFiles}
            onDropPaths={handleDropPaths}
            onPickOutputFolder={handlePickOutputFolder}
            onConvert={handleConvert}
            onCancel={handleCancel}
            onConfigChange={handleConfigChange}
            onApplyPreset={handleApplyPreset}
          />
        ) : (
          <ReportPage
            locale={locale}
            reports={reports}
            historyEntries={history}
            selectedReportId={selectedReportId}
            preview={reportPreview}
            onRefresh={refreshReports}
            onClearHistory={handleClearHistory}
            onSelectReport={setSelectedReportId}
            onOpenReport={handleOpenReport}
          />
        )}
      </main>
    </div>
  )
}

function dedupeFiles(files: FileItem[]): FileItem[] {
  const map = new Map<string, FileItem>()
  for (const item of files) {
    map.set(item.path, item)
  }
  return [...map.values()]
}
