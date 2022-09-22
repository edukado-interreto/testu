<template>
  <div>
    <SheetEditor :sheet="sheet"></SheetEditor>

    <v-expansion-panels class="mt-9" v-model="infobox">
      <v-expansion-panel>
        <v-expansion-panel-header>Details</v-expansion-panel-header>
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
                  :min="0"
                  :max="5"
                  :value="[0, 5]"
                  :tick-labels="['A1', 'A2', 'B1', 'B2', 'C1', 'C2']"
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
      title: 'New exercise'
    }
  },
  asyncData({params}) {
    return { tags_available }
  },
  data: () => ({
    user: {},
    sheet: [],
    details: {
      src_lang: 'en',
      description: '',
      tags: [],
      age_range: [0, 18],
      lang_learn: {
        cefr_level_range: [0, 5],
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
      payload.src_lang = this.details.src_lang;
      payload.tags = [...this.details.tags];
      if (this.details.lang_learn.lang) {
        payload.lang_learn = true;
        payload.lang_learn_lang = this.details.lang_learn.lang;
        payload.lang_learn_cefr_level_min = this.details.lang_learn.cefr_level_range[0];
        payload.lang_learn_cefr_level_max = this.details.lang_learn.cefr_level_range[1];
      }
      payload.age_min = this.details.age_range[0];
      payload.age_max = this.details.age_range[1];
      payload.unlisted = !!this.details.unlisted;
      payload.data = { sheet: this.sheet };
      payload.created_by = this.$store.getters['authenticator/authUser'].id;

      console.log("data:", payload);

      // create a FormData object from payload
      // the 'data' prop is encoded as json string,
      // the other ones are going to be regular form fields
      const form_data = new FormData();
      Object.keys(payload).filter(
        k => {
          if (k == 'data') return false;
          return true;
        }
      ).forEach(
        k => form_data.append(k, payload[k])
      );
      form_data.append('data', JSON.stringify(payload.data));
      // --

      console.log({form_data});

      const ret = await fetch('/api/v1/sheets/', {
        method: 'POST',
        //headers: {
        //  'Content-Type': 'application/json'
        //},
        body: form_data
        //body: JSON.stringify({
        //  data: payload
        //})
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
