<template>
  <v-row dense class="text-caption">
    <v-col cols="auto">
      <v-icon small>mdi-account</v-icon>
      {{ exercise.created_by || $t('exercise.anonymous') }}
    </v-col>
    <v-col cols="auto">
      <v-icon small>mdi-clock</v-icon> {{ date_formatted }}
    </v-col>
    <v-spacer></v-spacer>
    <v-col cols="auto" v-if="exercise.age_min > 0 || exercise.age_max < 18">
      <v-icon small>mdi-human-child</v-icon> {{ $t("exercise.age") }}
      {{ exercise.age_min }} -
      {{ exercise.age_max == 18 ? "18+" : exercise.age_max }}
    </v-col>
    <v-col cols="auto" v-if="exercise.lang_learn === true">
      <v-icon small>mdi-chat</v-icon>
      {{ langs_table[exercise.lang_learn_lang].name }} {{ cefr_info(exercise) }}
    </v-col>
    <v-col cols="auto" v-if="exercise.tags?.length > 0">
      <v-icon small>mdi-tag</v-icon>
      {{ tags_localized.join(", ") }}
      <!-- TODO: i18n -->
    </v-col>
  </v-row>
</template>
<script>
import cefr from "~/mixins/cefr.js";
import langs_available from "~/mixins/langs_available.js";
export default {
  props: ["exercise"],
  mixins: [langs_available, cefr],
  computed: {
    tags_localized() {
      return (this.exercise.tags || []).map((t) => this.$t(`tags.${t}`));
    },
    date_formatted() {
      return new Date(this.exercise.modified).toLocaleString("en-US"); // TODO: i18n
    },
  },
};
</script>
