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

      <v-data-iterator
        class="mt-5"
        :items="exercises"
        :items-per-page="20"
      >
        <template v-slot:default="props">
          <v-row>
            <v-col
              v-for="item in props.items"
              :key="item.name"
              cols="12"
              sm="6"
              md="4"
              lg="3"
            >
              <v-card>
                <v-card-title class="subheading font-weight-bold">
                  {{ item.name }}
                </v-card-title>
                <v-card-text v-if="item.description">
                  {{ item.description }}
                </v-card-text>
                <v-divider></v-divider>

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
  mixins: [
    langs_available,
    cefr
  ],
  data: () => ({
    exercises: [],
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
  computed: {
    current_cefr_label() {
      const [min, max] = this.search.lang_learn.levels.map(this.n2cefr);
      if (min == 'A1' && max == 'C2') return ''; // any level
      let ret = min;
      if (min != max) ret += ` - ${max}`;
      return ret;
    },
    tags_available() {
      return this.exercises.flatMap(e => e.tags).filter(t => !!t)
    }
  },
  methods: {
    async fetchExercises(search) {

      let resp;

      try {

        // TODO: fetch on server
        const resp = await (
          await fetch('/api/v1/sheets/') // TODO: search parameters
        ).json();

      } catch(e) {
        alert("Cannot fetch exercises from the server");
        console.log(e);
        return;
      }

      this.exercises = resp;

    },
  },
  async fetch() {
    this.exercises = await (
      await fetch('/api/v1/sheets/')
    ).json();
  },
  fetchOnServer: true,
  fetchKey: 'exercises'
}
</script>
