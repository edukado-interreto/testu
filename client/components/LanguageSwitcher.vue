<script>
import locale_names from "~/i18n/locale_names.json"

export default {
  data: () => ({ locale_names }),
}
</script>

<template>
  <v-menu offset-y>
    <template v-slot:activator="{ on, attrs }">
      <v-btn text v-bind="attrs" v-on="on" class="text-none px-1 mr-1">
        <v-icon class="mr-1">mdi-translate</v-icon>
        <span class="d-none d-sm-inline">
          {{ locale_names[$i18n.locale] }}
        </span>
        <v-icon class="ml-1">mdi-chevron-down</v-icon>
      </v-btn>
    </template>

    <v-list dense rounded>
      <v-subheader class="text--primary font-weight-black text-uppercase">
        {{ $t("main.lang_menu_header") }}
      </v-subheader>
      <v-list-item
        v-for="lang in $i18n.localeCodes"
        nuxt
        :to="switchLocalePath(lang)"
        :class="{ 'v-list-item--active': lang == $i18n.locale }"
        :key="lang"
      >
        <v-item-avatar>
          <v-avatar
            :color="lang == $i18n.locale ? 'primary' : 'grey'"
            size="22px"
          >
            <small class="white--text">
              {{ lang.split("-")[0].toUpperCase() }}
            </small>
          </v-avatar>
        </v-item-avatar>
        <v-list-item-content>
          <v-list-item-title>{{ locale_names[lang] }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>
            <a href="https://tradukejo.ikso.net/project/6/" target="_blank">
              {{ $t("langs.help") }}
            </a>
          </v-list-item-title>
        </v-list-item-content>
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
