<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-chip-group
          multiple
          active-class="primary"
          show-arrows
          v-model="search.tags"
          @change="update_filtered_exercises"
        >
          <v-chip
            v-for="tag in tags_used_localized"
            :key="tag.value"
            :value="tag.value"
            v-text="tag.text"
          ></v-chip>
        </v-chip-group>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="12" md="7">
        <v-text-field
          :label="$t('home.search_exercise')"
          append-icon="mdi-magnify"
          v-model="search.text"
          @keyup.enter="update_filtered_exercises"
          hide-details
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="3">
        <v-autocomplete
          :label="$t('exercise.language')"
          dense
          outlined
          hide-details
          auto-select-first
          clearable
          multiple
          v-model="search.src_langs"
          :items="langs_available"
          @change="update_filtered_exercises"
        >
          <template v-slot:selection="{ item, index }">
            <span>{{ item.text }}</span>
            <span v-if="index < search.src_langs.length-1">,&nbsp;</span>
          </template>
        </v-autocomplete>
      </v-col>
      <v-col cols="12" md="3">
        <v-autocomplete
          label="Language learning"
          @change="update_filtered_exercises"
          prepend-inner-icon="mdi-chat"
          dense
          outlined
          hide-details
          multiple
          v-model="search.lang_learn.langs"
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
                v-model="search.lang_learn.levels"
                @change="update_filtered_exercises"
              ></v-range-slider>
            </v-list-item>
          </template>
          <template v-slot:selection="{ item, index }">
            <span>{{ item.text }}</span>
            <span v-if="index < search.lang_learn.langs.length-1">,&nbsp;</span>
            <span
              v-else
              class="grey--text"
            >
              &nbsp;{{ current_cefr_label }}
            </span>
          </template>
        </v-autocomplete>
      </v-col>
      <v-spacer></v-spacer>
      <!--
      <v-col>
        <v-select
          dense
          label="Sort"
          disabled
          prepend-inner-icon="mdi-sort"
          v-model="search.sort"
          :items="[ { value: 'recent', text: 'Most recent' }, { value: 'rate', text: 'Most rated' }]"
        >
        </v-select>
      </v-col>
      -->
    </v-row>

      <v-btn
        class="primary--text mt-3"
        large
        text
        :to="localePath('/editor')"
        nuxt
      ><v-icon class="mr-1">mdi-plus</v-icon> {{$t("home.create_exercise")}}</v-btn>

      <v-data-iterator
        class="mt-5"
        :key="iterator_key"
        :items="exercises.results"
        :items-per-page="page_length"
        :server-items-length="exercises.count"
        :footer-props="{ 'disable-items-per-page': true }"
        @update:page="on_page_update"
        :loading="loading"
      >
        <template v-slot:default="props">
          <ExerciseListItem
            v-for="item in props.items"
            :item="item"
            :key="item.id"
          >
          </ExerciseListItem>
        </template>
      </v-data-iterator>
  </v-container>
</template>
<script>
import langs_available from '~/mixins/langs_available.js'
import cefr from '~/mixins/cefr.js'
export default {
  name: 'Index',
  mixins: [
    langs_available,
    cefr
  ],
  data: () => ({
    tags_used: [],
    iterator_key: '',
    page_length: 15,
    loading: false,
    exercises: {
      count: 0,
      next: null,
      prev: null,
      results: [],
    },
    search: {
      offset: 0,
      text: '',
      tags: [],
      src_langs: ['en'], // TODO: current interface language
      lang_learn: {
        langs: [],
        levels: [1, 6],
      },
      sort: 'recent'
    },
    //langs_available: [
    //  'en',
    //  'eo',
    //  'fr',
    //  'it'
    //]
  }),
  computed: {
    tags_used_localized() {
      return this.tags_used.map(t => ({
        value: t,
        text: this.$t(`tags.${t}`),
      }))
    },
    current_cefr_label() {
      const [min, max] = this.search.lang_learn.levels;
      return this.cefr_info({
        lang_learn_cefr_level_min: min,
        lang_learn_cefr_level_max: max,
      });
    },
  },
  methods: {
    date_formatted(d) {
      return (
        new Date(d)
      ).toLocaleString("en-US") // TODO: i18n 
    },
    async update_filtered_exercises(preserve_offset) {
      // FIXME: the parameter 'preserve_offset' may be an event
      // if the function is called from a component e.g. @click="update_filtered_exercises"
      if (preserve_offset !== 'preserve_offset') { 
        this.$set(this.search, 'offset', 0)
        console.log("reset to page 0")
        // FIXME: the v-data-iterator does not reset to page 0!
      }
      const params = {
        name: this.search.text,
        src_lang: this.search.src_langs,
        lang_learn_lang: this.search.lang_learn.langs,
        offset: this.search.offset,
        tags: this.search.tags,
      }
      if (params.lang_learn_lang?.length) {
        params.cefr_level_min = this.search.lang_learn.levels[0]
        params.cefr_level_max = this.search.lang_learn.levels[1]
      }
      await this.get_exercises_from_api(params)
      return

      // TODO: fetch from api + debounce
      console.log("update_filtered_exercises")
      console.log(this.search.lang_learn.langs)
      console.log(this.search.lang_learn.levels)
      this.filtered_exercises = this.exercises.filter(
        e => e.searchable !== false
      ).filter(
        e => e.name.toLowerCase().includes(
          this.search.text.toLowerCase() || ""
        )
      ).filter(
        e => (
          this.search.src_langs.length == 0
          || this.search.src_langs.includes(e.src_lang)
        )
      ).filter(e => {
        const langs = this.search.lang_learn.langs
        if (langs.length == 0) return true
        if (!langs.includes(e.lang_learn_lang)) return false
        const [min, max] = this.search.lang_learn.levels
        if (min > e.lang_learn_cefr_level_max) return false
        if (max < e.lang_learn_cefr_level_min) return false
        return true
      }).sort(
        // newest to oldest
        (a, b) => new Date(b.created) - new Date(a.created)
      )
    },
    async get_exercises_from_api(params_obj) {
      const query = new URLSearchParams()
      query.set('limit', this.page_length)
      for (const k in params_obj) query.set(k, params_obj[k])
      const url = `/v1/exercises/?${query.toString()}`
      console.log(`fetching ${url}`)

      // --
      query.delete('offset')
      this.iterator_key = query.toString()
      // ^ these two lines are a workaround.
      // The problem they solve is this:
      // the v-data-iterator does not roll back to page 1
      // when it is at page 2-N and an update of the items
      // occours, example changing a search parameter.
      // The workaround is to force the refresh of the
      // component changing its key when any search
      // parameter change. As a key we use the
      // query string of the api URL, stripping the
      // page number, i.e. `offset`.
      // --

      this.loading = true
      const resp = await this.$auth.axios.get(url)
      this.loading = false
      this.exercises = resp.data
      // {
      //   "count": 7,
      //   "next": "http://…/api/v1/exercises/?limit=2&offset=2",
      //   "previous": null,
      //   "results": [ … ]
      // }
    },
    on_page_update(page) {
      const new_offset = (page-1) * this.page_length
      if (new_offset == this.search.offset) return
      this.search.offset = new_offset
      this.update_filtered_exercises('preserve_offset')
    },
  },
  async fetch() {
    await this.update_filtered_exercises()
    this.tags_used = (
      await this.$auth.axios.get(
        "/v1/tags/used/?limit=999"
      )
    ).data.results.map(e => e.name)
  },
  fetchOnServer: true,
  fetchKey: 'exercises'
}
</script>
