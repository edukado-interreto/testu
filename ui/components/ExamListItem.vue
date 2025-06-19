<script setup lang="ts">
import { useI18n } from "vue-i18n"
import { useRoute, useRouter } from "vue-router"
import { useNuxtApp } from "#app"

const props = defineProps<{ item: any }>()
const { t, d } = useI18n()
const { $localePath } = useNuxtApp()

function localePath(path: string) {
  // fallback if $localePath is not available
  return $localePath ? $localePath(path) : path
}
</script>

<template>
  <v-card
    :to="localePath(`/exam_editor?exam=${props.item.lid}`)"
    nuxt
    class="mb-5"
  >
    <v-card-title class="subheading font-weight-bold">
      <span>
        {{ props.item.name }}
      </span>
      <v-spacer></v-spacer>
      <v-chip v-if="props.item.accept_submission" small color="primary">
        Accepts submissions
      </v-chip>
    </v-card-title>
    <v-card-subtitle v-if="props.item.description">
      {{ props.item.description }}
    </v-card-subtitle>
    <v-divider></v-divider>
    <v-card-text>
      <v-icon small>mdi-account</v-icon>
      {{ props.item.created_by || t("exercise.anonymous") }}
      <span>·</span>
      <v-icon small>mdi-clock</v-icon>
      {{ d(new Date(props.item.created), "dt") }}
    </v-card-text>
  </v-card>
</template>
