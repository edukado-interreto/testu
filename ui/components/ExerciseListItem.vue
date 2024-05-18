<template>
  <v-card :to="localePath(`/exercise/${item.lid}`)" nuxt class="mb-5">
    <v-card-title class="subheading font-weight-bold">
      {{ item.name }}
      <v-tooltip bottom v-if="item.searchable === false">
        <template v-slot:activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on" class="ml-2">mdi-link</v-icon>
        </template>
        <span>{{ $t("exercise.unlisted") }}</span>
      </v-tooltip>
    </v-card-title>
    <v-card-subtitle v-if="item.description">
      {{ item.description }}
    </v-card-subtitle>
    <v-divider></v-divider>
    <v-card-text class="pa-2">
      <ExerciseFooterAttributes :exercise="item"></ExerciseFooterAttributes>
    </v-card-text>
  </v-card>
</template>
<script>
import langs_available from "~/mixins/langs_available.js"
import cefr from "~/mixins/cefr.js"
export default {
  name: "ExerciseListItem",
  mixins: [langs_available, cefr],
  props: ["item"],
}
</script>
