<template>
  <v-data-iterator
    class="mt-5"
    :items="filtered_exams"
    :items-per-page="15"
  >
    <template v-slot:default="props">
      <ExamListItem
        v-for="item in props.items"
        :item="item"
        :key="item.lid"
      >
      </ExamListItem>
    </template>
  </v-data-iterator>
</template>
<script>
export default {
  data: () => ({
    exams: [],
  }),
  computed: {
    current_username() {
      const authUser = this.$store.getters['authenticator/authUser']
      if (!authUser) return null
      return authUser.username
    },
    filtered_exams() {
      return this.exams.filter(
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
    this.exams = (
      await this.$auth.axios.get('/v1/exams/')
    ).data.results // FIXME: pagination
  },
  fetchOnServer: true,
  fetchKey: 'exams',
}
</script>
