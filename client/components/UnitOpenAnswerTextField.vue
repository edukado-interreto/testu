<template>
  <v-text-field
    ref="select"
    dense
    :style="'display:inline-block; width: ' + gap_width"
    v-model="answer"
    :success="!silent && success === true"
    :error-messages="error_messages"
    hide-details="auto"
    :error="!silent && success === false"
    :prepend-inner-icon="icon"
    @input="on_change"
    :readonly="readonly || (once && success !== undefined)"
  ></v-text-field>
</template>
<script>
import confetti_shoot from "~/mixins/confetti_shoot.js"
export default {
  name: "UnitOpenAnswerTextField",
  props: [
    "value",
    "options",
    "shuffle", // bool: wether shuffle the options
    "ignore_case", // bool: wether to ignore the case
    "once", // bool: if true, allow only one try
    "error-explanation", // string: message to display when picked answer is wrong
    "readonly",
    "silent",
  ],
  mixins: [confetti_shoot],
  data: () => ({
    answer: undefined,
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
      return this.success ? "mdi-check-bold" : "mdi-close-thick"
    },
    error_messages() {
      if (this.silent) return
      if (this.success !== false) return
      return this.errorExplanation
    },
    choices: function () {
      /**
       * Return the array of the possible answers to choose from.
       + The array contains objects in the form:
       * { "value": <string>, "right": <bool> }
       */

      // shuffle makes no sense in open answers

      //if (this.shuffle) {
      //  return this.shuffle_array(
      //    this.options
      //  )
      //}

      return this.options
    },
    longest_choice_length: function () {
      /**
       * Return the length in character of the longest
       * answer that one can choice (to calculate gap width)
       * @returns {int}
       */
      return Math.max(...this.choices.map((s) => s.value.length))
    },
    gap_width: function () {
      /**
       * Returns the css value used to set the gap width
       * @returns {str}
       */

      if (this.longest_choice_length === 0) return "30ch"
      // open answer without options, return a standard size
      // that should fit for a generic answer

      return this.longest_choice_length + 7 + "ch"
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
    success: function () {
      /**
       * @returns: true | false | undefined
       */

      const adapt_str = (s) => (s && this.ignore_case ? s.toLowerCase() : s)

      const current_option = this.options.find(
        (e) => adapt_str(e.value) === adapt_str(this.answer),
      )

      if (this.options.every((o) => o.right === true)) {
        // the options list contains only one (or more) right option(s),
        // e.g.: "2+2 = [+4]" or "red is a [+color|+colour]".
        // In this case, we consider wrong (success = false) any
        // other answers apart from the empty string (success = undefined).
        if (!this.answer) return undefined
        return !!current_option
      }

      if (!current_option) return undefined

      return current_option.right
    },
  },
  methods: {
    on_change: function () {
      this.$emit("update:answer", this.answer)

      if (this.silent) return
      if (process.server) return
      if (this.success === true) {
        this.confetti_shoot(this.$refs.select.$refs["input-slot"])
      }
    },
  },
  watch: {
    answer(v) {
      this.$emit("input", v)
    },
  },
}
</script>
