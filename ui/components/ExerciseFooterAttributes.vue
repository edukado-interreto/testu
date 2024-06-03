<script setup lang="ts">
const { t } = useI18n()
const unit_component = useUnitComponent()
const { cefr_info } = useCefr()
const { langs_table, langs_available } = useLangsAvailable()

const props = defineProps<{ exercise: Exercise }>()

const tags_localized = computed(() => {
  return (props.exercise.tags || []).map((tag) => t(`tags.${tag}`))
})
</script>

<template>
  <v-row dense class="text-caption text-medium-emphasis d-print-none">
    <v-col cols="auto">
      <v-icon small>mdi-account</v-icon>
      {{ exercise.created_by || $t("exercise.anonymous") }}
    </v-col>
    <v-col cols="auto" v-if="exercise.modified">
      <v-icon small>mdi-clock</v-icon>
      {{ $d(new Date(exercise.modified), "long") }}
    </v-col>
    <v-spacer />
    <v-col cols="auto" v-if="exercise.age_min > 0 || exercise.age_max < 18">
      <v-icon small>mdi-human-child</v-icon>
      {{ $t("exercise.age") }} {{ exercise.age_min }} -
      {{ exercise.age_max == 18 ? "18+" : exercise.age_max }}
    </v-col>
    <v-col cols="auto" v-if="exercise.lang_learn === true">
      <v-icon small>mdi-chat</v-icon>
      {{ langs_table[exercise.lang_learn_lang].name }}
      {{ cefr_info(exercise) }}
    </v-col>
    <v-col cols="auto" v-if="exercise.tags?.length > 0">
      <v-icon small>mdi-tag</v-icon>
      {{ tags_localized.join(", ") }}
    </v-col>
    <v-col cols="auto">
      <v-icon small>mdi-heart</v-icon>
      {{ exercise.likes }}
    </v-col>
  </v-row>
</template>
