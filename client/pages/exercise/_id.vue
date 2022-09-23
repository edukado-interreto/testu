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
            >
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item
              nuxt
              :to="`/editor?new_from=${exercise.id}`"
            >
              <v-list-item-title>
                Create a copy
              </v-list-item-title>
            </v-list-item>
            <v-list-item
              v-if="user_is_creator"
              nuxt
              :to="`/editor?edit=${exercise.id}`"
            >
              <v-list-item-title>
                Edit exercise
              </v-list-item-title>
            </v-list-item>
            <v-list-item
              v-if="user_is_creator"
              class="red--text font-weight-bold"
              @click="remove"
            >
              <v-list-item-title>
                Delete exercise
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-col>
    </v-row>

    <v-row class="text-caption mb-2">
      <v-col cols="auto">
        <v-icon small>mdi-account</v-icon> {{ exercise.created_by || 'anonymous' }}
      </v-col>
      <v-col cols="auto">
        <v-icon small>mdi-clock</v-icon> {{ date_formatted }}
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
      <GapsEditor
        v-if="section.type == 'gapFilling'"
        :code="section.code"
        :shuffle="section.shuffle"
      />
    </v-sheet>
  </v-container>
</template>
<script>
  export default {
    name: 'Exercise',
    data: () => ({
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
      user_is_creator() {
        const authUser = this.$store.getters['authenticator/authUser']
        if (!authUser) return false
        return this.exercise.created_by === authUser.id
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
        this.$router.push('/')
      }
    },
    head() {
      return {
        title: this.exercise.name
      }
    }
  }
</script>
