<script setup lang="ts">
const localPath = useLocalePath()

const nav_drawer = ref(null)
</script>

<template>
  <v-app>
    <v-app-bar id="app-bar" flat outlined :app="true">
      <v-app-bar-nav-icon variant="text" @click="nav_drawer = !nav_drawer" />
      <v-btn
        id="home-button"
        size="x-large"
        variant="flat"
        class="text-none"
        :active="false"
        :to="localePath('/')"
      >
        <template v-slot:prepend>
          <img src="/favicon.png" height="40" />
        </template>
        Testu.eu
      </v-btn>
      <v-spacer />
      <h6
        class="catchphrase d-none d-md-block text-accent"
        v-text="$t('main.catchphrase')"
      />
      <v-spacer />
      <LanguageSwitcher />
      <v-btn
        class="text-none mx-2"
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
    </v-app-bar>
    <v-navigation-drawer v-model="nav_drawer">
      <MainMenu />
    </v-navigation-drawer>
    <v-main>
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
    </v-main>
  </v-app>
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
  margin-bottom: 4em;
  min-height: 50vh;
}
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
