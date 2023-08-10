<template>
  <div>
    <MsgBox ref="msgbox"></MsgBox>
    <SheetEditor :sheet="sheet" ref="sheet_editor" />

    <v-expansion-panels class="mt-9" v-model="infobox">
      <v-expansion-panel>
        <v-expansion-panel-header>
          <template v-slot:default="{ open }">
            {{ $t("editor.details") }}
            <span class="ml-5 text--disabled" v-if="!open">
              <span v-if="details.title">{{ details.title }}</span>
              <span v-else class="font-italic">Untitled exercise</span>
            </span>
          </template>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-text-field
            label="Title"
            v-model="details.title"
            maxlength="100"
          ></v-text-field>
          <v-text-field
            :label="$t('editor.description')"
            v-model="details.description"
          ></v-text-field>
          <v-autocomplete
            :label="$t('editor.tags')"
            small-chips
            deletable-chips
            multiple
            v-model="details.tags"
            :items="tags_available_localized"
          ></v-autocomplete>
          <v-autocomplete
            :label="$t('exercise.language')"
            v-model="details.src_lang"
            :items="langs_available"
          ></v-autocomplete>
          <v-autocomplete
            :label="$t('exercise.target_language')"
            v-model="details.lang_learn.lang"
            :items="langs_available"
            clearable
          >
            <template v-slot:selection="{ item, index }">
              <span>{{ item.text }}</span>
              <span class="grey--text">&nbsp;{{ current_cefr_label }}</span>
            </template>
          </v-autocomplete>
          <v-range-slider
            v-model="details.lang_learn.cefr_level_range"
            :label="$t('editor.cefr_levels_label')"
            :min="cefr_lbound"
            :max="cefr_ubound"
            :value="[cefr_lbound, cefr_ubound]"
            :tick-labels="cefr_levels"
            class="my-3"
            dense
          />
          <v-range-slider
            v-model="details.age_range"
            :label="`${$t('editor.age_range')} (${age_range_label[0]} – ${
              age_range_label[1]
            })`"
            min="0"
            max="18"
            class="my-3"
          />
          <v-checkbox
            :label="$t('editor.unlisted')"
            v-model="details.unlisted"
          ></v-checkbox>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-btn class="mt-7 primary--text" large text @click="save">
      <v-icon class="mr-2">mdi-content-save</v-icon>
      {{ $t("editor.save") }}
    </v-btn>

    <!-- {{ details }} -->
  </div>
</template>
<script>
import langs_available from "~/mixins/langs_available.js"
import cefr from "~/mixins/cefr.js"
export default {
  mixins: [langs_available, cefr],
  name: "Editor",
  head() {
    return {
      title: this.overwrite_id === undefined ? "New exercise" : "Edit exercise",
    }
  },
  async fetch() {
    this.tags_available = (
      await this.$auth.axios.get("/v1/tags/?limit=999")
    ).data.results.map((e) => e.name)

    if (this.$route.query.new_from) {
      await this.load_exercise(this.$route.query.new_from)
      this.$set(this.details, "title", "Copy of " + this.details.title) // TODO i18n
    }
    if (this.$route.query.edit) {
      await this.load_exercise(this.$route.query.edit)
      this.overwrite_id = this.$route.query.edit
    }
  },
  watch: {
    sheet: {
      deep: true,
      handler: function (sheet) {
        if (!this.loaded_sheet) return
        this.dirty = this.loaded_sheet !== JSON.stringify(sheet)
      },
    },
    details: {
      deep: true,
      handler: function (details) {
        if (!this.loaded_details) return
        this.dirty = this.loaded_details !== JSON.stringify(details)
      },
    },
  },
  data: () => ({
    beforeunload_event: undefined,
    tags_available: [],
    overwrite_id: undefined,
    user: {},
    dirty: false,
    sheet: [],
    details: {
      title: "",
      src_lang: "en",
      description: "",
      tags: [],
      age_range: [0, 18],
      lang_learn: {
        lang: undefined,
        cefr_level_range: [
          1, // this.cefr_lbound,
          6, // this.cefr_ubound,
        ],
      },
    },
    infobox: undefined,
  }),
  computed: {
    tags_available_localized() {
      return this.tags_available.map((t) => ({
        value: t,
        text: this.$t(`tags.${t}`),
      }))
    },
    current_cefr_label() {
      const [min, max] = this.details.lang_learn.cefr_level_range.map(
        this.n2cefr,
      )
      if (min == "A1" && max == "C2") return "" // any level
      let ret = min
      if (min != max) ret += ` - ${max}`
      return ret
    },
    age_range_label() {
      return this.details.age_range.map((n) => n + (n == 18 ? "+" : ""))
    },
  },
  methods: {
    async load_exercise(id) {
      const exercise = (await this.$auth.axios.get(`/v1/exercises/${id}/`)).data
      this.sheet = exercise.data.sheet || []
      this.details.title = exercise.name
      this.details.description = exercise.description
      this.details.tags = [...exercise.tags]
      this.details.src_lang = exercise.src_lang
      if (exercise.lang_learn) {
        ;(this.details.lang_learn.lang = exercise.lang_learn_lang),
          (this.details.lang_learn.cefr_level_range = [
            exercise.lang_learn_cefr_level_min,
            exercise.lang_learn_cefr_level_max,
          ])
      }
      this.details.age_range = [exercise.age_min, exercise.age_max]
      this.details.unlisted = !exercise.searchable
      this.loaded_sheet = JSON.stringify(this.sheet)
      this.loaded_details = JSON.stringify(this.details)
      // TODO set tags, age range and the other fields
    },
    async save() {
      if (this.sheet.length == 0) {
        await this.$refs.msgbox.alert("Please add at least one unit")
        return
      }
      if (!this.details.title) {
        await this.$refs.msgbox.alert("Please provide a title for the exercise")
        return
      }
      const payload = {}
      payload.name = this.details.title
      payload.description = this.details.description
      payload.tags = [...this.details.tags] // TODO: uncomment this
      payload.src_lang = this.details.src_lang
      payload.lang_learn = false
      if (this.details.lang_learn.lang) {
        payload.lang_learn = true
        payload.lang_learn_lang = this.details.lang_learn.lang
        payload.lang_learn_cefr_level_min =
          this.details.lang_learn.cefr_level_range[0]
        payload.lang_learn_cefr_level_max =
          this.details.lang_learn.cefr_level_range[1]
      }
      payload.age_min = this.details.age_range[0]
      payload.age_max = this.details.age_range[1]
      payload.searchable = !this.details.unlisted
      payload.data = {
        sheet: this.sheet.map((e, i) => ({
          ...e,
          _parsed: this.$refs.sheet_editor.$refs.unit[i].parsed,
          // inject the parsed exercises into the sheet object that will
          // be stored in the database. The code is parsed by the grand-children
          // components so we use $refs to access it here.
        })),
      }
      payload.created_by =
        this.$store.getters["authenticator/authUser"].username

      await this.$auth.checkTokens()

      // setup the api call: a PUT request if editing
      // an existing exercise, i.e. when this.overwrite_id
      // contains an exercise id, or a POST request if
      // creating a new one otherwise
      const api = {
        path: "/v1/exercises/",
        method: "POST",
      }
      if (this.overwrite_id !== undefined) {
        api.path = `/v1/exercises/${this.overwrite_id}/`
        api.method = "PUT"
      }

      try {
        const ret = await this.$auth.axios({
          url: api.path,
          method: api.method,
          data: payload,
        })
        this.dirty = false
        this.loaded_sheet = JSON.stringify(ret.data.sheet)
        this.$router.push(this.localePath(`/exercise/${ret.data.lid}`))
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
          await this.$refs.msgbox.alert(`Server error (${resp.status})`)
        }
      }
    },
    confirm_leave() {
      return confirm(this.$t("editor.confirm_leave"))
    },
    confirm_stay_dirty() {
      return this.dirty && !this.confirm_leave()
    },
    before_window_unload(e) {
      if (this.confirm_stay_dirty()) {
        e.preventDefault()
        e.returnString = ""
      }
    },
  },
  beforeRouteLeave(to, from, next) {
    this.confirm_stay_dirty() ? next(false) : next()
  },
  mounted: async function () {
    this.user = await this.$auth.user(true)
    window.addEventListener("beforeunload", this.before_window_unload, {
      capture: true,
    })
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.before_window_unload)
  },
  middleware: "redirects",
  meta: {
    requiresAuth: true,
  },
}
</script>
<style scoped>
.pre-line {
  white-space: pre-line;
}
.code {
  font-family: monospace;
}
</style>
