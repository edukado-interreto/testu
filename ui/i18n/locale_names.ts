export const LOCALE_NAMES = {
  cs: "Čeština",
  cy: "Cymraeg",
  de: "Deutsch",
  dsb: "Dolnoserbski",
  en: "English",
  eo: "Esperanto",
  es: "Español",
  fr: "Français",
  ga: "Gaeilge",
  hu: "Magyar",
  lt: "Lietuvių",
  pl: "Polski",
  ru: "Русский",
  sk: "Slovenčina",
  uk: "Українська",
}

/**
  const locales = [
    {code: "en", name: "English", file: "en.json"},
    ...
  ]
*/
const locales = Object.entries(LOCALE_NAMES).map(([code, name]) => ({
  code,
  name,
  file: `${code}.json`,
}))

export default locales
