import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import colors from 'vuetify/util/colors'

const vuetify = createVuetify({
  ssr: true,
  components,
  directives,
  theme: {
    themes: {
      light: {
        dark: false,
        colors: {
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
  },
})

export default defineNuxtPlugin(nuxtApp => {
  nuxtApp.vueApp.use(vuetify)

})
