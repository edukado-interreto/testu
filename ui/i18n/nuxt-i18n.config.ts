const LOCALE_NAMES = {
  cs: "Čeština",
  cy: "Cymraeg",
  de: "Deutsch",
  dsb: "Dolnoserbski",
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

// locales = [
//   {code: "en", name: "English", file: "en.json"},
//   ...
// ]
const locales = Object.entries(LOCALE_NAMES).map(([code, name]) => ({
  code,
  name,
  file: `${code}.json`,
}))

export default {
  locales,
  lazy: true,
  langDir: "i18n/locales", // for lazy loading locales
  strategy: "prefix", // testu.eu/en/
  vueI18n: "./i18n/i18n.config.ts",
  detectBrowserLanguage: {
    useCookie: true,
    cookieKey: "lang",
    alwaysRedirect: true,
    redirectOn: "root",
  },
}
