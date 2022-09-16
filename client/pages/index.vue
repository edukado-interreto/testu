<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="7">
        <v-text-field
          label="Search exercise"
          append-icon="mdi-magnify"
          clearable
          v-model="search.text"
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
                :min="0"
                :max="5"
                :value="[0, 5]"
                :tick-labels="['A1', 'A2', 'B1', 'B2', 'C1', 'C2']"
                v-model="search.lang_learn.levels"
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

  </v-container>
</template>
<script>
const CEFR = {
  A1: 0,
  A2: 1,
  B1: 2,
  B2: 3,
  C1: 4,
  C2: 5,
}

import langs_available from '~/mixins/langs_available.js'
export default {
  mixins: [
    langs_available
  ],
  data: () => ({
    exercises: [
      {
        id: '1',
        author: 'lorem',
        title: 'Ekzerco pri akuzativo',
        lang: 'eo',
        tags: ['grammar'],
        age_min: 0,
        age_max: 99,
        lang_learn: {
          target_lang: 'eo',
          cefr_min: CEFR.A2,
          cefr_max: CEFR.A2,
        }
      },
      {
        id: '2',
        author: 'ipsum',
        title: 'Sorting algorithms',
        lang: 'en',
        tags: ['programming', 'math'],
        age_min: 5,
        age_max: 99,
      },
      {
        id: '3',
        author: 'dolor',
        title: 'La seconda guerra mondiale',
        lang: 'it',
        tags: ['history', 'literature'],
        age_min: 5,
        age_max: 99,
      }
    ],
    search: {
      text: '',
      tags: [],
      src_langs: ['en'], // TODO: current interface language
      lang_learn: {
        langs: [],
        levels: [0, 5],
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
  methods: {
    n2cefr(n) {
      return Object.entries(CEFR).find(e => e[1] == n)[0];
    }
  },
  computed: {
    current_cefr_label() {
      const [min, max] = this.search.lang_learn.levels.map(this.n2cefr);
      if (min == 'A1' && max == 'C2') return ''; // any level
      let ret = min;
      if (min != max) ret += ` - ${max}`;
      return ret;
    },
    tags_available() {
      return this.exercises.flatMap(e => e.tags)
    }
  },
  //mounted: async function() {
  //  this.user = await this.$auth.user(true)
  //},
}
</script>

