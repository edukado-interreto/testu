<template>
  <v-container>
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
      >{{ section.description }}</div>
      <component
        :is="unit_component(section.type)"
        :code="section.code"
        :shuffle="section.shuffle"
        :silent="all_silent"
        :readonly="all_readonly"
        ref="unit"
      />
    </v-sheet>

    <v-btn @click="get_solved_sheet">test</v-btn>
    <component
      :is="unit_component('multiple_choice')"
      :solved="solved_test"
      :readonly="true"
    />
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
    solved_test: [],
    all_readonly: false,
    all_silent: true,
  }),
  async asyncData({ route, params }) {

    const id = (process.server) ? route.params.id : params.id;
    let exercise;

    if (id) {
      exercise = await (
        await fetch(`/api/v1/sheets/${id}/`)
      ).json()
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
        return this.exercise.created_by === authUser.id
      }
    },
    user_is_creator() {
      const authUser = this.$store.getters['authenticator/authUser']
      if (!authUser) return false
      return this.exercise.created_by === authUser.username
    }
  },
  methods: {
    async remove() {

      if (!confirm(
        'Are you sure you want to delete this exercise?'
      )) return;

      const resp = await fetch(`/api/v1/sheets/${this.id}`, {
        method: 'DELETE'
      })
      if (resp.status >= 400) {
        console.error(resp)
        alert(`Error ${resp.status}`)
        return
      }
    },
    get_solved_sheet() {
      this.solved_test = this.$refs.unit[0].get_solved()
      this.all_silent = false
      this.all_readonly = true
    },
  }
}
</script>
<style scoped>
  .pre-line { white-space: pre-line; }
</style>
