<script setup lang="ts">
const menu = {
  home: { icon: "home", route: { name: "index" } },
  login: { icon: "login", cls: "d-md-none", route: { name: "login" } },
  signup: { icon: "account-plus", cls: "d-md-none", route: { name: "signup" } },
  my_learning: { icon: "chart-bar", route: { name: "learn" } },
  my_teaching: { icon: "briefcase", route: { name: "teach" } },
  about: { icon: "information", route: { name: "about" } },
  why: { icon: "star-shooting-outline", route: { name: "why" } },
  guide: { icon: "help-circle", route: { name: "guide", hash: "#1_exercise" } },
}
</script>

<template>
  <v-list>
    <MenuItem v-for="(item, label) in menu" v-bind="item" :label :key="label" />

    <v-list-subheader>{{ $t("main.social") }}</v-list-subheader>
    <v-list-item
      href="https://www.facebook.com/profile.php?id=100086451753450"
      target="_blank"
    >
      <template #prepend>
        <v-icon size="22" class="logo">
          <v-img src="/logos/facebook-2021.svg" cover />
        </v-icon>
      </template>
      {{ $t("main.facebook_page") }}
    </v-list-item>

    <v-list-item href="https://t.me/+8Z1dtayqGzk2Yzk0" target="_blank">
      <template #prepend>
        <v-icon size="22" class="logo">
          <v-img src="/logos/telegram-2019.svg" class="logo" cover />
        </v-icon>
      </template>
      {{ $t("main.telegram_chat") }}
    </v-list-item>
  </v-list>
</template>

<style lang="scss">
.logo {
  opacity: 1 !important;

  img {
    filter: grayscale(1);
  }
}
</style>
