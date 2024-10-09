import i18n from "./i18n/nuxt-i18n.config"

const DJANGO_HOST = "http://django:8000"
const BACKEND_URLS = ["api", "admin", "assets", "__debug__"]
const devProxy = Object.fromEntries(
  BACKEND_URLS.map((url) => [`/${url}`, `${DJANGO_HOST}/${url}`])
)

// Vite configuration needed for sass version < 2.0 because of this warning:
// Deprecation Warning: The legacy JS API is deprecated and will be removed in Dart Sass 2.0.0.
const vite = {
  css: { preprocessorOptions: { sass: { api: "modern" }, scss: { api: "modern" } } },
}

export default defineNuxtConfig({
  build: { transpile: ["vuetify"] },
  compatibilityDate: "2024-10-10",
  css: [
    "vuetify/lib/styles/main.sass",
    "@mdi/font/css/materialdesignicons.min.css",
    "@/assets/testu.scss",
  ],
  devtools: { enabled: false },
  modules: ["@nuxtjs/i18n", "@pinia/nuxt"],
  nitro: { devProxy },
  runtimeConfig: { public: { apiBase: "" } }, // or NUXT_PUBLIC_API_BASE
  i18n,
  vite,
})
