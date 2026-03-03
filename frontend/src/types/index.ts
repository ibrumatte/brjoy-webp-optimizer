export type LocaleCode = 'pt-BR' | 'en-US'
export type ThemeMode = 'light' | 'dark' | 'system'

export type FileItem = {
  id: string
  path: string
  relPath: string
  size: number
  status: string
  sizeAfter: number
  error?: string
}

export type ConversionConfig = {
  formato: 'webp' | 'png'
  redimensionar: boolean
  largura_max: number | null
  altura_max: number | null
  recorte_1x1: boolean
  qualidade: number
  sharpen: boolean
  brightness: number
  batch_sizes_enabled: boolean
  batch_sizes: number[]
  substituir_no_lugar: boolean
  manter_estrutura: boolean
  output_folder: string
}

export type ConversionRequest = {
  files: FileItem[]
  config: ConversionConfig
}

export type ConversionStatus = {
  job_id: string
  phase: string
  completed: number
  total: number
  success: number
  errors: number
  skipped: number
  message: string
  startedAt: string
  finishedAt: string
  durationSeconds: number
  reportId: string
  outputFolder: string
  sourceFolders: string[]
  items: FileItem[]
}

export type ReportSummary = {
  id: string
  generated_at?: string
  generatedAt?: string
  source_folders?: string[]
  sourceFolders?: string[]
  output_folders?: string[]
  outputFolders?: string[]
  success: number
  errors: number
  total: number
  report_folder?: string
  reportFolder?: string
  html_report?: string
  ai_report?: string
  csv_report?: string
}

export type HistoryEntry = {
  timestamp?: string
  result?: string
  errors?: string
  folder?: string
  raw: string
}

export type UserPreferences = {
  locale: LocaleCode
  theme: ThemeMode
  lastPreset: string
  uiDensity: 'compact'
}

export type AppBootstrap = {
  appName: string
  locale: LocaleCode
  presets: Record<string, {
    resize: boolean
    width: number | null
    height: number | null
    crop: boolean
    quality: number
  }>
  preferences: UserPreferences
  supportedExtensions: string[]
}
