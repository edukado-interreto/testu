import type { DateTimeFormat, Locale } from "@intlify/core-base"

const LOCALES = {
  // ca: "Català",
  cs: "Čeština",
  cy: "Cymraeg",
  de: "Deutsch",
  dsb: "Dolnoserbšćina",
  en: "English",
  eo: "Esperanto",
  es: "Español",
  fr: "Français",
  ga: "Gaeilge",
  hu: "Magyar",
  lt: "Lietuvių",
  pl: "Polski",
  ru: "Русский",
  sk: "Slovenčina",
  uk: "Українська",
}

const FORMATS: DateTimeFormat = {
  short: {
    year: "numeric",
    month: "short",
    day: "numeric",
  },
  long: {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
  },
}

export const defaultLocale = "en" as Locale

export const locales = Object.entries(LOCALES).map(([code, name]) => ({
  code,
  name,
  file: `${code}.json`,
}))

export const datetimeFormats = Object.fromEntries(
  Object.keys(LOCALES).map((code) => [code, FORMATS])
)

export const fallbackLocale = {
  "en-US": ["en"],
  sk: ["cs"],
  cs: ["sk"],
  default: ["en", "eo"],
}

// Auto-use of vue-i18n options in defineNuxtConfig in nuxt.config.ts
export default { datetimeFormats, fallbackLocale }
