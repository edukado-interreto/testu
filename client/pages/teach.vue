<template>
  <v-container>
    <v-data-iterator
      class="mt-5"
      :items="filtered_exercises"
      :items-per-page="15"
    >
      <template v-slot:default="props">
        <v-row>
          <v-col
            v-for="item in props.items"
            :key="item.id"
            cols="12"
          >
            <v-card
              :to="`/exercise/${item.id}`"
              nuxt
            >
              <v-card-title
                class="subheading font-weight-bold"
              >
                {{ item.name }}
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
          </v-col>
        </v-row>
      </template>
    </v-data-iterator>
  </v-container>
</template>
<script>
import langs_available from '~/mixins/langs_available.js'
import cefr from '~/mixins/cefr.js'
export default {
  name: 'Teach',
  head() {
    return {
      title: 'My teaching'
    }
  },
  mixins: [
    langs_available,
    cefr
  ],
  data: () => ({
    exercises: [],
  }),
  computed: {
    current_username() {
      const authUser = this.$store.getters['authenticator/authUser']
      if (!authUser) return null
      return authUser.username
    },
    filtered_exercises() {
      return this.exercises.filter(
        e => e.created_by == this.current_username
      ).sort(
        // newest to oldest
        (a, b) => new Date(b.created) - new Date(a.created)
      )
    }
  },
  methods: {
    date_formatted(d) {
      return (
        new Date(d)
      ).toLocaleString("en-US") // TODO: i18n
    },
  },
  async fetch() {
    this.exercises = await (
      await fetch('/api/v1/sheets/')
    ).json();
  },
  fetchOnServer: true,
  fetchKey: 'exercises',
  middleware: 'redirects',
  meta: {
    requiresAuth: true
  }
}
</script>

