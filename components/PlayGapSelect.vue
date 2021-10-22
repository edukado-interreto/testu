<template>
  <v-select
    ref="select"
    dense
    hide-details
    :style="'display:inline-block; width: ' + gap_width"
    :items="choices"
    v-model="value"
    :success="success === true"
    :error="success === false"
    :prepend-inner-icon="success === undefined ? undefined : (success ? 'mdi-check-bold' : 'mdi-close-thick')"
  ></v-select>
</template>
<script>
export default {
  name: 'PlayGapSelect',
  props: [ "token" ],
  data: () => ({
    value: undefined
  }),
  computed: {
    choices: function() {
      /**
       * Return the array of the possible answers to choose from,
       * including right ones and wrong ones, in random order.
       * @returns {str[]}
       */
      return this.shuffle(
        this.token.rights.concat(
          this.token.wrongs
        )
      )
    },
    longest_choice_length: function() {
      /**
       * Return the length in character of the longest
       * answer that one can choice (to calculate gap width)
       * @returns {int}
       */
      return Math.max(
        ...this.choices.map(
          s => s.length
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
      if (this.token.rights.includes(this.value)) {
        return true
      }
      if (this.token.wrongs.includes(this.value)) {
        return false
      }
      return undefined
    }
  },
  methods: {
    shuffle: function(array) {
      /**
       * Shuffle an array using the Fisher-Yates algorithm,
       * O(n), un-biased.
       */
      let currentIndex = array.length,  randomIndex;
      // While there remain elements to shuffle...
      while (currentIndex != 0) {
        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        // And swap it with the current element.
        [array[currentIndex], array[randomIndex]] = [
          array[randomIndex], array[currentIndex]];
      }
      return array;
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
      // is more pretty if the confetti come from
      // below the element, hence the offset added in px_y.

      // coordinates as values between 0 and 1,
      // as requested by the confetti api
      return {
        x: px_x / window.innerWidth,
        y: px_y / window.innerHeight
      }
    }
  },
  watch: {
    success: function(val, oldVal) {
      if (process.server) return
      if (val === true) {
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
    }
  }
}
</script>
