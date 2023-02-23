<template>
  <v-container>
    <MsgBox ref="msgbox"></MsgBox>

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
        <h1 :class="{ 'font-italic': !exam.name }">
          {{ exam.name || 'Untitled exam' }}
        </h1>
        <div class="text-caption" v-if="exam.created">
          Created: {{ exam.created?.toLocaleString('en-US') }}
        </div>
      </div>
      <div class="d-flex my-3 my-sm-0 ml-0 ml-sm-4 pt-1">
        <v-btn
          class="mr-2 primary--text"
          :disabled="!exam.lid"
          nuxt
          :to="localePath(`/exam/${exam.lid}`)"
          text
        >
          <v-icon class="me-1">mdi-eye</v-icon>
          View exam
        </v-btn>
        <v-menu offset-y>
          <template v-slot:activator="{on, attrs}">
            <v-btn icon v-bind="attrs" v-on="on" :disabled="!exam.lid">
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


    <div class="mt-4 mb-5">
      <nuxt-link
        :to="localePath(`/exercise/${exam.exercise_lid}`)"
      >
        <v-icon>mdi-file-outline</v-icon>
        Go to the exercise
      </nuxt-link>
    </div>

    <v-row no-gutters>
      <v-col cols="auto">
        <v-switch
          :disabled="!exam.lid"
          label="Accept new submissions"
          v-model="exam.accept_submission"
        >
        </v-switch>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>

    <div
      v-if="submissions.length > 0"
      class="mt-5 mb-15"
    >
      <ExamSubmissions
        :submissions="submissions"
      ></ExamSubmissions>
    </div>
    <template v-else>
      <div
        v-if="exam.lid"
        class="pa-9 text--disabled text-h6 grey lighten-4 rounded mb-10"
      >
        No submissions
      </div>
    </template>

    <v-sheet elevation="2" rounded class="pa-4 mt-5">
      <v-text-field
        label="Exam name"
        v-model="exam.name"
      ></v-text-field>
      <v-textarea
        label="Exam description"
        v-model="exam.description"
        auto-grow
        rows="1"
      ></v-textarea>

      <v-btn
        class="my-3 primary--text"
        large
        :loading="is_saving"
        text
        @click="save"
      >
        <v-icon class="mr-2">mdi-content-save</v-icon>
        Save
      </v-btn>

    </v-sheet>
  </v-container>
</template>
<script>
export default {
  data: () => ({
    is_saving: false,
    exam: {
      accept_submission: true,
    },
    submissions: [],
  }),
  async fetch() {
    const exam_id = this.$route.query.exam
    const new_from = this.$route.query.new_from
    if (new_from) {
      //const exercise = (
      //  await this.$auth.axios.get(`/v1/exercises/${new_from}/`)
      //).data
      //console.log(exercise)
      this.$set(this.exam, 'exercise_lid', new_from)
    }
    if (exam_id) {
      this.exam = (
        await this.$auth.axios.get(`/v1/exams/${exam_id}/`)
      ).data
      this.exam.created = new Date(this.exam.created)
      console.log("loaded exam", this.exam)
      this.fetch_exam_submissions(exam_id)
    }
  },
  computed: {
    breadcrumbs() {
      return [
        { text: this.$t('main.my_teaching'), href: this.localePath('teach'), disabled: false },
        { text: 'Exams', href: this.localePath('teach')+'#exams', disabled: false },
        { text: this.exam.name || 'Untitled exam', disabled: true },
      ]
    },
  },
  methods: {
    async fetch_exam_submissions(id) {
      const submissions = (
        await this.$auth.axios.get(`/v1/exams/${id}/submissions/`)
      ).data
      submissions.forEach(s => s.created = new Date(s.created))
      this.submissions = submissions
    },
    async save() {
      if (!this.exam.name) {
        await this.$refs.msgbox.alert("Please choose a name for the exam")
        return
      }

      this.is_saving = true
      console.log("saving:", this.exam)

      const api = {
        path: '/v1/exams/',
        method: 'POST'
      }
      if (this.exam.lid) {
        api.path = `/v1/exams/${this.exam.lid}/`
        api.method = 'PUT'
      }

      console.log("request:", api)

      let ret = undefined
      try {
        ret = await this.$auth.axios({
          url: api.path,
          method: api.method,
          data: this.exam,
        })
      } catch(e) {
        console.error({...e});
        await this.$refs.msgbox.alert(`Server error (${e.response.status})`)
        return
      } finally {
        this.is_saving = false
      }

      console.log(ret.data)

      if (!this.exam.lid) {
        // the exercise was just created.
        // We replace the url /?new_from=...
        // with /?exam=<lid>
        this.$router.replace({ query: { exam: ret.data.lid } })
      }
      this.exam = ret.data

      window.scrollTo({ top:0, behavior: 'smooth'})

    }
  }
}
</script>
<style scoped>
  a { text-decoration: none; }
</style>
