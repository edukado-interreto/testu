<template>
  <v-container>

    <v-breadcrumbs
      class="pt-0 pl-0"
      :items='breadcrumbs'
    >
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>

    <div
      class="d-flex justify-space-between flex-column flex-sm-row"
    >
      <div>
        <h1>{{ exam.name }}</h1>
        <div class="text-caption">
          Created: {{ exam.created.toLocaleString('en-US') }}
        </div>
      </div>
      <div class="d-flex my-3 my-sm-0 ml-0 ml-sm-4 pt-1">
        <v-btn class="mr-2">
          <v-icon class="me-1">mdi-eye</v-icon>
          View exam
        </v-btn>
        <v-menu offset-y>
          <template v-slot:activator="{on, attrs}">
            <v-btn icon v-bind="attrs" v-on="on">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-link-variant</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                Copy exam link
              </v-list-item-title>
            </v-list-item><v-list-item color="error">
              <v-list-item-icon>
                <v-icon class="error--text">mdi-delete</v-icon>
              </v-list-item-icon>
              <v-list-item-title class="error--text font-weight-bold">
                Delete exam
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </div>


    <div class="mt-4 mb-10">
      <nuxt-link
        :to="localePath(`/exercise/${id}`)"
      >
        <v-icon>mdi-file-outline</v-icon>
        Go to the exercise
      </nuxt-link>
    </div>

    <v-switch
      label="Accepting submissions"
      v-model="exam.accepts_submissions"
    >
    </v-switch>
    
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
    breadcrumbs() {
      return [
        { text: this.$t('main.my_teaching'), href: this.localePath('teach'), disabled: false },
        { text: 'Exams', href: this.localePath('teach')+'#exams', disabled: false },
        { text: this.exam.name, disabled: true },
      ]
    },
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
