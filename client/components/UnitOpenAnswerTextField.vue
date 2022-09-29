<template>
  <v-text-field
    ref="select"
    dense
    :style="'display:inline-block; width: ' + gap_width"
    v-model="answer"
    :success="success === true"
    :error-messages="success === false ? errorExplanation : undefined"
    hide-details="auto"
    :error="success === false"
    :prepend-inner-icon="success === undefined ? undefined : (success ? 'mdi-check-bold' : 'mdi-close-thick')"
    @change="on_change"
    :readonly="once && success !== undefined"
  >
  </v-text-field>
</template>
<script>
import confetti_shoot from '~/mixins/confetti_shoot.js'
export default {
  name: 'UnitOpenAnswerTextField',
  props: [
    "options",
    "shuffle", // bool: wether shuffle the options
    "once", // bool: if true, allow only one try
    "error-explanation", // string: message to display when picked answer is wrong 
  ],
  mixins: [
    confetti_shoot
  ],
  data: () => ({
    answer: undefined
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
      const current_option = this.options.find(
        e => e.value === this.answer
      )

      if (!current_option) return undefined

      return current_option.right
    }
  },
  methods: {
    on_change: function() {

      this.$emit('answer', this.answer)

      if (process.server) return
      if (this.success === true) {
        this.confetti_shoot(
          this.$refs.select.$refs['input-slot']
        )
      }
    },
  },
}
</script>

