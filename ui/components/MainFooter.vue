<script setup lang="ts">
const props = defineProps<{ embedded: boolean }>()
</script>

<template>
  <v-footer
    v-if="!embedded"
    app
    padless
    class="grey lighten-4 flex-column d-print-none"
    style="position: relative !important"
  >
    <div id="erasmus" class="white d-sm-flex align-center">
      <v-spacer />
      <img src="/partners/erasmus.png" class="mx-3" height="26" alt="" />
      <p class="text-grey-darken-1 ma-3" style="font-size: 0.9em">
        {{ $t("about.partners.european_commission") }}
      </p>
      <v-spacer />
    </div>

    <div class="px-4 py-2">
      <v-icon>mdi-creative-commons</v-icon>
      <a
        rel="license"
        href="https://creativecommons.org/publicdomain/zero/1.0/"
        target="_blank"
        class="text-grey caption text-decoration-none font-weight-bold"
      >
        CC0
      </a>
      <span class="caption mx-2">·</span>
      <v-icon>mdi-open-source-initiative</v-icon>
      <a
        href="https://gitlab.com/edukado-interreto/testu/"
        target="_blank"
        class="text-grey caption text-decoration-none font-weight-bold"
      >
        {{ $t("main.source_code") }}
      </a>
      <span class="caption mx-2">·</span>
      <NuxtLink
        :to="localePath('/terms')"
        class="text-grey caption text-decoration-none font-weight-bold"
      >
        {{ $t("main.terms") }}
      </NuxtLink>
      <span class="caption mx-2">·</span>
      <NuxtLink
        :to="localePath('/privacy')"
        class="text-grey caption text-decoration-none font-weight-bold"
      >
        {{ $t("main.privacy") }}
      </NuxtLink>
    </div>
  </v-footer>
</template>
