import type { LocaleCode, ThemeMode, UserPreferences } from '../types'
import { t } from '../utils/i18n'

type TopBarProps = {
  locale: LocaleCode
  theme: ThemeMode
  density: UserPreferences['uiDensity']
  currentTab: 'converter' | 'report'
  onTabChange: (tab: 'converter' | 'report') => void
  onLocaleChange: (locale: LocaleCode) => void
  onThemeChange: (theme: ThemeMode) => void
  onDensityChange: (density: 'compact') => void
}

export function TopBar({
  locale,
  theme,
  density,
  currentTab,
  onTabChange,
  onLocaleChange,
  onThemeChange,
  onDensityChange,
}: TopBarProps) {
  const tabClass = (tab: 'converter' | 'report') =>
    `rounded-xl px-4 py-2 text-sm font-semibold transition ${
      currentTab === tab
        ? 'bg-brand-blue500 text-white shadow-sm'
        : 'bg-transparent text-slate-300 hover:bg-white/10 hover:text-white'
    }`

  return (
    <header className="border-b border-slate-700/30 bg-gradient-to-r from-brand-navy900 via-brand-navy800 to-brand-navy900">
      <div className="mx-auto flex max-w-[1400px] items-center justify-between px-6 py-4">
        <div className="flex items-center gap-8">
          <div>
            <div className="text-3xl font-black tracking-tight text-white">BrJoy</div>
            <div className="text-xs text-slate-300">{t(locale, 'header.subtitle')}</div>
          </div>
          <nav className="flex items-center gap-2 rounded-2xl border border-white/10 bg-black/10 p-1">
            <button className={tabClass('converter')} onClick={() => onTabChange('converter')}>
              {t(locale, 'tabs.converter')}
            </button>
            <button className={tabClass('report')} onClick={() => onTabChange('report')}>
              {t(locale, 'tabs.report')}
            </button>
          </nav>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={locale}
            onChange={(e) => onLocaleChange(e.target.value as LocaleCode)}
            className="rounded-xl border border-white/20 bg-white/10 px-3 py-2 text-sm font-medium text-white outline-none"
          >
            <option className="text-slate-900" value="pt-BR">PT-BR</option>
            <option className="text-slate-900" value="en-US">EN-US</option>
          </select>
          <select
            value={theme}
            onChange={(e) => onThemeChange(e.target.value as ThemeMode)}
            className="rounded-xl border border-white/20 bg-white/10 px-3 py-2 text-sm font-medium text-white outline-none"
          >
            <option className="text-slate-900" value="system">System</option>
            <option className="text-slate-900" value="light">Light</option>
            <option className="text-slate-900" value="dark">Dark</option>
          </select>
          <select
            value={density}
            onChange={() => onDensityChange('compact')}
            disabled
            className="rounded-xl border border-white/20 bg-white/10 px-3 py-2 text-sm font-medium text-white outline-none"
          >
            <option className="text-slate-900" value="compact">{t(locale, 'density.compact')}</option>
          </select>
        </div>
      </div>
    </header>
  )
}
