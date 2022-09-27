<template>
  <div>
    <SheetEditor
      :sheet="sheet"
      ref="sheet_editor"
    ></SheetEditor>

    <v-expansion-panels class="mt-9" v-model="infobox">
      <v-expansion-panel>
        <v-expansion-panel-header>
          <template v-slot:default="{ open }">
            Exercise details
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
          ></v-text-field>
          <v-text-field
            label="Description"
            v-model="details.description"
          ></v-text-field>
          <v-autocomplete
            v-if="false"
            label="Tags"
            small-chips
            deletable-chips
            multiple
            v-model="details.tags"
            :items="tags_available"
          ></v-autocomplete>
          <v-autocomplete
            label="Language"
            v-model="details.src_lang"
            :items="langs_available"
          ></v-autocomplete>
          <v-autocomplete
            label="Language learning"
            v-model="details.lang_learn.lang"
            :items="langs_available"
            clearable
          >
            <template v-slot:prepend-item>
              <v-list-item
                @mousedown.prevent
              >
                <v-range-slider
                  dense
                  :min="cefr_lbound"
                  :max="cefr_ubound"
                  :value="[cefr_lbound, cefr_ubound]"
                  :tick-labels="cefr_levels"
                  v-model="details.lang_learn.cefr_level_range"
                ></v-range-slider>
              </v-list-item>
            </template>
            <template v-slot:selection="{ item, index }">
              <span>{{ item.text }}</span>
              <span
                class="grey--text"
              >
                &nbsp;{{ current_cefr_label }}
              </span>
            </template>
          </v-autocomplete>
          <v-range-slider
            :label="`Age range (${age_range_label[0]} – ${age_range_label[1]})`"
            v-model="details.age_range"
            min="0"
            max="18"
          >
          </v-range-slider>
          <v-checkbox
            label="Unlisted in search results"
            v-model="details.unlisted"
          ></v-checkbox>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    
    <v-btn
      class="mt-7 primary--text"
      large
      text
      @click="save"
    >
      <v-icon class="mr-2">mdi-content-save</v-icon>
      Save
    </v-btn>

    <!-- {{ details }} -->
  </div>
</template>
<script>
import tags_available from '~/data/tags_available.json'
import langs_available from '~/mixins/langs_available.js'
import cefr from '~/mixins/cefr.js'
export default {
  mixins: [
    langs_available,
    cefr
  ],
  name: 'Editor',
  head() {
    return {
      title: (this.overwrite_id === undefined) ? 'New exercise' : 'Edit exercise'
    }
  },
  async fetch() {
    if (this.$route.query.new_from) {
      await this.load_exercise(this.$route.query.new_from)
      this.$set(this.details, 'title', 'Copy of ' + this.details.title) // TODO i18n
    }
    if (this.$route.query.edit) {
      await this.load_exercise(this.$route.query.edit)
      this.overwrite_id = this.$route.query.edit
    }
  },
  async asyncData({params, route}) {
    return { tags_available }
  },
  data: () => ({
    overwrite_id: undefined,
    user: {},
    sheet: [],
    details: {
      title: '',
      src_lang: 'en',
      description: '',
      tags: [],
      age_range: [0, 18],
      lang_learn: {
        lang: undefined,
        cefr_level_range: [
          1, // this.cefr_lbound,
          6, // this.cefr_ubound,
        ],
      }
    },
    infobox: undefined
  }),
  computed: {
    current_cefr_label() {
      console.log('in cefr label')
      const [min, max] = this.details.lang_learn.cefr_level_range.map(this.n2cefr);
      console.log('cefr label min max:', min, max)
      if (min == 'A1' && max == 'C2') return ''; // any level
      let ret = min;
      if (min != max) ret += ` - ${max}`;
      return ret;
    },
    age_range_label() {
      return this.details.age_range.map(
        n => n + ((n == 18) ? '+' : '')
      )
    }
  },
  methods: {
    async load_exercise(id) {
      const exercise = await (
        await fetch(`/api/v1/sheets/${id}/`)
      ).json()
      this.sheet = exercise.data.sheet
      this.details.title = exercise.name
      this.details.description = exercise.description
      this.details.tags = [...exercise.tags]
      this.details.src_lang = exercise.src_lang
      if (exercise.lang_learn) {
        this.details.lang_learn.lang = exercise.lang_learn_lang,
        this.details.lang_learn.cefr_level_range = [
          exercise.lang_learn_cefr_level_min,
          exercise.lang_learn_cefr_level_max,
        ]
      }
      this.details.age_range = [
        exercise.age_min,
        exercise.age_max
      ]
      this.details.unlisted = !exercise.searchable
      // TODO set tags, age range and the other fields
    },
    async save() {
      if (this.sheet.length == 0) {
        alert("Please add at least one unit");
        return;
      }
      if (!this.details.title) {
        alert("Please provide a title for the exercise");
        return;
      }
      const payload = {};
      payload.name = this.details.title;
      payload.description = this.details.description;
      // payload.tags = [...this.details.tags]; // TODO: uncomment this
      payload.src_lang = this.details.src_lang;
      payload.lang_learn = false;
      if (this.details.lang_learn.lang) {
        payload.lang_learn = true;
        payload.lang_learn_lang = this.details.lang_learn.lang;
        payload.lang_learn_cefr_level_min = this.details.lang_learn.cefr_level_range[0];
        payload.lang_learn_cefr_level_max = this.details.lang_learn.cefr_level_range[1];
      }
      payload.age_min = this.details.age_range[0];
      payload.age_max = this.details.age_range[1];
      payload.searchable = !this.details.unlisted;
      payload.data = {
        sheet: this.sheet.map(
          (e, i) => ({
            ...e,
            _parsed: this.$refs.sheet_editor.$refs.unit[i].parsed
            // inject the parsed exercises into the sheet object that will
            // be stored in the database. The code is parsed by the grand-children
            // components so we use $refs to access it here.
          })
        )
      };
      payload.created_by = this.$store.getters['authenticator/authUser'].username;

      console.log("data:", payload);

      // setup the api call: a PUT request if editing
      // an existing exercise, i.e. when this.overwrite_id
      // contains an exercise id, or a POST request if
      // creating a new one otherwise
      const api = {
        path: '/api/v1/sheets/',
        method: 'POST'
      }
      if (this.overwrite_id !== undefined) {
        api.path = `/api/v1/sheets/${this.overwrite_id}/`
        api.method = 'PUT'
      }

      const ret = await fetch(api.path, {
        method: api.method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      })
      
      console.log(ret);

      let ret_json;
      try {
        ret_json = await ret.json();
      } catch {
      }

      if (ret.status >= 400) {
        console.error({ ret, ret_json })
        alert(`Error ${ret.status}. ${ret_json}`)
        return
      }

      console.log(ret_json)
      this.$router.push(`/exercise/${ret_json.id}`)
    }
  },
  mounted: async function() {
    this.user = await this.$auth.user(true)
  },
  middleware: 'redirects',
  meta: {
    requiresAuth: true
  }
}
</script>
<style scoped>
  .pre-line { white-space: pre-line; }
  .code { font-family: monospace; }
</style>
