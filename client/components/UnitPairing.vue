<template>
  <div>
    <v-row dense v-for="(pair, i) in drags" :key="parsed[i][1]">
      <v-col cols="4">
        <div class="mr-4">
          <!--
            we use redundant divs because binding some events
            to v-sheet elements results in a buggy behaviour
          -->
          <div
            v-if="pair[0] !== null"
            :draggable="movable[i][0]"
            @dragstart="on_dragstart($event, i, 0)"
          >
            <v-sheet
              rounded
              :elevation="2"
              class="pa-1"
              style="position:relative;"
            >
              <div
                class="pa-1"
              >{{pair[0]}}</div>
              <v-icon
                class="pa-2"
                style="position:absolute; right: 0; top: 0; cursor: move;"
                @mouseenter="$set(movable[i], 0, true)"
                @mouseleave="$set(movable[i], 0, false)"
              >mdi-drag</v-icon>
            </v-sheet>
          </div>
          <v-sheet
            v-else
            rounded
            class="pa-2 grey lighten-4 grey--text text-center"
            @drop="on_drop($event, i, 0)"
            @dragenter="on_dragenter($event, i, 0)"
            @dragleave="on_dragleave($event, i, 0)"
            @dragover="on_dragover($event, i, 0)"
          >&nbsp;</v-sheet>
        </div>
      </v-col>
      <v-col cols="4">
        <div
          v-if="pair[1] !== null"
          :draggable="movable[i][1]"
          @dragstart="on_dragstart($event, i, 1)"
        >
          <v-sheet
            rounded
            :elevation="2"
            class="pa-1"
            style="position:relative;"
          >
            <div
              class="pa-1"
            >{{pair[1]}}</div>
            <v-icon
              class="pa-2"
              style="position:absolute; right: 0; top: 0; cursor: move;"
              @mouseenter="$set(movable[i], 1, true)"
              @mouseleave="$set(movable[i], 1, false)"
            >mdi-drag</v-icon>
          </v-sheet>
        </div>
        <v-sheet
          v-else
          rounded
          class="pa-2 grey lighten-4 grey--text text-center"
          @drop="on_drop($event, i, 1)"
          @dragenter="on_dragenter($event, i, 1)"
          @dragleave="on_dragleave($event, i, 1)"
          @dragover="on_dragover($event, i, 1)"
        >drop here</v-sheet>
      </v-col>
      <v-col cols="4">
        <v-sheet
          rounded
          :elevation="2"
          class="pa-1"
        >
          <div
            class="pa-1"
          >{{parsed[i][1]}}</div>
        </v-sheet>
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
    drags: [],   // see update_dragging
    movable: [], // for info
    overed: [],  // about these
  }),
  mounted() {
    this.update_dragging()
  },
  methods: {
    test() {
      console.log("TEST")
    },
    on_dragstart(e, src_row, src_col) {
      console.log("dragstart, component", this._uid)
      e.dataTransfer.setData("component", this._uid)
      e.dataTransfer.setData("src_row", src_row)
      e.dataTransfer.setData("src_col", src_col)
    },
    on_dragleave(e, dst_row, dst_col) {
      this.$set(this.overed[dst_row], dst_col, false)
    },
    on_dragover(e, dst_row, dst_col) {
      if (this.drags[dst_row][dst_col] !== null) return;
      e.preventDefault();
    },
    on_dragenter(e, dst_row, dst_col) {
      if (this.drags[dst_row][dst_col] !== null) return;
      e.preventDefault();
      this.$set(this.overed[dst_row], dst_col, true)
    },
    on_drop(e, dst_row, dst_col) {
      console.log("drop")
      console.log({
        component: e.dataTransfer.getData("component"),
        dst_row,
        dst_col
      })
      if (
        this._uid != e.dataTransfer.getData("component")
      ) return // prevent cross-unit drag and drop
      e.preventDefault()
      const src_row = e.dataTransfer.getData("src_row")
      const src_col = e.dataTransfer.getData("src_col")
      console.log("from", src_row, src_col);
      console.log("to", dst_row, dst_col);
      this.$set(this.drags[dst_row], dst_col, this.drags[src_row][src_col])
      this.$set(this.drags[src_row], src_col, null)
      this.$set(this.overed[dst_row], dst_col, false)
    },
    update_dragging() {
      // this.drags: two-dimensional array with values
      // of the draggable items.
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

      // this.movable: two-dimensional array of booleans.
      // Represents the 'draggable' html attribute of the items.
      // Since we drag using a handle, we turn on this
      // attribute only when the mouse enters the handle
      // and set it back to off on mouse leave.
      this.movable = this.parsed.map(
        p => [false, false]
      )

      // this.overed: two-dimensional array of booleans.
      // Will be set to true on dragenter, false on dragleave.
      // Used to style the drop zone.
      this.overed = this.parsed.map(
        p => [false, false]
      )

    },
  },
  computed: {
    score_available() {
      return 0 // TODO
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
