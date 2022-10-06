<template>
  <div class="mb-5">
    <v-row dense v-for="(pair, i) in drags" :key="parsed[i][1]">
      <v-col cols="4">
        <div class="mr-4 fill-height">
          <!--
            we use redundant divs because binding some events
            to v-sheet elements results in a buggy behaviour
          -->
          <div
            v-if="pair[0] !== null"
            :draggable="movable[i][0]"
            @dragstart="on_dragstart($event, i, 0)"
            class="fill-height"
          >
            <v-sheet
              rounded
              :elevation="2"
              class="pa-1 fill-height"
              style="position:relative;"
            >
              <div
                class="pa-1 mr-7"
              >
                <UnitPairingContent
                  :text="pair[0]"
                ></UnitPairingContent>
              </div>
              <v-icon
                class="pa-2"
                style="position:absolute; right: 0; top: 0; cursor: move;"
                @mouseenter="$set(movable[i], 0, true)"
                @touchstart="$set(movable[i], 0, true)"
                @mouseleave="$set(movable[i], 0, false)"
                @touchend="$set(movable[i], 0, false)"
              >mdi-drag</v-icon>
            </v-sheet>
          </div>
          <v-sheet
            v-else
            rounded
            :class="
              'pa-2 grey grey--text text-center fill-height '
              + (overed[i][0] ? 'lighten-2' : 'lighten-5')
            "
            @drop="on_drop($event, i, 0)"
            @dragenter="on_dragenter($event, i, 0)"
            @dragleave="on_dragleave($event, i, 0)"
            @dragover="on_dragover($event, i, 0)"
          >&nbsp;</v-sheet>
        </div>
      </v-col>
      <v-col cols="4" ref="guess_col">
        <div
          v-if="pair[1] !== null"
          :draggable="movable[i][1]"
          @dragstart="on_dragstart($event, i, 1)"
          class="fill-height"
        >
          <v-sheet
            rounded
            :elevation="2"
            class="pa-1 fill-height"
            style="position:relative;"
          >
            <div
              class="pa-1 mr-7"
            >
              <UnitPairingContent
                :text="pair[1]"
              ></UnitPairingContent>
            </div>
            <v-icon
              class="pa-2"
              style="position:absolute; right: 0; top: 0; cursor: move;"
              @mouseenter="$set(movable[i], 1, true)"
              @touchstart="$set(movable[i], 1, true)"
              @mouseleave="$set(movable[i], 1, false)"
              @touchend="$set(movable[i], 1, false)"
            >mdi-drag</v-icon>
          </v-sheet>
        </div>
        <v-sheet
          v-else
          rounded
          :class="
            'pa-2 grey grey--text '
            + 'd-flex justify-center align-center fill-height '
            + (overed[i][1] ? 'lighten-2' : 'lighten-4')
          "
          @drop="on_drop($event, i, 1)"
          @dragenter="on_dragenter($event, i, 1)"
          @dragleave="on_dragleave($event, i, 1)"
          @dragover="on_dragover($event, i, 1)"
        >
          <div style="pointer-events: none; touch-action: none;">
            drop here
          </div>
        </v-sheet>
      </v-col>
      <v-col cols="4" style="position: relative;">
        <v-sheet
          rounded
          :elevation="2"
          class="pa-1 mr-7 fill-height"
        >
          <div
            class="pa-1"
          >
            <UnitPairingContent
              :text="parsed[i][1]"
            ></UnitPairingContent>
          </div>
        </v-sheet>
        <div
          v-if="success !== undefined"
          style="position: absolute; right:4px; top: 10px"
        >
          <v-icon v-if="success[i] === true" color="success">mdi-check-bold</v-icon>
          <v-icon v-if="success[i] === false" color="error">mdi-close-thick</v-icon>
        </div>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import confetti_shoot from '~/mixins/confetti_shoot.js'
import shuffle_array from '~/mixins/shuffle_array.js'
export default {
  name: 'UnitPairing',
  props: [ 'code', 'shuffle' ],
  mixins: [
    confetti_shoot,
    shuffle_array
  ],
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
    on_dragstart(e, src_row, src_col) {
      console.log("dragstart, component", this._uid)
      e.dataTransfer.setData("text/plain", JSON.stringify({
        component: this._uid,
        row: src_row,
        col: src_col,
      }))
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
      let src
      try {
        src = JSON.parse(e.dataTransfer.getData("text"))
        if (src.component != this._uid) throw "Cross-component drop"
      } catch(e) {
        // abort if invalid json or cross-component drop
        this.$set(this.overed[dst_row], dst_col, false)
        return
      }
      e.preventDefault()
      this.$set(this.drags[dst_row], dst_col, this.drags[src.row][src.col])
      this.$set(this.drags[src.row], src.col, null)
      this.$set(this.overed[dst_row], dst_col, false)

      if (
        (dst_col == 1) // drop in guess column
        && (this.success[dst_row] === true)
      ) {
        this.confetti_shoot(
          this.$refs['guess_col'][dst_row]
        )
      }
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
        (a, b) => a.localeCompare(b)
      ).map(
        e => [e, null]
      )
      
      if (this.shuffle) {
        this.drags = this.shuffle_array(
          this.drags
        )
      }

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
    success() {
      return this.drags.map((pair, i) => {
        if (pair[1] === null) return undefined
        return pair[1] === this.parsed[i][0]
      })
    },
    score_available() {
      return 0 // TODO
    },
    parsed: function() {
      let ret = this.code.split(
        "\n\n"
      ).map((s, i) => {
        let [src, dst] = s.split(/==(.*)/s).map(s => s.trim())
        // split on the first occurrence of "==", e.g.
        // "a == b == c" => ["a", "b == c"]. Multiline.

        // if no "==" is found, the destination will be
        // the row number, i.e. ordering exercise
        if (!dst) {
          dst = `${i+1}`
        }
        console.log(src, dst)
        return [src, dst]
      }).filter(
        ([src, dst]) => !!src
      )
      return ret
    }
  },
  watch: {
    parsed() {
      this.update_dragging()
    },
    shuffle() {
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
