<template>
  <v-container>
    <v-alert
      icon="mdi-school"
      text
      color="primary"
      prominent
      class="mb-8 pa-sm-12"
    >
      <div class="text-h6">
        This is an exam
      </div>
      <div>
        The results of this exercise will be visible to the examinator <strong>{{ exam.created_by }}</strong>.
      </div>
    </v-alert>

    <div
      v-if="!submitter_display_name && !logged_in"
    >
      <p class="text-center text-body-2 mt-12 mb-7">
        To proceed to the exam, please log in or choose a display name.
      </p>
      <v-row justify="center" class="mt-3">
        <v-col cols="12" sm="4" md="2" align="center">
          <v-btn color="primary" block>Log in</v-btn>
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

  </v-container>
</template>
<script>
export default {
  data: () => ({
    submitter_display_name: "",
    display_name_vmodel: "",
    exam: {
      name: 'Examination Esperanto B1, classroom A',
      exercise_id: 24,
      created: new Date(),
      exam_url: 'https://example.org',
      created_by: 'etuardu',
      accepts_submissions: true,
    }
  }),
  async asyncData({ route, params }) {
    const id = (process.server) ? route.params.id : params.id
    return {
      id
    }
  },
  computed: {
    logged_in() {
      return this.authUser && this.authUser.username !== undefined
    },
    authUser() {
      return this.$store.getters['authenticator/authUser']
    }
  },
}
</script>
