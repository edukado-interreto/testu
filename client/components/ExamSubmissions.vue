<template>
  <div>
    <v-row class="sticky mb-6">
      <v-col>
        <v-select
          outlined
          dense
          :items="submissions_items"
          v-model="submissions_index"
          hide-details
        ></v-select>
      </v-col>
      <v-col>
        <v-btn
          icon
          @click="submissions_index -= 1"
          :disabled="submissions_index == 0"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
        {{ nth_of_total }}
        <v-btn
          icon
          @click="submissions_index += 1"
          :disabled="submissions_index == submissions_items.length - 1"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <SheetReview
      :key="current_submission.pk"
      :submission="current_submission"
    ></SheetReview>
    <!--
      We use 'key' to force reload the component 
      when changing current_submission,
      otherwise some fields may not get updated
      showing answers belonging to the first
      reviewed submission
    -->
  </div>
</template>
<script>
export default {
  props: ["submissions"],
  data: () => ({
    submissions_index: 0,
  }),
  computed: {
    nth_of_total() {
      const of = "of"
      const len = this.submissions_items.length
      if (len == 0) return `0 ${of} 0`
      return `${this.submissions_index + 1} ${of} ${len}`
    },
    current_submission() {
      return this.submissions_items[this.submissions_index]?.data
    },
    submissions_items() {
      return this.submissions
        .sort((a, b) => b.created - a.created)
        .map((e, i) => ({
          value: i,
          text:
            (e.created_by || `${e.guest} (guest)`) +
            " (" +
            e.created.toLocaleString("en-US") +
            ")",
          data: e,
        }))
    },
  },
}
</script>
<style scoped>
.sticky {
  position: sticky;
  top: 56px;
  z-index: 1;
  background: white;
  box-shadow: 0 12px 12px white;
}
</style>
