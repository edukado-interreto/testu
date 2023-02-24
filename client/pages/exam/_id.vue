<template>
  <v-container>
    <MsgBox ref="msgbox"></MsgBox>
    <v-alert
      icon="mdi-school"
      text
      color="primary"
      prominent
      class="mb-8 pa-sm-12"
    >
      <template
        v-if="exam.accept_submission"
      >
        <div class="text-h6">
          This is an exam
        </div>
        <div>
          The results of this exercise will be visible to the examinator <strong>{{ exam.created_by }}</strong>.
        </div>
      </template>
      <template
        v-else
      >
        <div class="text-h6">
          This exam does not accept new submissions
        </div>
      </template>
    </v-alert>

    <div
      v-if="!submitter_display_name && !logged_in && exam.accept_submission"
    >
      <p class="text-center text-body-2 mt-12 mb-7">
        To proceed to the exam, please log in or choose a display name.
      </p>
      <v-row justify="center" class="mt-3">
        <v-col cols="12" sm="4" md="2" align="center">
          <v-btn color="primary" block @click="login">Log in</v-btn>
        </v-col>
        <v-col cols="12" sm="1" md="1" align="center">
          or
        </v-col>
        <v-col cols="12" sm="6" md="4" align="center">
          <v-text-field
            outlined
            dense
            v-model="display_name_vmodel"
            label="Display name"
            placeholder="Choose a display name…"
            persistent-placeholder
          >
            <template v-slot:append-outer>
              <v-btn small @click="submitter_display_name = display_name_vmodel">Ok</v-btn>
            </template>
          </v-text-field>
        </v-col>
      </v-row>
    </div>

    <div v-if="should_exercise_be_shown">
      
      <v-row>
        <v-col>
          <h1>{{ exam.name }}</h1>
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="auto">
          <v-btn
            class="primary--text"
            v-if="current_username == exam.created_by"
            text
            nuxt
            :to="localePath(`/exam_editor?exam=${id}`)"
          >
            <v-icon class="me-1">mdi-pencil</v-icon>
            Edit
          </v-btn>
        </v-col>
      </v-row>

      <v-row dense class="text-caption mb-6">
      <v-col cols="auto">
        <v-icon small>mdi-account</v-icon> {{ exam.created_by || 'anonymous' }}
      </v-col>
      <v-col cols="auto">
        <v-icon small>mdi-clock</v-icon> {{ exam.created.toLocaleString('en-US')  }}
      </v-col>
    </v-row>

      <v-sheet v-if="exam.description" class="mb-7">
        {{ exam.description }}
      </v-sheet>

      <h2>{{ exercise.name }}</h2>

      <v-sheet v-if="exercise.description" class="mt-3 mb-7">
        {{ exercise.description }}
      </v-sheet>

      <v-sheet
        v-for="(unit, i) in exercise.data.sheet"
        :key="unit._key"
      >
        <div class="headline my-4"> 
          {{ i+1 }}. {{ unit.title }}
          <span v-if="unit.title === ''" class="font-italic">
            Untitled unit
          </span>
        </div>
        <div
          v-if="unit.description"
          class="body-2 mb-4 pre-line"
        >
          <RichContent
            :text="unit.description"
          >
          </RichContent>
        </div>
        <component
          :is="unit_component(unit.type)"
          :code="unit.code"
          :shuffle="unit.shuffle"
          :ignore_case="unit.ignore_case"
          :silent="all_silent"
          :readonly="all_readonly"
          ref="unit"
        />
      </v-sheet>

      <v-alert
        text
        color="primary"
        class="mb-0 mt-10"
        v-if="submitted"
      >
        Well done, your exam has been submitted to the examinator!
      </v-alert>

      <v-btn
        @click="submit"
        class="mt-9 primary"
        :disabled="submitted || !exam.accept_submission"
        :loading="is_submitting"
      >Submit</v-btn>

    </div>

  </v-container>
</template>
<script>
import unit_component from '~/mixins/unit_component.js'
export default {
  mixins: [
    unit_component,
  ],
  data: () => ({
    is_submitting: false,
    submitter_display_name: "",
    display_name_vmodel: "",
    submitted: false,
    all_silent: true,
    all_readonly: false,
  }),
  async asyncData({ $auth, route, params }) {
    const id = (process.server) ? route.params.id : params.id
    const exam = (
      await $auth.axios.get(`/v1/exams/${id}`)
    ).data
    exam.created = new Date(exam.created)
    const exercise = (
      await $auth.axios.get(`/v1/exercises/${exam.exercise_lid}`)
    ).data
    return {
      id,
      exam,
      exercise,
    }
  },
  computed: {
    logged_in() {
      return this.authUser && this.authUser.username !== undefined
    },
    authUser() {
      return this.$store.getters['authenticator/authUser']
    },
    current_username() {
      const authUser = this.$store.getters['authenticator/authUser']
      if (!authUser) return null
      return authUser.username
    },
    should_exercise_be_shown() {
      if (this.current_username == this.exam.created_by) return true
      if (!this.exam.accept_submission) return false
      if (this.submitter_display_name || this.logged_in) return true
      return false
    }
  },
  methods: {
    login() {
      // navigate to the login screen, setting
      // the current route as post-login redirect url
      this.$store.commit(
        "authenticator/updateRedirectUrl", 
        this.$route.path
      )
      this.$router.push(this.localePath('/login'))
    },
    create_submission() {
      // create the submission object to be sent to the server

      const submission = {}

      if (this.current_username) {
        submission.created_by = this.current_username
      } else {
        submission.guest = this.submitter_display_name
      }

      submission.created = new Date()
      submission.exercise_lid = this.exam.exercise_lid
      submission.exam_lid = this.exam.lid
      submission.exercise = { ...this.exercise }
      submission.exercise.data.sheet = this.exercise.data.sheet.map(
        (unit, i) => ({
          ...unit,
          solved: this.$refs.unit[i].get_solved()
        })
      )

      return submission
    },
    async submit() {

      if (!(await this.$refs.msgbox.confirm(
        "This operation cannot be undone. Proceed?"
      ))) return 

      this.is_submitting = true
      this.all_readonly = true

      const submission = this.create_submission()

      try {
        await this.$auth.axios.post('/v1/submissions/', submission)
      } catch(e) {
        console.error({...e})
        await this.$refs.msgbox.alert("An error occurred while submitting the exam.")
        return
      } finally {
        this.is_submitting = false
      }

      this.submitted = true
      
    }
  }
}
</script>
