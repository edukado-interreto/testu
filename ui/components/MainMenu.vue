<script setup lang="ts">
const menu = [
  { label: "home", icon: "home", path: "/" },
  { label: "login", icon: "login", path: "/login", cls: "d-md-none" },
  { label: "signup", icon: "account-plus", path: "/signup", cls: "d-md-none" },
  { label: "my_learning", icon: "chart-bar", path: "/learn" },
  { label: "my_teaching", icon: "briefcase", path: "/teach" },
  { label: "about", icon: "information", path: "/about" },
  { label: "why", icon: "star-shooting-outline", path: "/why" },
  { label: "guide", icon: "help-circle", path: "/guide" },
]
</script>

<template>
  <v-list>
    <MenuItem v-for="item in menu" v-bind="item" :key="item.label"></MenuItem>
  </v-list>
</template>
