import { LOCALE_NAMES } from "./locale_names"

const DEFAULT_LOCALE = "en"

const FORMATS = {
  short: {
    year: "numeric",
    month: "numeric",
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

const datetimeFormats = Object.fromEntries(
  Object.keys(LOCALE_NAMES).map((code) => [code, FORMATS])
)

export default defineI18nConfig(() => ({
  legacy: false,
  defaultLocale: DEFAULT_LOCALE,
  fallbackLocale: { sk: ["cs"], cs: ["sk"], default: ["en", "eo"] },
  datetimeFormats,
}))
