<template>
  <v-container>
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
    this.exercises = (
      await this.$auth.axios.get('/v1/sheets/')
    ).data
  },
  fetchOnServer: true,
  fetchKey: 'exercises',
  middleware: 'redirects',
  meta: {
    requiresAuth: true
  }
}
</script>

