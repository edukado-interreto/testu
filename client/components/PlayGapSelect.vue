<template>
  <v-select
    ref="select"
    dense
    :style="'display:inline-block; width: ' + gap_width"
    :items="choices"
    item-text="value"
    item-value="value"
    return-object
    v-model="answer"
    :success="!silent && (success === true)"
    :error-messages="error_messages"
    hide-details="auto"
    :error="!silent && (success === false)"
    :prepend-inner-icon="icon"
    @change="on_change"
    :readonly="readonly || (once && success !== undefined)"
  >
  </v-select>
</template>
<script>
import confetti_shoot from '~/mixins/confetti_shoot.js'
export default {
  name: 'PlayGapSelect',
  props: [
    "value",
    "options",
    "shuffle", // bool: wether shuffle the options
    "once", // bool: if true, allow only one try
    "error-explanation", // string: message to display when picked answer is wrong 
    "readonly",
    "silent",
  ],
  mixins: [
    confetti_shoot
  ],
  data: () => ({
    answer: undefined
  }),
  created() {
    // This will preload the answer on create.
    // Note that if the parent component changes
    // the prop 'value' afterwards, it will not
    // update the internal 'answer' variable.
    this.answer = this.value
  },
  computed: {
    icon() {
      if (this.silent) return
      if (this.success === undefined) return
      return this.success ? 'mdi-check-bold' : 'mdi-close-thick'
    },
    error_messages() {
      if (this.silent) return
      if (this.success !== false) return
      return this.errorExplanation
    },
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
      if ('right' in (this.answer || {})) {
        // the gap was filled with a value:
        // return the value's rightness
        return this.answer.right
      }
      // the gap is still not filled
      return undefined
    }
  },
  methods: {
    on_change: function() {

      this.$emit('update:answer', this.answer)

      if (this.silent) return
      if (process.server) return
      if (this.success === true) {
        this.confetti_shoot(
          this.$refs.select.$refs['input-slot']
        )
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
  },
  watch: {
    answer(v) {
      this.$emit('input', v)
    }
  }
}
</script>
