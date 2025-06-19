import { createVuetify } from "vuetify"
import * as components from "vuetify/components"
import * as directives from "vuetify/directives"
import colors from "vuetify/util/colors"
import { ca, cs, de, en, es, fr, hu, lt, pl, ru, sk, uk } from "vuetify/locale"

const vuetify = createVuetify({
  ssr: true,
  components,
  directives,
  theme: {
    themes: {
      dark: {
        dark: true,
      },
      light: {
        dark: false,
        colors: {
          primary: colors.blue.darken2,
          accent: colors.pink.accent4,
          secondary: colors.amber.darken3,
          tertiary: colors.grey.darken2,
          info: colors.teal.lighten1,
          warning: colors.amber.darken3,
          error: colors.pink.accent2,
          success: colors.lightGreen.darken2,
        },
      },
    },
  },
  locale: {
    // locale: "en",
    fallback: "en",
    messages: { ca, cs, de, en, es, fr, hu, lt, pl, ru, sk, uk },
  },
})

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(vuetify)
})
