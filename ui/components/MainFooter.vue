<script setup lang="ts">
const localePath = useLocalePath()
const props = defineProps<{ embedded: boolean }>()
</script>

<template>
  <v-footer
    v-if="!embedded"
    app
    color="grey-lighten-4"
    class="flex-column d-print-none pa-0"
    style="position: relative"
  >
    <div id="erasmus" class="bg-white d-sm-flex align-center">
      <v-spacer />
      <img src="/partners/erasmus.png" class="mx-3" height="26" alt="" />
      <p class="text-grey-darken-1 pa-3 v-col-md-7">
        {{ $t("about.partners.european_commission") }}
      </p>
      <v-spacer />
    </div>

    <div id="footer-links" class="px-4 py-2">
      <v-icon class="me-1">mdi-creative-commons</v-icon>
      <a
        rel="license"
        href="https://creativecommons.org/publicdomain/zero/1.0/"
        target="_blank"
        class="text-grey caption text-decoration-none font-weight-bold"
      >
        CC0
      </a>
      <span class="caption mx-2">·</span>
      <v-icon class="me-1">mdi-open-source-initiative</v-icon>
      <a
        href="https://gitlab.com/edukado-interreto/testu/"
        target="_blank"
        class="text-grey caption text-decoration-none font-weight-bold"
      >
        {{ $t("main.source_code") }}
      </a>
      <span class="caption mx-2">·</span>
      <nuxt-link
        :to="localePath('/terms')"
        class="text-grey caption text-decoration-none font-weight-bold"
      >
        {{ $t("main.terms") }}
      </nuxt-link>
      <span class="caption mx-2">·</span>
      <nuxt-link
        :to="localePath('/privacy')"
        class="text-grey caption text-decoration-none font-weight-bold"
      >
        {{ $t("main.privacy") }}
      </nuxt-link>
    </div>
    <Toasts />
  </v-footer>
</template>

<style scoped lang="scss">
#erasmus {
  padding: 0.6rem;
  width: 100%;

  p {
    font-size: 12px;
  }
}

#footer-links {
  font-size: 12px;
}
</style>
