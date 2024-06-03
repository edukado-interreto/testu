import locales from "./locale_names"

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
