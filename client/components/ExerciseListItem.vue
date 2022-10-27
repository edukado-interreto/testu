<template>
  <v-card
    :to="`/exercise/${item.id}`"
    nuxt
    class="mb-5"
  >
    <v-card-title
      class="subheading font-weight-bold"
    >
      {{ item.name }}
      <v-tooltip bottom v-if="item.searchable === false">
        <template
          v-slot:activator="{on, attrs}"
        >
          <v-icon
            v-bind="attrs"
            v-on="on"
            class="ml-2"
          >mdi-link</v-icon>
        </template>
        <span>This exercise is unlisted in search results</span>
      </v-tooltip>
    </v-card-title>
    <v-card-subtitle v-if="item.description">
      {{ item.description }}
    </v-card-subtitle>
    <v-card-text class="text-caption">
      <div v-if="item.age_min > 0 || item.age_max < 18">
        Age: {{ item.age_min }} - {{ (item.age_max == 18) ? '18+' : item.age_max  }}
      </div>
      <div v-if="item.lang_learn === true">
        Language learning: {{ langs_table[item.lang_learn_lang].name }} {{ cefr_info(item) }}
      </div>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-text>
      <v-icon small>mdi-account</v-icon> {{ item.created_by || 'anonymous' }}
      <span>·</span>
      <v-icon small>mdi-clock</v-icon> {{ date_formatted(item.created) }}
    </v-card-text>
  </v-card>

</template>
<script>
import langs_available from '~/mixins/langs_available.js'
import cefr from '~/mixins/cefr.js'
export default {
  name: 'ExerciseListItem',
  mixins: [
    langs_available,
    cefr
  ],
  props: [ 'item' ],
  methods: {
    date_formatted(d) {
      return (
        new Date(d)
      ).toLocaleString("en-US") // TODO: i18n 
    },
  }
}
</script>
