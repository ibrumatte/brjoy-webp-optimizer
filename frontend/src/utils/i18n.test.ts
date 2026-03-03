import { describe, expect, it } from 'vitest'
import { t } from './i18n'

describe('i18n utility', () => {
  it('returns translated value for pt-BR key', () => {
    expect(t('pt-BR', 'actions.convert')).toBe('Converter')
  })

  it('falls back to key when missing', () => {
    expect(t('en-US', 'missing.key')).toBe('missing.key')
  })

  it('supports new drop hint strings', () => {
    expect(t('en-US', 'drop.zoneHint')).toContain('fallback')
  })

  it('supports history empty state strings', () => {
    expect(t('pt-BR', 'state.emptyHistory')).toContain('Histórico')
  })

  it('supports notice strings', () => {
    expect(t('en-US', 'notice.openReportFailed')).toContain('report')
  })

  it('supports density labels', () => {
    expect(t('pt-BR', 'density.compact')).toBe('Compacto')
  })
})
