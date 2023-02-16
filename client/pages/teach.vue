<template>
  <v-container>
    <v-tabs v-model="tab">
      <v-tab>Exercises</v-tab>
      <v-tab>Exams</v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab" class="pa-1 mt-5">
      <!-- exercises -->
      <v-tab-item>
        <v-data-iterator
          class="mt-5"
          :items="filtered_exercises"
          :items-per-page="15"
        >
          <template v-slot:default="props">
            <ExerciseListItem
              v-for="item in props.items"
              :item="item"
              :key="item.id"
            >
            </ExerciseListItem>
          </template>
        </v-data-iterator>
      </v-tab-item>

      <!-- exams -->
      <v-tab-item>
        <v-card :to="localePath(`/review/0`)">
          <v-card-title>
            Exams list item
          </v-card-title>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
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
    tab: 0,
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
    this.exercises = (
      await this.$auth.axios.get('/v1/exercises/')
    ).data.results // FIXME: pagination
  },
  fetchOnServer: true,
  fetchKey: 'exercises',
  middleware: 'redirects',
  meta: {
    requiresAuth: true
  }
}
</script>

