import type {
  AppBootstrap,
  ConversionRequest,
  ConversionStatus,
  FileItem,
  HistoryEntry,
  ReportSummary,
  UserPreferences,
} from '../types'

declare global {
  interface Window {
    pywebview?: {
      api?: Record<string, (...args: unknown[]) => Promise<unknown>>
    }
  }
}

const fallbackBootstrap: AppBootstrap = {
  appName: 'BrJoy Image Converter',
  locale: 'pt-BR',
  presets: {
    'Hero Image': { resize: true, width: 1920, height: 1080, crop: true, quality: 85 },
    'Blog Post': { resize: true, width: 1200, height: 630, crop: true, quality: 85 },
    'Thumbnail': { resize: true, width: 400, height: 300, crop: true, quality: 80 },
    'Mobile Optimized': { resize: true, width: 800, height: null, crop: false, quality: 80 },
    'Avatar/Icon': { resize: true, width: 256, height: 256, crop: true, quality: 90 },
    'Original Quality': { resize: false, width: null, height: null, crop: false, quality: 95 },
  },
  preferences: {
    locale: 'pt-BR',
    theme: 'system',
    lastPreset: '',
    uiDensity: 'compact',
  },
  supportedExtensions: ['.jpg', '.jpeg', '.png', '.webp'],
}

async function call<T>(method: string, ...args: unknown[]): Promise<T> {
  const api = window.pywebview?.api
  if (!api || typeof api[method] !== 'function') {
    throw new Error(`Bridge method not available: ${method}`)
  }
  return api[method](...args) as Promise<T>
}

export const desktopApi = {
  async getBootstrap(): Promise<AppBootstrap> {
    try {
      return await call<AppBootstrap>('get_app_bootstrap')
    } catch {
      return fallbackBootstrap
    }
  },
  async pickFiles(): Promise<string[]> {
    return call<string[]>('pick_files')
  },
  async pickFolder(): Promise<string | null> {
    return call<string | null>('pick_folder')
  },
  async scanFolder(rootPath: string): Promise<FileItem[]> {
    return call<FileItem[]>('scan_folder', rootPath)
  },
  async collectPaths(paths: string[], baseFolder?: string): Promise<FileItem[]> {
    return call<FileItem[]>('collect_paths', paths, baseFolder ?? null)
  },
  async startConversion(payload: ConversionRequest): Promise<{ job_id: string }> {
    return call<{ job_id: string }>('start_conversion', payload)
  },
  async getConversionStatus(jobId: string): Promise<ConversionStatus> {
    return call<ConversionStatus>('get_conversion_status', jobId)
  },
  async cancelConversion(jobId: string): Promise<{ canceled: boolean }> {
    return call<{ canceled: boolean }>('cancel_conversion', jobId)
  },
  async listReports(): Promise<ReportSummary[]> {
    return call<ReportSummary[]>('list_reports')
  },
  async openReport(reportId: string, kind: 'html' | 'ai' | 'csv' | 'folder'): Promise<{ ok: boolean }> {
    return call<{ ok: boolean }>('open_report', reportId, kind)
  },
  async getReportPreview(reportId: string): Promise<string> {
    return call<string>('get_report_preview', reportId, 8000)
  },
  async listHistory(): Promise<HistoryEntry[]> {
    return call<HistoryEntry[]>('list_history')
  },
  async clearHistory(): Promise<{ ok: boolean }> {
    return call<{ ok: boolean }>('clear_history')
  },
  async setPreferences(prefs: Partial<UserPreferences>): Promise<{ ok: boolean; preferences: UserPreferences }> {
    return call<{ ok: boolean; preferences: UserPreferences }>('set_preferences', prefs)
  },
}
