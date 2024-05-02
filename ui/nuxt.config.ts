// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  app: { head: { charset: "utf-8", viewport: "width=device-width, initial-scale=1", title: "Testu.eu", titleTemplate: "%s - Testu.eu", },
  },
  build: { transpile: ["vuetify"], },
  css: [ "vuetify/lib/styles/main.sass", "@mdi/font/css/materialdesignicons.css", ],
  devtools: { enabled: false }
})
