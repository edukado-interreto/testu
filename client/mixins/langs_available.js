import langs from '~/data/langs.js'
export default {
  computed: {
    langs_available() {
      // TODO: localization of languages name
      return Object.entries(
        langs.langs
      ).map(
        e => ({ value: e[0], text: e[1].name })
      ).sort(
        (a, b) => a.text.localeCompare(b.text)
      );
    }
  },
}
