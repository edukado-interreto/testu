import i18n from "./i18n/nuxt-i18n.config"

const DJANGO_HOST = "http://django:8000"
const BACKEND_URLS = ["api", "admin", "assets", "__debug__"]
const devProxy = Object.fromEntries(
  BACKEND_URLS.map((url) => [`/${url}`, `${DJANGO_HOST}/${url}`])
)

export default defineNuxtConfig({
  devtools: false,

  runtimeConfig: {
    public: {
      apiBase: "", // can be overridden by NUXT_PUBLIC_API_BASE env variable
    },
  },

  css: [
    "vuetify/lib/styles/main.sass",
    "@mdi/font/css/materialdesignicons.min.css",
    "@/assets/testu.scss",
  ],

  build: { transpile: ["vuetify"] },

  nitro: { devProxy },

  vite: { define: { "process.env.DEBUG": false } },

  modules: ["@nuxtjs/i18n", "@pinia/nuxt"],

  i18n,
})
