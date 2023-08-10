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
          >
            {{ tag.text }}
            <!--
            &nbsp;<span class="text-caption">({{ tag.count }})</span>
            -->
          </v-chip>
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
          :items="source_langs_localized"
          @change="update_filtered_exercises"
        >
          <template v-slot:selection="{ item, index }">
            <span>{{ item.text }}</span>
            <span v-if="index < search.src_langs.length - 1">,&nbsp;</span>
          </template>
        </v-autocomplete>
      </v-col>
      <v-col cols="12" md="3">
        <v-autocomplete
          :label="$t('exercise.target_language')"
          @change="update_filtered_exercises"
          prepend-inner-icon="mdi-chat"
          dense
          outlined
          hide-details
          multiple
          v-model="search.lang_learn.langs"
          :items="learn_langs_localized"
          clearable
        >
          <template v-slot:prepend-item>
            <v-list-item @mousedown.prevent>
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
            <span v-if="index < search.lang_learn.langs.length - 1">
              ,&nbsp;
            </span>
            <span v-else class="grey--text">
              &nbsp;{{ current_cefr_label }}
            </span>
          </template>
        </v-autocomplete>
      </v-col>
      <v-col cols="12" md="2">
        <v-autocomplete
          :label="$t('exercise.author')"
          prepend-inner-icon="mdi-human-male-board"
          dense
          outlined
          hide-details
          auto-select-first
          clearable
          hide-no-data
          item-text="username"
          item-value="username"
          v-model="search.created_by"
          :items="authors_used"
          @change="update_filtered_exercises"
        ></v-autocomplete>
      </v-col>
      <v-spacer></v-spacer>
      <v-col>
        <v-select
          dense
          :label="$t('sort.sort')"
          prepend-inner-icon="mdi-sort"
          v-model="search.sort"
          :items="[
            { value: '-likes,-created', text: $t('sort.rated') },
            { value: '-created', text: $t('sort.recent') },
          ]"
          @change="update_filtered_exercises"
        ></v-select>
      </v-col>
    </v-row>

    <v-btn
      class="primary--text mt-3"
      large
      text
      :to="localePath('/editor')"
      nuxt
    >
      <v-icon class="mr-1">mdi-plus</v-icon>
      {{ $t("home.create_exercise") }}
    </v-btn>

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
        ></ExerciseListItem>
      </template>
    </v-data-iterator>
  </v-container>
</template>
<script>
import langs_available from "~/mixins/langs_available.js"
import cefr from "~/mixins/cefr.js"
export default {
  name: "Index",
  mixins: [langs_available, cefr],
  data: () => ({
    authors_used: [], // from api [ { name: "art", pk: 9, count: 5 }, … ]
    tags_used: [], // from api [ { name: "art", pk: 9, count: 5 }, … ]
    source_langs_used: [], // from api [ { code: "en", count: 11 }, … ]
    learn_langs_used: [], // from api [ { code: "en", count: 11 }, … ]
    iterator_key: "",
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
      text: "",
      tags: [],
      created_by: "",
      src_langs: [],
      lang_learn: {
        langs: [],
        levels: [1, 6],
      },
      sort: "-likes,-created",
    },
  }),
  computed: {
    source_langs_localized() {
      // [ { text: "English", value: "en" }, … ]
      // to be used in v-autocomplete items
      const codes = this.source_langs_used.map((e) => e.code)
      return this.langs_available.filter((e) => codes.includes(e.value))
    },
    learn_langs_localized() {
      // [ { text: "English", value: "en" }, … ]
      // to be used in v-autocomplete items
      const codes = this.learn_langs_used.map((e) => e.code)
      return this.langs_available.filter((e) => codes.includes(e.value))
    },
    tags_used_localized() {
      // [ { text: "Scienco", value: "science", count: 1 }, … ]
      // to be used in v-chip-group
      return this.tags_used.map((t) => ({
        value: t.name,
        text: this.$t(`tags.${t.name}`),
        count: t.count,
      }))
    },
    current_cefr_label() {
      const [min, max] = this.search.lang_learn.levels
      return this.cefr_info({
        lang_learn_cefr_level_min: min,
        lang_learn_cefr_level_max: max,
      })
    },
  },
  methods: {
    async update_filtered_exercises(preserve_offset) {
      // TODO: debounce?
      // Note: the parameter 'preserve_offset' may be an event
      // if the function is called from a component e.g. @click="update_filtered_exercises"
      if (preserve_offset !== "preserve_offset") {
        this.$set(this.search, "offset", 0)
      }
      const params = {
        name: this.search.text,
        src_lang: this.search.src_langs,
        lang_learn_lang: this.search.lang_learn.langs,
        offset: this.search.offset,
        created_by: this.search.created_by,
        tags: this.search.tags,
        ordering: this.search.sort,
      }
      if (params.lang_learn_lang?.length) {
        params.cefr_level_min = this.search.lang_learn.levels[0]
        params.cefr_level_max = this.search.lang_learn.levels[1]
      }
      await this.get_exercises_from_api(params)
    },
    async get_exercises_from_api(params_obj) {
      const query = new URLSearchParams()
      query.set("limit", this.page_length)
      for (const k in params_obj) query.set(k, params_obj[k])
      const url = `/v1/exercises/?${query.toString()}`

      // --
      query.delete("offset")
      this.iterator_key = query.toString()
      // ^ these two lines are a workaround.
      // The problem they solve is this:
      // the v-data-iterator does not roll back to page 1
      // when an update of the items occours, example
      // after changing a search parameter.
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
      const new_offset = (page - 1) * this.page_length
      if (new_offset == this.search.offset) return
      this.search.offset = new_offset
      this.update_filtered_exercises("preserve_offset")
    },
  },
  async fetch() {
    await this.update_filtered_exercises()
    this.authors_used = (
      await this.$auth.axios.get("/v1/authors/?limit=999")
    ).data?.results
    this.tags_used = (
      await this.$auth.axios.get("/v1/tags/used/?limit=999")
    ).data?.results
    this.source_langs_used = (
      await this.$auth.axios.get("/v1/languages/source/")
    ).data?.filter((l) => !!l.code)
    this.learn_langs_used = (
      await this.$auth.axios.get("/v1/languages/learn/")
    ).data?.filter((l) => !!l.code)
  },
  fetchOnServer: true,
  fetchKey: "exercises",
}
</script>
