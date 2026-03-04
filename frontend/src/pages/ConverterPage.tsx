import { useMemo, useState, type DragEvent } from 'react'
import type { ConversionConfig, FileItem, LocaleCode, ConversionStatus } from '../types'
import { t } from '../utils/i18n'

type ConverterPageProps = {
  locale: LocaleCode
  files: FileItem[]
  config: ConversionConfig
  presets: Record<string, { resize: boolean; width: number | null; height: number | null; crop: boolean; quality: number }>
  selectedPreset: string
  status: ConversionStatus | null
  historyCount: number
  dropHintKey: 'drop.zoneHint' | 'drop.zoneNoPath'
  onAddFiles: () => void
  onScanFolder: () => void
  onClearFiles: () => void
  onDropPaths: (paths: string[]) => void
  onPickOutputFolder: () => void
  onConvert: () => void
  onCancel: () => void
  onConfigChange: (next: Partial<ConversionConfig>) => void
  onApplyPreset: (presetName: string) => void
}

function formatBytes(bytes: number): string {
  if (!Number.isFinite(bytes)) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB']
  let value = bytes
  let idx = 0
  while (value >= 1024 && idx < units.length - 1) {
    value /= 1024
    idx += 1
  }
  return `${value.toFixed(1)} ${units[idx]}`
}

export function ConverterPage({
  locale,
  files,
  config,
  presets,
  selectedPreset,
  status,
  historyCount,
  dropHintKey,
  onAddFiles,
  onScanFolder,
  onClearFiles,
  onDropPaths,
  onPickOutputFolder,
  onConvert,
  onCancel,
  onConfigChange,
  onApplyPreset,
}: ConverterPageProps) {
  const totalInputSize = useMemo(() => files.reduce((acc, file) => acc + file.size, 0), [files])
  const isConverting = status?.phase === 'running' || status?.phase === 'queued'
  const percent = status && status.total > 0 ? Math.round((status.completed / status.total) * 100) : 0
  const isPt = locale === 'pt-BR'
  const [settingsTab, setSettingsTab] = useState<'basic' | 'advanced'>('basic')
  const filesSuffix = locale === 'en-US' ? 'file(s)' : 'arquivo(s)'
  const historySuffix = locale === 'en-US' ? 'history entries' : 'entradas no histórico'

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault()
    const dropped = Array.from(event.dataTransfer.files || [])
    const paths = dropped
      .map((file) => (file as File & { path?: string }).path ?? '')
      .filter((value) => value.length > 0)
    onDropPaths(paths)
  }

  return (
    <div className="grid h-full grid-cols-[minmax(0,1fr)_320px] gap-5 p-6">
      <section className="flex min-h-0 flex-col rounded-2xl border border-border bg-surface-card shadow-soft">
        <div className="flex items-center justify-between border-b border-border px-5 py-4">
          <div>
            <h2 className="text-lg font-semibold text-text-primary">{t(locale, 'labels.files')}</h2>
            <p className="text-sm text-text-secondary">
              {files.length} {filesSuffix} • {formatBytes(totalInputSize)}
            </p>
          </div>
          <div className="flex gap-2">
            <button onClick={onAddFiles} className="rounded-xl bg-brand-blue500 px-3 py-2 text-sm font-semibold text-white hover:bg-brand-blue600">
              {t(locale, 'actions.addFiles')}
            </button>
            <button onClick={onScanFolder} className="rounded-xl border border-border bg-white px-3 py-2 text-sm font-semibold text-text-primary hover:bg-slate-50">
              {t(locale, 'actions.scanFolder')}
            </button>
            <button onClick={onClearFiles} className="rounded-xl border border-border bg-white px-3 py-2 text-sm font-semibold text-text-primary hover:bg-slate-50">
              {t(locale, 'actions.clear')}
            </button>
          </div>
        </div>

        <div className="table-scroll min-h-0 flex-1 overflow-auto px-5 py-4">
          <div
            className="mb-3 rounded-xl border border-dashed border-border bg-slate-50 px-4 py-3 text-center"
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
          >
            <div className="text-sm font-semibold text-text-primary">{t(locale, 'drop.zoneTitle')}</div>
            <div className="text-xs text-text-secondary">{t(locale, dropHintKey)}</div>
          </div>
          {files.length === 0 ? (
            <div className="mt-20 text-center text-text-secondary">{t(locale, 'state.emptyFiles')}</div>
          ) : (
            <table className="w-full border-separate border-spacing-0 text-sm">
              <thead>
                <tr>
                  <th className="sticky top-0 bg-slate-50 px-3 py-2 text-left font-semibold text-text-secondary">Nome</th>
                  <th className="sticky top-0 bg-slate-50 px-3 py-2 text-right font-semibold text-text-secondary">Tamanho</th>
                  <th className="sticky top-0 bg-slate-50 px-3 py-2 text-center font-semibold text-text-secondary">Status</th>
                </tr>
              </thead>
              <tbody>
                {(status?.items ?? files).map((file) => (
                  <tr key={file.id} className="border-b border-border/60">
                    <td className="max-w-[520px] truncate px-3 py-2 text-text-primary">{file.relPath}</td>
                    <td className="px-3 py-2 text-right text-text-secondary">{formatBytes(file.size)}</td>
                    <td className="px-3 py-2 text-center">
                      <span className="rounded-lg bg-slate-100 px-2 py-1 text-xs font-medium text-slate-700">{file.status}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="border-t border-border px-5 py-4">
          <div className="mb-3 flex items-center justify-between text-sm text-text-secondary">
            <span>{status?.message ?? t(locale, 'state.ready')}</span>
            <span>{percent}%</span>
          </div>
          <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200">
            <div className="h-full rounded-full bg-gradient-to-r from-brand-blue500 to-brand-green500 transition-all" style={{ width: `${percent}%` }} />
          </div>
          <div className="mt-4 flex items-center justify-between">
            <div className="text-xs text-text-secondary">{historyCount} {historySuffix}</div>
            <div className="flex gap-2">
              {isConverting && (
                <button onClick={onCancel} className="rounded-xl border border-red-300 bg-red-50 px-4 py-2 text-sm font-semibold text-red-600 hover:bg-red-100">
                  {t(locale, 'actions.cancel')}
                </button>
              )}
              <button
                onClick={onConvert}
                disabled={files.length === 0 || isConverting}
                className="rounded-xl bg-brand-green500 px-5 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-60 hover:bg-brand-green600"
              >
                {t(locale, 'actions.convert')} ({files.length})
              </button>
            </div>
          </div>
        </div>
      </section>

      <aside className="side-scroll min-h-0 overflow-auto rounded-2xl border border-border bg-surface-card p-4 shadow-soft">
        <h3 className="text-base font-semibold text-text-primary">{t(locale, 'labels.settings')}</h3>
        <p className="mt-1 text-xs text-text-secondary">
          {isPt ? 'Fluxo simples: escolha formato, qualidade e rode.' : 'Simple flow: pick format, quality, and run.'}
        </p>

        <div className="mt-3 rounded-xl border border-border bg-white p-1">
          <div className="grid grid-cols-2 gap-1">
            <button
              onClick={() => setSettingsTab('basic')}
              className={`rounded-lg px-3 py-2 text-sm font-semibold ${
                settingsTab === 'basic'
                  ? 'bg-brand-blue500 text-white shadow-sm'
                  : 'text-text-secondary hover:bg-slate-100 hover:text-text-primary'
              }`}
            >
              {isPt ? 'Basico' : 'Basic'}
            </button>
            <button
              onClick={() => setSettingsTab('advanced')}
              className={`rounded-lg px-3 py-2 text-sm font-semibold ${
                settingsTab === 'advanced'
                  ? 'bg-brand-blue500 text-white shadow-sm'
                  : 'text-text-secondary hover:bg-slate-100 hover:text-text-primary'
              }`}
            >
              {isPt ? 'Avancado' : 'Advanced'}
            </button>
          </div>
        </div>

        {settingsTab === 'basic' ? (
          <div className="mt-3 space-y-3">
            <div className="rounded-xl border border-border bg-white p-3">
              <label className="mb-1 block text-[11px] font-semibold uppercase tracking-wide text-text-secondary">Preset</label>
              <select
                value={selectedPreset}
                onChange={(e) => onApplyPreset(e.target.value)}
                className="w-full rounded-lg border border-border bg-white px-3 py-2 text-sm"
              >
                <option value="">{isPt ? 'Custom' : 'Custom'}</option>
                {Object.keys(presets).map((preset) => (
                  <option key={preset} value={preset}>{preset}</option>
                ))}
              </select>
            </div>

            <div className="rounded-xl border border-border bg-white p-3">
              <label className="mb-2 block text-[11px] font-semibold uppercase tracking-wide text-text-secondary">{t(locale, 'labels.format')}</label>
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={() => onConfigChange({ formato: 'webp' })}
                  className={`rounded-lg border px-3 py-2 text-sm font-semibold ${config.formato === 'webp' ? 'border-brand-blue500 bg-brand-blue500 text-white' : 'border-border bg-white text-text-primary'}`}
                >
                  WebP
                </button>
                <button
                  onClick={() => onConfigChange({ formato: 'png' })}
                  className={`rounded-lg border px-3 py-2 text-sm font-semibold ${config.formato === 'png' ? 'border-brand-blue500 bg-brand-blue500 text-white' : 'border-border bg-white text-text-primary'}`}
                >
                  PNG
                </button>
              </div>
              <label className="mt-3 mb-2 block text-[11px] font-semibold uppercase tracking-wide text-text-secondary">
                {t(locale, 'labels.quality')} ({config.qualidade}%)
              </label>
              <input
                type="range"
                min={60}
                max={100}
                value={config.qualidade}
                onChange={(e) => onConfigChange({ qualidade: Number(e.target.value) })}
                className="w-full"
              />
            </div>

            <div className="rounded-xl border border-border bg-white p-3">
              <label className="mb-1 block text-[11px] font-semibold uppercase tracking-wide text-text-secondary">{t(locale, 'labels.outputFolder')}</label>
              <div className="flex gap-2">
                <input value={config.output_folder} readOnly className="w-full rounded-lg border border-border bg-slate-100 px-3 py-2 text-xs text-text-secondary" />
                <button
                  onClick={onPickOutputFolder}
                  disabled={config.manter_estrutura || config.substituir_no_lugar}
                  className="rounded-lg border border-border bg-white px-3 py-2 text-sm font-semibold text-text-primary disabled:opacity-50"
                >
                  {t(locale, 'actions.chooseFolder')}
                </button>
              </div>
            </div>

            <label className="flex items-center justify-between rounded-xl border border-border bg-white px-3 py-2 text-sm text-text-primary">
              <span>{t(locale, 'labels.keepStructure')}</span>
              <input type="checkbox" checked={config.manter_estrutura} onChange={(e) => onConfigChange({ manter_estrutura: e.target.checked })} />
            </label>
          </div>
        ) : (
          <div className="mt-3 space-y-3">
            <div className="rounded-xl border border-border bg-slate-50/70 p-3">
              <label className="flex items-center justify-between rounded-lg border border-border bg-white px-3 py-2 text-sm text-text-primary">
                <span>{t(locale, 'labels.resize')}</span>
                <input type="checkbox" checked={config.redimensionar} onChange={(e) => onConfigChange({ redimensionar: e.target.checked })} />
              </label>

              <div className="grid grid-cols-2 gap-2">
                <input
                  type="number"
                  disabled={!config.redimensionar}
                  value={config.largura_max ?? ''}
                  onChange={(e) => onConfigChange({ largura_max: e.target.value ? Number(e.target.value) : null })}
                  className="rounded-lg border border-border bg-white px-3 py-2 text-sm disabled:bg-slate-100"
                  placeholder="Width"
                />
                <input
                  type="number"
                  disabled={!config.redimensionar}
                  value={config.altura_max ?? ''}
                  onChange={(e) => onConfigChange({ altura_max: e.target.value ? Number(e.target.value) : null })}
                  className="rounded-lg border border-border bg-white px-3 py-2 text-sm disabled:bg-slate-100"
                  placeholder="Height"
                />
              </div>

              <label className="flex items-center justify-between rounded-lg border border-border bg-white px-3 py-2 text-sm text-text-primary">
                <span>{t(locale, 'labels.crop')}</span>
                <input type="checkbox" checked={config.recorte_1x1} onChange={(e) => onConfigChange({ recorte_1x1: e.target.checked })} />
              </label>

              <label className="flex items-center justify-between rounded-lg border border-border bg-white px-3 py-2 text-sm text-text-primary">
                <span>{t(locale, 'labels.batchSizes')}</span>
                <input type="checkbox" checked={config.batch_sizes_enabled} onChange={(e) => onConfigChange({ batch_sizes_enabled: e.target.checked })} />
              </label>

              <input
                type="text"
                placeholder="800,1200,1920"
                disabled={!config.batch_sizes_enabled}
                value={config.batch_sizes.join(',')}
                onChange={(e) => {
                  const sizes = e.target.value
                    .split(',')
                    .map((v) => Number(v.trim()))
                    .filter((v) => Number.isFinite(v) && v > 0)
                  onConfigChange({ batch_sizes: sizes })
                }}
                className="w-full rounded-lg border border-border bg-white px-3 py-2 text-sm disabled:bg-slate-100"
              />

              <label className="flex items-center justify-between rounded-lg border border-border bg-white px-3 py-2 text-sm text-text-primary">
                <span>{t(locale, 'labels.sharpen')}</span>
                <input type="checkbox" checked={config.sharpen} onChange={(e) => onConfigChange({ sharpen: e.target.checked })} />
              </label>

              <div className="rounded-lg border border-border bg-white px-3 py-2">
                <label className="mb-2 block text-[11px] font-semibold uppercase tracking-wide text-text-secondary">{t(locale, 'labels.brightness')} ({config.brightness}%)</label>
                <input
                  type="range"
                  min={50}
                  max={150}
                  value={config.brightness}
                  onChange={(e) => onConfigChange({ brightness: Number(e.target.value) })}
                  className="w-full"
                />
              </div>

              <label className="flex items-center justify-between rounded-lg border border-border bg-white px-3 py-2 text-sm text-text-primary">
                <span>{t(locale, 'labels.keepStructure')}</span>
                <input type="checkbox" checked={config.manter_estrutura} onChange={(e) => onConfigChange({ manter_estrutura: e.target.checked })} />
              </label>

              <label className="flex items-center justify-between rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
                <span>{t(locale, 'labels.replaceInPlace')}</span>
                <input type="checkbox" checked={config.substituir_no_lugar} onChange={(e) => onConfigChange({ substituir_no_lugar: e.target.checked })} />
              </label>
            </div>
          </div>
        )}
      </aside>
    </div>
  )
}
