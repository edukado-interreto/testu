<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="7">
        <v-text-field
          label="Search exercise"
          append-icon="mdi-magnify"
          v-model="search.text"
          @keyup.enter="update_filtered_exercises"
          hide-details
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="5">
        <v-chip-group
          multiple
          active-class="primary"
          show-arrows
          v-model="search.tags"
        >
          <v-chip
            v-for="tag in tags_available"
            :key="tag"
            :value="tag"
            v-text="tag"
          ></v-chip>
        </v-chip-group>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="3">
        <v-autocomplete
          label="Language"
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
    </v-row>

      <v-btn
        class="primary--text mt-3"
        large
        text
        to="/editor"
      ><v-icon class="mr-1">mdi-plus</v-icon>Create a new exercise</v-btn>

      <v-data-iterator
        class="mt-5"
        :items="filtered_exercises"
        :items-per-page="15"
      >
        <template v-slot:default="props">
          <v-row>
            <v-col
              v-for="item in props.items"
              :key="item.id"
              cols="12"
            >
              <v-card
                :to="`/exercise/${item.id}`"
                nuxt
              >
                <v-card-title
                  class="subheading font-weight-bold"
                >
                  {{ item.name }}
                </v-card-title>
                <v-card-subtitle v-if="item.description">
                  {{ item.description }}
                </v-card-subtitle>
                <v-card-text class="text-caption">
                  <div v-if="item.age_min > 0 || item.age_max < 18">
                    Age: {{ item.age_min }} - {{ (item.age_max == 18) ? '18+' : item.age_max  }}
                  </div>
                  <div v-if="item.lang_learn === true">
                    Language learning: {{ langs_table[item.lang_learn_lang].name }} {{ cefr_info(item) }}
                  </div>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-text>
                  <v-icon small>mdi-account</v-icon> {{ item.created_by || 'anonymous' }}
                  <span>·</span>
                  <v-icon small>mdi-clock</v-icon> {{ date_formatted(item.created) }}
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </template>
      </v-data-iterator>



  </v-container>
</template>
<script>
import langs_available from '~/mixins/langs_available.js'
import cefr from '~/mixins/cefr.js'
export default {
  name: 'Index',
  head() {
    return {
      title: 'Home page'
    }
  },
  mixins: [
    langs_available,
    cefr
  ],
  data: () => ({
    exercises: [],
    filtered_exercises: [],
    search: {
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
    current_cefr_label() {
      const [min, max] = this.search.lang_learn.levels;
      return this.cefr_info({
        lang_learn_cefr_level_min: min,
        lang_learn_cefr_level_max: max,
      });
    },
    tags_available() {
      return this.exercises.flatMap(e => e.tags).filter(t => !!t)
    }
  },
  methods: {
    date_formatted(d) {
      return (
        new Date(d)
      ).toLocaleString("en-US") // TODO: i18n 
    },
    update_filtered_exercises() {
      // TODO: fetch from api + debounce
      console.log("update_filtered_exercises")
      console.log(this.search.lang_learn.langs)
      console.log(this.search.lang_learn.levels)
      this.filtered_exercises = this.exercises.filter(
        e => e.name.includes(this.search.text || "")
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
  },
  async fetch() {
    this.exercises = await (
      await fetch('/api/v1/sheets/')
    ).json();
    this.update_filtered_exercises()
  },
  fetchOnServer: true,
  fetchKey: 'exercises'
}
</script>
