<template>
  <v-container>
    <MsgBox ref="msgbox"></MsgBox>
    <v-row>
      <v-col>
        <h1>{{ exercise.name }}</h1>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="auto">
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              v-bind="attrs"
              v-on="on"
              :disabled="!user_logged_in"
            >
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item
              nuxt
              :to="`/editor?new_from=${exercise.id}`"
            >
              <v-list-item-icon>
                <v-icon>mdi-content-copy</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                Create a copy
              </v-list-item-title>
            </v-list-item>
            <v-list-item
              v-if="user_is_creator"
              nuxt
              :to="`/editor?edit=${exercise.id}`"
            >
              <v-list-item-icon>
                <v-icon>mdi-pencil</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                Edit exercise
              </v-list-item-title>
            </v-list-item>
            <v-list-item
              v-if="user_is_creator"
              class="error--text font-weight-bold"
              @click="remove"
            >
              <v-list-item-icon>
                <v-icon color="error">mdi-delete</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                Delete exercise
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-col>
    </v-row>
    <v-row dense class="text-caption mb-6">
      <v-col cols="auto">
        <v-icon small>mdi-account</v-icon> {{ exercise.created_by || 'anonymous' }}
      </v-col>
      <v-col cols="auto">
        <v-icon small>mdi-clock</v-icon> {{ date_formatted }}
      </v-col>
      <v-spacer></v-spacer>
      <v-col
        cols="auto"
        v-if="exercise.age_min > 0 || exercise.age_max < 18"
      >
        <v-icon small>mdi-human-child</v-icon> Age: {{ exercise.age_min }} - {{ (exercise.age_max == 18) ? '18+' : exercise.age_max  }}
      </v-col>
      <v-col
        cols="auto"
        v-if="exercise.lang_learn === true"
      >
        <v-icon small>mdi-chat</v-icon>
        {{ langs_table[exercise.lang_learn_lang].name }} {{ cefr_info(exercise) }}
      </v-col>
    </v-row>

    <v-sheet v-if="exercise.description" class="mb-7">
      {{ exercise.description }}
    </v-sheet>

    <v-sheet
      v-for="(section, i) in exercise.data.sheet"
      :key="section._key"
    >
      <div class="headline my-4"> 
        {{ i+1 }}. {{ section.title }}
        <span v-if="section.title === ''" class="font-italic">
          Untitled unit
        </span>
      </div>
      <div
        v-if="section.description"
        class="body-2 mb-4 pre-line"
      >
        <RichContent
          :text="section.description"
        >
        </RichContent>
      </div>
      <component
        :is="unit_component(section.type)"
        :code="section.code"
        :shuffle="section.shuffle"
        :ignore_case="section.ignore_case"
        :silent="all_silent"
        :readonly="all_readonly"
        ref="unit"
      />
    </v-sheet>

    <v-btn
      @click="submit"
      class="mt-9 primary"
      :disabled="submitted"
    >Check results</v-btn>
    

    <div
      v-for="(c, i) in submission"
    >
      <!-- this is not working, hence the long list:
      <component
        :key="i"
        :is="unit_component('c.type')"
        :solved="c.solved"
        :readonly="true"
      />
      -->
      <UnitMultipleChoice
        v-if="c.type == 'multiple_choice'"
        :key="i"
        :solved="c.solved"
        :readonly="true"
      ></UnitMultipleChoice>
      <UnitPairing
        v-if="c.type == 'pairing'"
        :key="i"
        :solved="c.solved"
        :readonly="true"
      ></UnitPairing>
      <UnitDefault
        v-if="c.type == 'default'"
        :key="i"
        :solved="c.solved"
        :readonly="true"
      ></UnitDefault>
      <UnitOpenAnswer
        v-if="c.type == 'open_answer'"
        :key="i"
        :solved="c.solved"
        :readonly="true"
      ></UnitOpenAnswer>
    </div>

    </v-sheet>
  </v-container>
</template>
<script>
import cefr from '~/mixins/cefr.js'
import langs_available from '~/mixins/langs_available.js'
import unit_component from '~/mixins/unit_component.js'
export default {
  name: 'Exercise',
  mixins: [
    langs_available,
    cefr,
    unit_component,
  ],
  data: () => ({
    solved_test: {},
    submission: [],
    all_readonly: false,
    all_silent: true,
    submitted: false,
  }),
  async asyncData({ route, params, $auth }) {
    const id = (process.server) ? route.params.id : params.id;
    let exercise;
    if (id) {
      exercise = (
        await $auth.axios.get(`/v1/sheets/${id}/`)
      ).data
    }
    return {
      id,
      exercise
    }
  },
  computed: {
    date_formatted() {
      return (
        new Date(this.exercise.modified)
      ).toLocaleString("en-US") // TODO: i18n 
    },
    user_logged_in() {
      const authUser = this.$store.getters['authenticator/authUser']
      if (!authUser) return false
      return true
    },
    user_is_creator() {
      const authUser = this.$store.getters['authenticator/authUser']
      if (!authUser) return false
      return this.exercise.created_by === authUser.username
    }
  },
  methods: {
    async remove() {

      if (!await this.$refs.msgbox.confirm(
        'Are you sure you want to delete this exercise?'
      )) return;

      try {
        await this.$auth.axios.delete(`/v1/sheets/${this.id}`)
        this.$router.push('/')
      } catch(e) {
        console.error({...e})
        await this.$refs.msgbox.alert(`Error ${e.response.status}`)
      }
    },
    submit() {
      // show the results of the quiz

      //this.solved_test = this.$refs.unit[0].get_solved()
      //console.log(this.exercise.data.sheet[0].type)

      this.submission = this.exercise.data.sheet.map((e, i) => ({
        type: e.type,
        solved: JSON.parse(JSON.stringify(this.$refs.unit[i].get_solved()))
      }))

      this.submitted = true
      window.scrollTo({ top:0, behavior: 'smooth'})

      this.all_silent = false
      this.all_readonly = true
    },
  },
  head() {
    return {
      title: this.exercise.name
    }
  },
}
</script>
<style scoped>
  .pre-line { white-space: pre-line; }
</style>
