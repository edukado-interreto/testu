import langs from '~/data/langs.js'
export default {
  computed: {
    langs_table() {
      return langs.langs; // TODO i18n
    },
    langs_available() {
      return Object.entries(
        langs.langs
      ).map(
        e => ({
          value: e[0],
          text: e[1].name // TODO: localization of languages name
        })
      ).sort(
        (a, b) => a.text.localeCompare(b.text)
      );
    }
  },
}
