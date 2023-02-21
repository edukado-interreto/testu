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
        <v-btn class="mr-2" :disabled="!exam.lid">
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


    <div class="mt-4 mb-10">
      <nuxt-link
        :to="localePath(`/exercise/${exam.exercise}`)"
      >
        <v-icon>mdi-file-outline</v-icon>
        Go to the exercise
      </nuxt-link>
    </div>

    <v-switch
      :disabled="!exam.lid"
      label="Accept new submissions"
      v-model="exam.accept_submission"
    >
    </v-switch>

    <div v-if="exam.submissions">
      <ExamSubmissions
        :submissions="exam.submissions"
      ></ExamSubmissions>
    </div>
    <div
      v-if="exam.lid && !exam.submissions"
      class="pa-9 text--disabled text-h6 grey lighten-4 rounded"
    >
      No submissions
    </div>

    <v-sheet elevation="2" rounded class="pa-4 mt-5">
      <v-text-field
        label="Name"
        v-model="exam.name"
      ></v-text-field>
      <v-textarea
        label="Description"
        v-model="exam.description"
        auto-grow
        rows="1"
      ></v-textarea>

      <v-btn
        class="my-3 primary--text"
        large
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
    exam: {
      accept_submission: true,
    },
  }),
  async fetch() {
    const exam_id = this.$route.query.exam
    const new_from = this.$route.query.new_from
    if (new_from) {
      //const exercise = (
      //  await this.$auth.axios.get(`/v1/exercises/${new_from}/`)
      //).data
      //console.log(exercise)
      this.$set(this.exam, 'exercise', new_from)
      // FIXME: should be: this.exam.exercise_lid
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
    async save() {
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

      try {
        const ret = await this.$auth.axios({
          url: api.path,
          method: api.method,
          data: this.exam,
        })
        console.log(ret.data)
        if (!this.exam.lid) {
          // this.$router.replace... // query.id=lid
        }
      } catch(e) {
        console.error({...e});
        if (e.response.status >= 400) {
          await this.$refs.msgbox.alert(`Server error (${e.response.status})`)
        }
      }

    }
  }
}
</script>
<style scoped>
  a { text-decoration: none; }
</style>
