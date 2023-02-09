<template>
  <v-container>
    <v-row align="center">
      <v-col>
        <h1>{{ exam.name }}</h1>
          <a
            :href="localePath(`/exercise/${exam.exercise_id}`)"
            target="blank"
          >
            <v-icon class="pb-1">mdi-file-outline</v-icon>
            Exercise
          </a>
        </v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn>
          <v-icon>mdi-link</v-icon>
        </v-btn>
        <v-btn class="error">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <v-row class="mt-0" align="center" mb="0">
      <v-col>
        <v-switch
          label="Accepting submissions"
          v-model="exam.accepts_submissions"
        >
        </v-switch>
      </v-col>
      <v-col cols="auto" class="text-caption">
        Created: {{ exam.created.toLocaleString('en-US') }}
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-select
          outlined
          dense
          :items="submissions_items"
          v-model="submissions_index"
        ></v-select>
      </v-col>
      <v-col>
        <v-btn
          icon
          @click="submissions_index -= 1"
          :disabled="submissions_index == 0"
        ><v-icon>mdi-chevron-left</v-icon></v-btn>
        {{ nth_of_total }}
        <v-btn
          icon
          @click="submissions_index += 1"
          :disabled="submissions_index == submissions_items.length-1"
        ><v-icon>mdi-chevron-right</v-icon></v-btn>
      </v-col>
    </v-row>

    <p class="text-caption">
      Right answers:
      <v-progress-circular
        :value="current_submission.score*100"
        :rotate="270"
        :size="25"
        :width="6"
        color="primary"
      >
      </v-progress-circular>
      {{ current_submission.score * 100 }}%
    </p>

  </v-container>
</template>
<script>
export default {
  data: () => ({
    submissions_index: 0,
    exam: {
      name: 'Examination Esperanto B1, classroom A',
      exercise_id: 24,
      created: new Date(),
      exam_url: 'https://example.org',
      created_by: 'etuardu',
      accepts_submissions: true,
      submissions: [
        {
          submitted: new Date(2023, 1, 2, 9, 11, 13),
          score: 0.65,
          author: {
            display_name: 'edoardo',
            user_id: 'edoardo'
          },
        },
        {
          submitted: new Date(2023, 1, 2, 16, 4, 5),
          score: 0.4,
          author: {
            display_name: 'Mario',
            user_id: null
          },
        },
        {
          submitted: new Date(2023, 1, 2, 9, 11, 13),
          score: 0.5,
          author: {
            display_name: 'edoardo',
            user_id: 'edoardo'
          },
        },
      ]
    }
  }),
  async asyncData({ route, params }) {
    const id = (process.server) ? route.params.id : params.id
    return {
      id
    }
  },
  computed: {
    nth_of_total() {
      const of = 'of'
      const len = this.submissions_items.length
      if (len == 0) return `0 ${of} 0`
      return `${this.submissions_index+1} ${of} ${len}`
    },
    current_submission() {
        return this.submissions_items[this.submissions_index].data
    },
    submissions_items() {
      return this.exam.submissions.sort(
        (a, b) => b.submitted - a.submitted
      ).map((e, i) => ({
        value: i,
        text: (
          e.author.display_name + ' (' +
          e.submitted.toLocaleString('en-US') +
          ')'
        ),
        data: e,
      }))
    }
  }
}
</script>
<style scoped>
  a { text-decoration: none; }
</style>
