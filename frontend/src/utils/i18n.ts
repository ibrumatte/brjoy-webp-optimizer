import pt from '../i18n/pt-BR.json'
import en from '../i18n/en-US.json'
import type { LocaleCode } from '../types'

const dict = {
  'pt-BR': pt,
  'en-US': en,
}

export function t(locale: LocaleCode, key: string): string {
  const lang = dict[locale] ?? dict['pt-BR']
  return (lang as Record<string, string>)[key] ?? key
}
