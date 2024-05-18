<script setup lang="ts">
const localePath = useLocalePath()
const embedded = computed(() => window?.location !== window?.parent?.location)
const logged_in = ref(false)
</script>

<template>
    <v-app-bar
      v-if="!embedded"
      :app="!embedded"
      id="app-bar"
      class="d-print-none"
      flat
      tile
      outlined
    >
      <v-btn
        id="home-button"
        size="x-large"
        variant="flat"
        class="text-none text-accent font-weight-medium"
        :active="false"
        :to="localePath('/')"
      >
        <template v-slot:prepend>
          <img src="/favicon.png" height="40" />
        </template>
        testu.eu
      </v-btn>
      <v-spacer />
      <h6
        class="catchphrase d-none d-md-block text-accent"
        v-text="$t('main.catchphrase')"
      />
      <v-spacer />
      <LanguageSwitcher class="me-2"/>

      <div v-if="!logged_in" class="d-none d-md-block mx-4">
        <v-btn
          class="text-none me-4"
          variant="flat"
          color="grey-lighten-4"
          :to="localePath('/login')"
          nuxt
        >
          {{ $t("main.login") }}
        </v-btn>
        <v-btn
          class="text-none"
          variant="flat"
          color="amber-darken-1"
          :to="localePath('/signup')"
          nuxt
        >
          {{ $t("main.signup") }}
        </v-btn>
      </div>
      <v-app-bar-nav-icon class="d-md-none" @click="nav_drawer = !nav_drawer" />
    </v-app-bar>
</template>

<style scoped lang="scss">
.catchphrase {
  font-family: "Roboto Slab", Roboto, serif;
  font-size: 120%;
  font-weight: 700;
}
#app-bar {
  border-bottom-width: thin;
  border-bottom-style: solid;
  border-bottom-color: rgba(var(--v-border-color), var(--v-border-opacity));
}
</style>
