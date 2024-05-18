<script setup lang="ts">
const menu = [
  { label: "home", icon: "home", path: "/" },
  { label: "login", icon: "login", path: "/login", cls: "d-md-none" },
  { label: "signup", icon: "account-plus", path: "/signup", cls: "d-md-none" },
  { label: "my_learning", icon: "chart-bar", path: "/learn" },
  { label: "my_teaching", icon: "briefcase", path: "/teach" },
  { label: "about", icon: "information", path: "/about" },
  { label: "why", icon: "star-shooting-outline", path: "/why" },
  { label: "guide", icon: "help-circle", path: "/guide#1_exercise" },
]
</script>

<template>
  <v-list>
    <MenuItem v-for="item in menu" v-bind="item" :key="item.label" />

    <v-list-subheader>{{ $t("main.social") }}</v-list-subheader>
    <v-list-item href="https://www.facebook.com/profile.php?id=100086451753450" target="_blank">
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
