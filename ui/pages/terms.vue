<template>
  <v-container>
    <h1>{{ $t("main.terms") }}</h1>

    <p>{{ $t("terms.intro") }}</p>

    <h2 class="mt-4 mb-2">1. {{ $t("terms.section1.title") }}</h2>
    <ol>
      <li>{{ $t("terms.section1.text1") }}</li>
      <li>{{ $t("terms.section1.text2") }}</li>
      <li>{{ $t("terms.section1.text3") }}</li>
      <li>{{ $t("terms.section1.text4") }}</li>
      <li>{{ $t("terms.section1.text5") }}</li>
      <li>{{ $t("terms.section1.text6") }}</li>
      <li>{{ $t("terms.section1.text7") }}</li>
      <li>{{ $t("terms.section1.text8") }}</li>
      <li>{{ $t("terms.section1.text9") }}</li>
    </ol>

    <h2 class="mt-4 mb-2">2. {{ $t("terms.section2.title") }}</h2>
    <p>{{ $t("terms.section2.text1") }}</p>

    <h2 class="mt-4 mb-2">3. {{ $t("terms.section3.title") }}</h2>

    <ol>
      <li>{{ $t("terms.section3.text1") }}</li>
      <li>
        {{ $t("terms.section3.text2") }}
        <ul>
          <li>{{ $t("terms.section3.text2_1") }}</li>
          <li>{{ $t("terms.section3.text2_2") }}</li>
          <li>{{ $t("terms.section3.text2_3") }}</li>
        </ul>
      </li>
      <li>{{ $t("terms.section3.text3") }}</li>
      <li>
        {{ $t("terms.section3.text4") }}
        <ul>
          <li>{{ $t("terms.section3.text4_1") }}</li>
          <li>{{ $t("terms.section3.text4_2") }}</li>
          <li>{{ $t("terms.section3.text4_3") }}</li>
          <li>{{ $t("terms.section3.text4_4") }}</li>
          <li>{{ $t("terms.section3.text4_5") }}</li>
          <li>{{ $t("terms.section3.text4_6") }}</li>
          <li>{{ $t("terms.section3.text4_7") }}</li>
          <li>{{ $t("terms.section3.text4_8") }}</li>
        </ul>
      </li>
      <li>
        {{ $t("terms.section3.text5") }}
        <ul>
          <li>{{ $t("terms.section3.text5_1") }}</li>
          <li>{{ $t("terms.section3.text5_2") }}</li>
          <li>{{ $t("terms.section3.text5_3") }}</li>
        </ul>
      </li>
      <li>{{ $t("terms.section3.text6") }}</li>
    </ol>

    <h2 class="mt-4 mb-2">4. {{ $t("terms.section4.title") }}</h2>
    <p>{{ $t("terms.section4.text1") }}</p>

    <h2 class="mt-4 mb-2">5. {{ $t("terms.section5.title") }}</h2>
    <ol>
      <li>{{ $t("terms.section5.text1") }}</li>
      <li>{{ $t("terms.section5.text2") }}</li>
      <li>{{ $t("terms.section5.text3") }}</li>
      <li>{{ $t("terms.section5.text4") }}</li>
    </ol>

    <h2 class="mt-4 mb-2">6. {{ $t("terms.section6.title") }}</h2>
    <p v-html="$t('terms.section6.text1', { license: licenseLink })"></p>

    <h2 class="mt-4 mb-2">7. {{ $t("terms.section7.title") }}</h2>
    <ol>
      <li>{{ $t("terms.section7.text1") }}</li>
      <li v-html="$t('terms.section7.text2', { link: settingsLink })"></li>
      <li>{{ $t("terms.section7.text3") }}</li>
      <li>{{ $t("terms.section7.text4") }}</li>
    </ol>

    <h2 class="mt-4 mb-2">8. {{ $t("terms.section8.title") }}</h2>
    <ol>
      <li>{{ $t("terms.section8.text1") }}</li>
      <li>{{ $t("terms.section8.text2") }}</li>
      <li>{{ $t("terms.section8.text3") }}</li>
      <li>{{ $t("terms.section8.text4") }}</li>
      <li>{{ $t("terms.section8.text5") }}</li>
      <li>{{ $t("terms.section8.text6") }}</li>
    </ol>

    <h2 class="mt-4 mb-2">9. {{ $t("terms.section9.title") }}</h2>
    <ol>
      <li>{{ $t("terms.section9.text1") }}</li>
      <li>{{ $t("terms.section9.text2") }}</li>
      <li v-html="$t('terms.section9.text3', { link: termsLink })"></li>
      <li>{{ $t("terms.section9.text4") }}</li>
      <li v-html="$t('terms.section9.text5', { link: contactLink })"></li>
    </ol>

    <p class="mt-4">{{ $t("terms.last_update", { date: lastUpdate }) }}</p>
  </v-container>
</template>
<script>
export default {
  head() {
    return {
      title: this.$t("main.terms"),
    }
  },
  data() {
    return {
      settingsLink:
        '<a href="/user/settings" target="_blank">https://testu.eu/user/settings</a>',
      lastUpdate: "2023-07-13",
    }
  },
  computed: {
    termsLink() {
      return `<a href="${this.localePath(
        "/terms",
      )}" target="_blank">https://testu.eu${this.localePath("/terms")}</a>`
    },
    contactLink() {
      return `<a href="${this.localePath(
        "/privacy",
      )}" target="_blank">${this.$t("main.privacy")}</a>`
    },
    licenseLink() {
      return `<a href="https://creativecommons.org/publicdomain/zero/1.0/deed.${
        this.locale
      }" target="_blank">${this.$t("terms.section6.text1_license")}</a>`
    },
    locale() {
      return this.$i18n.locale.split("-")[0]
    },
  },
}
</script>
