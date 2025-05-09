import { defaultLocale, locales } from "./i18n.config"
import type { Strategies } from "@nuxtjs/i18n"

export default {
  locales,
  defaultLocale,
  detectBrowserLanguage: {
    alwaysRedirect: true,
    cookieKey: "lang", // django.conf.settings.LANGUAGE_COOKIE_NAME
    useCookie: true,
  },
  lazy: true,
  strategy: "prefix" as Strategies, // testu.eu/en/
  bundle: {
    // silent a deprecation warning
    optimizeTranslationDirective: false,
  },
}
