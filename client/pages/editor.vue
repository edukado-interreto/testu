<template>
  <div>
    <SheetEditor :sheet="sheet"></SheetEditor>

    <v-expansion-panels class="mt-9" v-model="infobox">
      <v-expansion-panel>
        <v-expansion-panel-header>Details</v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-text-field dense label="Title"></v-text-field>
          <v-text-field dense label="Description"></v-text-field>
          <v-autocomplete
            label="Tags"
            dense
            small-chips
            deletable-chips
            multiple
            v-model="details.tags"
            :items="tags_available"
          ></v-autocomplete>
          <v-select dense label="Language"></v-select>
          <v-select dense label="Language learning"></v-select>
          <v-select dense label="Age range"></v-select>
          <v-checkbox label="Unlisted in search results"></v-checkbox>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    
    <v-btn
      class="mt-7 primary--text"
      large
      text
    >
      <v-icon class="mr-2">mdi-content-save</v-icon>
      Save
    </v-btn>
  </div>
</template>
<script>
import tags_available from '~/data/tags_available.json'
export default {
  name: 'Editor',
  head() {
    return {
      title: 'New exercise'
    }
  },
  data: () => ({
    user: {},
    sheet: [],
    details: {
      tags: []
    },
    infobox: undefined
  }),
  asyncData({params}) {
    return { tags_available }
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
