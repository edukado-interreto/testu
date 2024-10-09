import locales from "./locale_names"
import type { RedirectOnOptions, Strategies } from "@nuxtjs/i18n"

export default {
  detectBrowserLanguage: {
    alwaysRedirect: true,
    cookieKey: "lang",
    redirectOn: "root" as RedirectOnOptions,
    useCookie: true,
  },
  langDir: "i18n/locales", // for lazy loading locales
  locales,
  lazy: true,
  strategy: "prefix" as Strategies, // testu.eu/en/
  vueI18n: "./i18n/i18n.config.ts",
}
