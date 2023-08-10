<template>
  <v-container>
    <MsgBox ref="msgbox"></MsgBox>

    <v-breadcrumbs class="pt-0 pl-0" :items="breadcrumbs">
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>
    <v-row>
      <v-col>
        <h1 :class="{ 'font-italic': !exam.name }">
          {{ exam.name || $t("exam.untitled") }}
        </h1>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="auto">
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on" :disabled="!exam.lid">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item color="error" @click="delete_exam">
              <v-list-item-icon>
                <v-icon class="error--text">mdi-delete</v-icon>
              </v-list-item-icon>
              <v-list-item-title class="error--text font-weight-bold">
                {{ $t("exam.delete") }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-col>
    </v-row>
    <p class="text-caption" v-if="exam.created">
      {{ $t("exam.created", { date: $d(new Date(exam.created), "dt") }) }}
    </p>

    <v-row no-gutters class="mt-4">
      <v-col cols="12" sm="6">
        <nuxt-link :to="localePath(`/exercise/${exam.exercise_lid}`)">
          <v-icon>mdi-file-outline</v-icon>
          {{ $t("exam.goto_exercise") }}
        </nuxt-link>
      </v-col>
      <v-col v-if="exam.lid">
        <t-CopyTextField
          :value="sharable_link"
          :label="$t('exam.link')"
        ></t-CopyTextField>
      </v-col>
      <v-col v-if="exam.lid" class="flex-shrink-1 flex-grow-0">
        <v-btn
          :disabled="!exam.lid"
          :to="localePath(`/exam/${exam.lid}`)"
          class="primary--text"
          nuxt
          text
        >
          {{ $t("exam.view") }}
        </v-btn>
      </v-col>
    </v-row>

    <v-row no-gutters>
      <v-col cols="auto">
        <v-switch
          :disabled="!exam.lid"
          :label="$t('exam.accept_submissions')"
          v-model="exam.accept_submission"
          @change="toggle_accept_submission"
          :loading="is_toggling_accept_submission"
        ></v-switch>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>

    <div v-if="submissions.length > 0" class="mt-5 mb-15">
      <ExamSubmissions :submissions="submissions"></ExamSubmissions>
    </div>
    <template v-else>
      <div
        v-if="exam.lid"
        class="pa-9 text-h5 grey--text grey lighten-4 rounded mb-10"
      >
        <v-icon large class="grey--text me-1 pb-1">mdi-inbox</v-icon>
        {{ $t("exam.no_submissions") }}
      </div>
    </template>

    <v-expansion-panels class="mt-9" v-model="infobox">
      <v-expansion-panel>
        <v-expansion-panel-header>
          <template v-slot:default="{ open }">
            {{ $t("exam.details") }}
            <span class="ml-5 text--disabled" v-if="!open">
              <span v-if="exam.name">{{ exam.name }}</span>
              <span v-else class="font-italic">{{ $t("exam.untitled") }}</span>
            </span>
          </template>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-text-field
            :label="$t('exam.name')"
            v-model="exam.name"
            maxlength="100"
          ></v-text-field>
          <v-textarea
            :label="$t('exam.description')"
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
            {{ $t("editor.save") }}
          </v-btn>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>
<script>
export default {
  data: () => ({
    is_saving: false,
    is_toggling_accept_submission: false,
    exam: {
      accept_submission: true,
    },
    submissions: [],
    infobox: 0, // 0 = open, undefined = closed
  }),
  async fetch() {
    const exam_id = this.$route.query.exam
    const new_from = this.$route.query.new_from
    if (new_from) {
      //const exercise = (
      //  await this.$auth.axios.get(`/v1/exercises/${new_from}/`)
      //).data
      //console.log(exercise)
      this.$set(this.exam, "exercise_lid", new_from)
    }
    if (exam_id) {
      this.infobox = undefined // expansion panel closed
      this.exam = (await this.$auth.axios.get(`/v1/exams/${exam_id}/`)).data
      this.exam.created = new Date(this.exam.created)
      console.log("loaded exam", this.exam)
      this.fetch_exam_submissions(exam_id)
    }
  },
  computed: {
    breadcrumbs() {
      return [
        {
          text: this.$t("main.my_teaching"),
          href: this.localePath("teach"),
          disabled: false,
        },
        {
          text: "Exams",
          href: this.localePath("teach") + "#exams",
          disabled: false,
        },
        { text: this.exam.name || "Untitled exam", disabled: true },
      ]
    },
    sharable_link() {
      return new URL(
        this.localePath(`/exam/${this.exam.lid}`),
        window.location.origin,
      ).href
    },
  },
  methods: {
    async delete_exam() {
      if (!this.exam.lid) return
      if (
        !(await this.$refs.msgbox.confirm(
          "Are you sure you want to delete this exam?",
        ))
      )
        return
      try {
        await this.$auth.axios.delete(`/v1/exams/${this.exam.lid}/`)
      } catch (e) {
        console.error({ ...e })
        await this.$refs.msgbox.alert(`Server error (${e.response.status})`)
        return
      }
      this.$router.push(this.localePath("teach") + "#exams")
    },
    async fetch_exam_submissions(id) {
      const submissions = (
        await this.$auth.axios.get(`/v1/exams/${id}/submissions/`)
      ).data
      submissions.forEach((s) => (s.created = new Date(s.created)))
      this.submissions = submissions
    },
    async toggle_accept_submission(value) {
      if (!this.exam.lid) return

      const confirm_text = value
        ? "New submissions to the exam will be accepted. Proceed?"
        : "This exam will no longer accept new submissions. Proceed?"

      if (!(await this.$refs.msgbox.confirm(confirm_text))) {
        this.exam.accept_submission = !value
        return
      }

      this.is_toggling_accept_submission = true
      try {
        await this.$auth.axios.patch(`/v1/exams/${this.exam.lid}/`, {
          accept_submission: value,
        })
      } catch (e) {
        this.exam.accept_submission = !value
        console.error({ ...e })
        await this.$refs.msgbox.alert(`Server error (${e.response.status})`)
      } finally {
        this.is_toggling_accept_submission = false
      }
    },
    async save() {
      if (!this.exam.name) {
        await this.$refs.msgbox.alert("Please choose a name for the exam")
        return
      }

      this.is_saving = true
      console.log("saving:", this.exam)

      const api = {
        path: "/v1/exams/",
        method: "POST",
      }
      if (this.exam.lid) {
        api.path = `/v1/exams/${this.exam.lid}/`
        api.method = "PUT"
      }

      console.log("request:", api)

      let ret = undefined
      try {
        ret = await this.$auth.axios({
          url: api.path,
          method: api.method,
          data: this.exam,
        })
      } catch (e) {
        console.error({ ...e })
        const resp = e.response
        if (resp.status == 400) {
          const details = Object.entries(resp.data)
            .map(([k, v]) => `${k}: ${v.join(" ")}`)
            .join("\n")
          // { name: ['Field missing.', 'Other error.'], field2: ['Field too long.'] }
          // => 'name: Field missing. Other error.\nfield2: Field too long.'
          await this.$refs.msgbox.alert(`Server error:\n${details}`)
        }
        if (resp.status > 400) {
          await this.$refs.msgbox.alert(`Server error (${e.response.status})`)
        }
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
        this.infobox = undefined
      }
      this.exam = ret.data
      this.exam.created = new Date(this.exam.created)

      window.scrollTo({ top: 0, behavior: "smooth" })
    },
  },
}
</script>
<style scoped>
a {
  text-decoration: none;
}
</style>
