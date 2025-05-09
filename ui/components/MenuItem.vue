<script setup lang="ts">
const { locale, setLocale } = useI18n()
import type { RouteLocation, RouteLocationNamedI18n } from "vue-router"

const props = defineProps<{
  label: string
  icon: string
  route: RouteLocationNamedI18n
  cls?: string
}>()
const localePath = useLocalePath()

const list_item_classes =
  "v-list-item v-list-item--link v-theme--light v-list-item--density-default v-list-item--one-line rounded-0 v-list-item--variant-text"
</script>

<template>
  <nuxt-link
    :to="localePath(route)"
    active-class="v-list-item--active text-primary"
    :class="[list_item_classes, cls || ''].join(' ')"
  >
    <div class="v-list-item__overlay" />
    <div class="v-list-item__prepend">
      <v-icon>mdi-{{ icon }}</v-icon>
      <div class="v-list-item__spacer" />
    </div>
    <div class="v-list-item__content">{{ $t(`main.${label}`) }}</div>
  </nuxt-link>
</template>
