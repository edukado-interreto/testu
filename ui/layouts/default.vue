<script setup lang="ts">
import { useDisplay } from "vuetify"

const attrs = useAttrs()
const { mobile } = useDisplay()

const nav_drawer = ref(!mobile)
const embedded = computed(() => window?.location !== window?.parent?.location)
</script>

<template>
  <MainAppBar v-model="nav_drawer" />
  <v-navigation-drawer
    v-model="nav_drawer"
    v-if="!embedded"
    :app="!embedded"
    class="d-print-none"
    style="z-index: 1010"
    mobile-breakpoint="xs"
    :temporary="mobile"
    :location="mobile ? 'right' : 'left'"
    :rail="(attrs.is_editor as boolean) && !mobile"
  >
    <MainMenu />
  </v-navigation-drawer>
  <v-main>
    <slot />
  </v-main>
  <MainFooter :embedded="embedded" />
  <CookieConsent />
</template>

<style lang="scss">
@media print {
  .v-img * {
    print-color-adjust: exact; /* force printing background */
  }
}
</style>

<style scoped lang="scss">
@media print {
  .v-main {
    padding: 0 !important;
    width: 100% !important;
  }
}

.v-main {
  margin-bottom: 3em;
  min-height: 50vh;
}
</style>
