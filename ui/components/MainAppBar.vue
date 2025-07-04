<script setup lang="ts">
const auth = useAuthStore()
const localePath = useLocalePath()
const { t } = useI18n()

const model = defineModel<boolean>()

const home = localePath({ name: "index" })

const embedded = computed(() => {
  if (!window) return false
  return window.location !== window.parent?.location
})

const logout = async () => {
  auth.logout()
  await navigateTo(home)
}

onMounted(async () => {
  await auth.check_token()
})
</script>

<template>
  <v-app-bar
    v-if="!embedded"
    :app="!embedded"
    id="app-bar"
    class="d-print-none"
    scroll-behavior="hide"
    flat
    tile
  >
    <v-btn
      id="home-button"
      size="x-large"
      variant="flat"
      class="text-none text-accent font-weight-medium"
      :active="false"
      :to="home"
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

    <LanguageSwitcher class="me-2" />

    <v-btn v-if="auth.logged_in" icon class="mx-4">
      <v-icon>mdi-account</v-icon>
      <v-menu activator="parent">
        <v-list>
          <v-list-item :title="auth.user?.username" />

          <v-list-item @click="logout" :title="t('main.logout')" />
        </v-list>
      </v-menu>
    </v-btn>

    <div v-else class="d-none d-md-block mx-4">
      <v-btn
        class="text-none me-4"
        variant="flat"
        color="grey-lighten-4"
        :to="localePath({ name: 'login' })"
        nuxt
      >
        {{ $t("main.login") }}
      </v-btn>
      <v-btn
        class="text-none"
        variant="flat"
        color="amber-darken-1"
        :to="localePath({ name: 'signup' })"
        nuxt
      >
        {{ $t("main.signup") }}
      </v-btn>
    </div>
    <v-app-bar-nav-icon class="d-md-none" @click="model = !model" />
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
