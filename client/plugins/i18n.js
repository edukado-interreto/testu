export default function ({ app }) {
  app.i18n.onLanguageSwitched = (oldLocale, newLocale) => {
    // set vuetify's locale when switching language
    app.vuetify.framework.lang.current = newLocale
  }
}
