import i18n from "./i18n/nuxti18n"

const DJANGO_HOST = "http://django:8000"
const BACKEND_URLS = ["api", "admin", "assets", "__debug__"]
const devProxy = Object.fromEntries(
  BACKEND_URLS.map((url) => [`/${url}`, `${DJANGO_HOST}/${url}`])
)

export default defineNuxtConfig({
  build: { transpile: ["vuetify"] },
  compatibilityDate: "2025-04-06",
  css: [
    "vuetify/lib/styles/main.sass",
    "@/assets/vuetify/settings.scss",
    "@mdi/font/css/materialdesignicons.min.css",
    "@/assets/testu.scss",
  ],
  devtools: { enabled: false },
  i18n,
  modules: ["@nuxtjs/i18n", "@pinia/nuxt"],
  nitro: { devProxy },
  runtimeConfig: { public: { apiBase: "" } }, // or NUXT_PUBLIC_API_BASE
  // vite: {
  //   css: {
  //     preprocessorOptions: {
  //       scss: {
  //         additionalData: '@forward "~/assets/vuetify/settings.scss";',
  //       },
  //     },
  //   },
  // },
})
