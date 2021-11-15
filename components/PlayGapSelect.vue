<template>
  <v-select
    ref="select"
    dense
    :style="'display:inline-block; width: ' + gap_width"
    :items="choices"
    item-text="value"
    item-value="value"
    return-object
    v-model="value"
    :success="success === true"
    hide-details="auto"
    :error="success === false"
    :prepend-inner-icon="success === undefined ? undefined : (success ? 'mdi-check-bold' : 'mdi-close-thick')"
    @change="on_change"
    :readonly="once && success !== undefined"
  >
  </v-select>
</template>
<script>
export default {
  name: 'PlayGapSelect',
  props: [
    "options",
    "shuffle", // bool: wether shuffle the options
    "once", // bool: if true, allow only one try
  ],
  data: () => ({
    value: undefined
  }),
  computed: {
    choices: function() {
      /**
       * Return the array of the possible answers to choose from.
       + The array contains objects in the form:
       * { "value": <string>, "right": <bool> }
       */

      if (this.shuffle) {
        return this.shuffle_array(
          this.options
        )
      }

      return this.options

    },
    longest_choice_length: function() {
      /**
       * Return the length in character of the longest
       * answer that one can choice (to calculate gap width)
       * @returns {int}
       */
      return Math.max(
        ...this.choices.map(
          s => s.value.length
        )
      )
    },
    gap_width: function() {
      /**
       * Returns the css value used to set the gap width
       * @returns {str}
       */
      return this.longest_choice_length + 7 + 'ch';
      // FIXME
      // heuristic calculation: to display the string "0"
      // into the v-select, a minimum width of 8ch was
      // found to be required. Hence, assuming that any
      // character has roughly the same width of "0", we
      // do the math on the longest answer's length.
      // Note that this assumption is by no mean accurate
      // and changing the styling or the icon slots etc.
      // of the v-select will have an inpact on it.
    },
    success: function() {
      /**
       * @returns: true | false | undefined
       */
      if ('right' in (this.value || {})) {
        // the gap was filled with a value:
        // return the value's rightness
        return this.value.right
      }
      // the gap is still not filled
      return undefined
    }
  },
  methods: {
    on_change: function() {
      if (process.server) return
      if (this.success === true) {
        this.$confetti({
          angle: 90,
          spread: 110,
          particleCount: 60,
          //origin: { x: 0.5, y: 0.5 },
          origin: this.confetti_gun_coords(
            this.$refs.select.$refs['input-slot']
          ),
          decay: 0.8,
          disableForReducedMotion: true
        });
      }
    },
    shuffle_array: function(in_array) {
      /**
       * Shuffle an array using the Fisher-Yates algorithm,
       * O(n), un-biased.
       */

      const out_array = in_array.slice();
      // clone the input array

      let currentIndex = out_array.length, randomIndex;

      // While there remain elements to shuffle...
      while (currentIndex != 0) {
        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        // And swap it with the current element.
        [out_array[currentIndex], out_array[randomIndex]] = [
          out_array[randomIndex], out_array[currentIndex]];
      }

      return out_array;
    },
    confetti_gun_coords: function(element) {
      /**
       * Calculate the coordinates x and y in order
       * to shoot some confetti from the given html element.
       * @param {HTMLElement} element
       * @returns {{ x: {Number}, y: {Number} }}
       */
      const rect = element.getBoundingClientRect()

      // coordinates in pixels
      const px_x = rect.left + rect.width  / 2  // center
      const px_y = rect.top  + rect.height + 15 // underneath
      // since we shoot the confetti straight upwards,
      // it is more pretty if the confetti come from
      // below the element, hence the offset added in px_y.

      // coordinates as values between 0 and 1,
      // as required by the confetti api
      return {
        x: px_x / window.innerWidth,
        y: px_y / window.innerHeight
      }
    }
  },
}
</script>
