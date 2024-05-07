<script setup lang="ts">
import locale_names from "@/locale_names.json"

const { locale, locales, setLocale } = useI18n()
const switchLocalePath = useSwitchLocalePath()

const set_locale = (code) => {
  setLocale(code)
  console.info(switchLocalePath(code))
}
</script>

<template>
  <v-menu transition="slide-y-transition" scroll-strategy="block">
    <template #activator="{ props }">
      <v-btn v-bind="props" class="text-none px-1 mr-1">
        <v-icon class="mr-1">mdi-translate</v-icon>
        <span class="d-none d-sm-inline">
          {{ locale_names[locale] }}
        </span>
        <v-icon class="ml-1">mdi-chevron-down</v-icon>
      </v-btn>
    </template>

    <v-list density="compact" rounded>
      <v-list-subheader class="text--primary font-weight-black text-uppercase">
        {{ $t("main.lang_menu_header") }}
      </v-list-subheader>
      <v-list-item
        v-for="{ code, name } in locales"
        @click="() => set_locale(code)"
        :active="code == locale"
        :key="code"
      >
        <template #prepend>
          <v-avatar :color="code == locale ? 'primary' : 'grey'" size="22px">
            <small class="text-white">
              {{ code.split("-")[0].toUpperCase() }}
            </small>
          </v-avatar>
        </template>
        {{ name }}
      </v-list-item>

      <v-list-item>
        <v-btn
          to="https://tradukejo.ikso.net/project/6/"
          target="_blank"
          size="small"
          density="comfortable"
          variant="flat"
          color="accent"
          class="text-none font-weight-bold"
        >
          {{ $t("langs.help") }}
        </v-btn>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<style scoped>
.v-menu__content {
  max-height: 85vh;
}
.v-list-item--dense,
.v-list--dense .v-list-item {
  min-height: 1.8rem;
  padding: 0 8px;
}
.v-list-item .v-list-item__content {
  padding: 2px 0.8rem !important;
}
.v-avatar small {
  font-size: 60%;
  font-weight: bold;
}
</style>
