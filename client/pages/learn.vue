<template>
  <v-container>
    <v-data-table
      :items="table.items"
      :headers="table.headers"
      sort-by="created"
      :sort-desc="true"
    >
      <template v-slot:item.is_exam="{ item }">
        <v-chip class="primary" v-if="item.is_exam">Exam</v-chip>
      </template>
      <template v-slot:item.created="{ item }">
        {{ item.created.toLocaleString("en-US") }}
      </template>
      <template v-slot:item.actions="{ item }">
        <v-btn small depressed nuxt :to="localePath(`/review/${item.pk}`)">
          Review
        </v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>
<script>
export default {
  data: () => ({
  }),
  async asyncData({ $auth }) {
    const submissions = (
      await $auth.axios.get('/v1/submissions/')
    ).data.results
    return {
      submissions
    }
  },
  computed: {
    table() {
      const items = this.submissions.map( s => ({
        pk: s.pk,
        created: new Date(s.created),
        is_exam: !!s.exam_lid,
        exercise_name: s.exercise.name,
      }))
      const headers = [
        { text: 'Exercise', value: 'exercise_name' },
        { text: '', value: 'is_exam', sortable: false },
        { text: 'Date', value: 'created' },
        { text: '', value: 'actions', sortable: false },
      ]
      return { headers, items }
    }
  }
}
</script>
