import locale_names from "./locale_names.json"

const locales = Object.entries(locale_names).map(([code, name]) => ({code, name, file: `${code}.json`}));

export default defineNuxtConfig({
  devtools: false,
  css: [
    "vuetify/lib/styles/main.sass",
    "@mdi/font/css/materialdesignicons.min.css",
    "@/assets/testu.scss"
  ],

  build: {
    transpile: ["vuetify"],
  },

  vite: {
    define: {
      "process.env.DEBUG": false,
    },
  },

  modules: ["@nuxtjs/i18n"],

  i18n: {
    defaultLocale: "en",
    langDir: "locales",
    lazy: true,
    locales,
    strategy: "prefix",
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: "i18n_redirected",
      alwaysRedirect: true,
      redirectOn: "root"
    },
  }
})
