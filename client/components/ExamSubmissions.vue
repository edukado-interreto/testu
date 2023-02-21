<template>
  <v-row>
    <v-col>
      <v-select
        outlined
        dense
        :items="submissions_items"
        v-model="submissions_index"
      ></v-select>
    </v-col>
    <v-col>
      <v-btn
        icon
        @click="submissions_index -= 1"
        :disabled="submissions_index == 0"
      ><v-icon>mdi-chevron-left</v-icon></v-btn>
      {{ nth_of_total }}
      <v-btn
        icon
        @click="submissions_index += 1"
        :disabled="submissions_index == submissions_items.length-1"
      ><v-icon>mdi-chevron-right</v-icon></v-btn>
    </v-col>
  </v-row>
</template>
<script>
export default {
  props: [ 'submissions' ],
  data: () => ({
    submissions_index: 0,
  }),
  computed: {
    nth_of_total() {
      const of = 'of'
      const len = this.submissions_items.length
      if (len == 0) return `0 ${of} 0`
      return `${this.submissions_index+1} ${of} ${len}`
    },
    current_submission() {
        return this.submissions_items[this.submissions_index].data
    },
    submissions_items() {
      return this.submissions.sort(
        (a, b) => b.submitted - a.submitted
      ).map((e, i) => ({
        value: i,
        text: (
          e.author.display_name + ' (' +
          e.submitted.toLocaleString('en-US') +
          ')'
        ),
        data: e,
      }))
    }
  }
}
</script>
