<template>
  <v-container>

    <v-card
      max-width="600"
      elevation="1"
      class="mb-4"
    >
      <v-card-text class="d-block d-sm-flex align-baseline">
        <div class="text-h6 font-weight-light grey--text text--darken-3">
          Recent activity
        </div>
        <div class="subheading ms-0 ms-sm-4 grey--text">
          Submitted exercises per day
        </div>
      </v-card-text>
      <v-sheet
      >
        <v-sparkline
          :labels="stats.labels"
          :value="stats.values"
          :gradient="['red', 'orange', 'yellow']"
          stroke-linecap="round"
          :smooth="true"
          line-width="2"
          padding="16"
          auto-draw
          type="trend"
          height="60"
        ></v-sparkline>
      </v-sheet>
    </v-card>

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

    submissions.forEach(s => s.created = new Date(s.created))
    return {
      submissions
    }
  },
  computed: {
    table() {
      const items = this.submissions.map( s => ({
        pk: s.pk,
        created: s.created,
        is_exam: !!s.exam_lid,
        exercise_name: s.exercise.name,
      }))
      const headers = [
        { text: 'Exercise', value: 'exercise_name', sortable: false },
        { text: '', value: 'is_exam', sortable: false },
        { text: 'Date', value: 'created', sortable: false },
        { text: '', value: 'actions', sortable: false },
      ]
      return { headers, items }
    },
    stats() {
      const days = {}

      this.submissions.forEach(s => {
        const dateWithoutTime = (
          new Date(s.created)
        ).setHours(0,0,0,0) // as int
        days[dateWithoutTime] = days[dateWithoutTime]+1 || 1
      })
      // days = {1676588400000: 2, 1677106800000: 9}

      const days_array = Object.entries(days).sort(
        (a, b) => a[0]-b[0] // oldest to newest
      ).map(a => ({
        day: (new Date(a[0]*1)).toLocaleString('en-US', { dateStyle: 'short' }),
        value: a[1],
      }))
      // days_array = [
      //   { "day": "2/17/23", "value": 2 },
      //   { "day": "2/23/23", "value": 9 }
      // ]

      const empties = [...Array(7 - days_array.length)].map(a => ({ day: "·", value: 0 }))
      days_array.unshift(...empties)
      // pad the array to 7 elements, prepending empty values if needed
      // days_array = [
      //   { "day": "·", "value": 0 },
      //   { "day": "·", "value": 0 },
      //   { "day": "·", "value": 0 },
      //   { "day": "·", "value": 0 },
      //   { "day": "·", "value": 0 },
      //   { "day": "2/17/23", "value": 2 },
      //   { "day": "2/23/23", "value": 9 }
      // ]

      console.log(days_array)

      return {
        labels: days_array.map(a => a.day),
        values: days_array.map(a => a.value),
      }
      // {
      //   "labels": [ "2/17/23", "2/23/23" ],
      //   "values": [ 2, 9 ]
      // }

    },
  },
  middleware: 'redirects',
  meta: {
    requiresAuth: true
  }
}
</script>
