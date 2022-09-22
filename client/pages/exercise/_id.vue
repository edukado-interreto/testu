<template>
  <v-container>
    <h1>{{ exercise.name }}</h1>
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
      }
    },
    head() {
      return {
        title: this.exercise.name
      }
    }
  }
</script>
