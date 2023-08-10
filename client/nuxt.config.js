import colors from "vuetify/es5/util/colors"
import testu_locales from "./i18n/testu_locales.js"
import vuetify_locales from "./i18n/vuetify_locales.js"

export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  ssr: false,

  // Target: https://go.nuxtjs.dev/config-target
  target: "static",

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: "%s - TestU",
    title: "testu.eu",
    htmlAttrs: {
      lang: "en",
    },
    meta: [
      { charset: "utf-8" },
      {
        name: "viewport",
        content: "width=device-width, initial-scale=1",
      },
      { hid: "description", name: "description", content: "" },
      { name: "format-detection", content: "telephone=no" },
    ],
    link: [{ rel: "icon", type: "image/png", href: "/favicon.png" }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: "~/plugins/canvas-confetti.js", mode: "client" },
    { src: "~/plugins/vue-auth-jwt.js", mode: "client" },
    { src: "~/plugins/i18n.js" },
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/vuetify
    "@nuxtjs/vuetify",
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    "@nuxtjs/axios",
    "@nuxtjs/i18n",
  ],

  i18n: {
    defaultLocale: "en-GB",
    langDir: "i18n/",
    locales: testu_locales.locales,
    lazy: true,
    vueI18n: {
      fallbackLocale: ["en-GB", "en"],
      dateTimeFormats: Object.fromEntries(
        Object.entries(testu_locales.locales).map(([, locale]) => [
          locale["code"],
          {
            dt: Object.fromEntries(
              ["year", "month", "day", "hour", "minute"].map((el) => [
                el,
                "numeric",
              ]),
            ),
          },
        ]),
      ),
    },
  },

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {},

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ["~/assets/variables.scss"],
    theme: {
      dark: false,
      themes: {
        light: {
          primary: colors.blue.darken2,
          accent: colors.pink.accent4,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.darken3,
          error: colors.pink.accent2,
          success: colors.lightGreen.darken2,
        },
      },
    },
    lang: {
      locales: vuetify_locales,
      current: "en",
    },
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},

  server: {
    host: "0.0.0.0",
  },
}
