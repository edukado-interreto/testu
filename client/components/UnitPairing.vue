<template>
  <div>
    <v-row v-for="pair in drags">
      <v-col cols="4">
        <v-sheet
          rounded
          :elevation="2"
          class="pa-1 mr-4"
          style="position:relative;"
        >
          <div
            class="pa-1"
          >{{pair[0]}}</div>
          <v-icon
            class="pa-2"
            style="position:absolute; right: 0; top: 0; cursor: move;"
          >mdi-drag</v-icon>
        </v-sheet>
      </v-col>
      <v-col cols="4">
        x
      </v-col>
      <v-col cols="4">
        x
      </v-col>
    </v-row>
  </div>
</template>
<script>
export default {
  name: 'UnitPairing',
  props: [ 'code', 'shuffle' ],
  data: () => ({
    score_awarded: 0,
    drags: [],
  }),
  mounted() {
    this.update_dragging()
  },
  methods: {
    update_dragging() {
      // A two-dimensional array with the draggable items.
      // Represents the two columns of items that can be
      // moved around. The first column is the "home"
      // column, the second one is the "guess" column.
      // At first, all values are in the home column.
      // Eventually the user will move all of them to the
      // guess column to complete the exercise.
      // The values can be moved freely back and forth
      // from the home to the guess column during the 
      // solving process.
      // E.g.
      // parsed: [['pomo', 'mela'], ['domo', 'casa']]
      // drags: [['domo', null], ['pomo', null]]
      this.drags = this.parsed.map(
        p => p[0]
      ).sort(
        (a, b) => a.localeCompare(b) // TODO: shuffle if the flag is set
      ).map(
        e => [e, null]
      )
    },
    on_answer(answer, i, j) {
      // We use this event to update the amount of
      // right answers. We access the computed
      // 'success' prop of each child component
      // to get the amount of successful answers.
      console.log(answer.value, i, j)
      this.score_awarded = this.$refs.gap.filter(
        c => !!c.success
      ).length
    }
  },
  computed: {
    score_available() {
      return this.parsed.flatMap(
        row => row.filter(t => t.token === 'gap')
      ).length
    },
    parsed: function() {
      let ret = this.code.split(
        "\n\n"
      ).map((s, i) => {
        let [src, dst] = s.split("=").map(s => s.trim())
        // if no = sign is found, the destination will be
        // the row number, i.e. ordering exercise
        if (dst === undefined) {
          dst = `${i+1}`
        }
        return [src, dst]
      });
      return ret
    }
  },
  watch: {
    parsed() {
      this.update_dragging()
    }
  }
}
</script>
<style scoped>
  li {
    margin-bottom: 1.25em;
    line-height: 2.25em;
  }
  .pre-line { white-space: pre-line; }
</style>
