<template>
  <div>
    <v-checkbox
      dense
      v-for="(choice, i) in choices"
      v-model="answer"
      :value="choice.value"
      hide-details="auto"
      @change="on_change(i)"
      ref="checkbox"
      :key="choice.value"
      :readonly="readonly"
      :color="silent ? 'primary' : is_correct_answer(i) ? 'green' : 'grey'"
    >
      <template v-slot:label>
        <span
          class="black--text"
          :class="{
            'text-decoration-line-through': is_checked(i) && is_error(i),
            'font-weight-bold': is_correct_answer(i),
            'success--text': is_correct_answer(i),
          }"
        >
          {{ choice.value }}
        </span>
        <template v-if="!silent">
          <v-icon v-if="show_success_feedback[i]" class="mx-1" color="success">
            mdi-check-bold
          </v-icon>
          <v-icon
            v-if="is_checked(i) && is_error(i)"
            class="mx-1"
            color="error"
          >
            mdi-close-thick
          </v-icon>
        </template>
      </template>
    </v-checkbox>
  </div>
</template>
<script>
import confetti_shoot from "~/mixins/confetti_shoot.js"
export default {
  name: "UnitMultipleChoiceCheckbox",
  props: [
    "value",
    "options",
    "shuffle", // bool: whether shuffle the options
    "once", // bool: if true, allow only one try
    "error-explanation", // string: message to display when picked answer is wrong
    "readonly",
    "silent",
  ],
  mixins: [confetti_shoot],
  data: () => ({
    answer: [],
  }),
  created() {
    // This will preload the answer on create.
    // Note that if the parent component changes
    // the prop 'value' afterwards, it will not
    // update the internal 'answer' variable.
    this.answer = this.value || []
  },
  computed: {
    choices: function () {
      /**
       * Return the array of the possible answers to choose from.
       + The array contains objects in the form:
       * { "value": <string>, "right": <bool> }
       */

      if (this.shuffle) {
        return this.shuffle_array(this.options)
      }

      return this.options
    },
    success: function () {
      /**
       * The correctness status of each checkbox
       * @returns: [ true | false ]
       */
      return this.choices.map((c) => {
        const checked = this.answer.includes(c.value)
        if (checked && c.right === true) return true
        if (!checked && c.right === false) return true
        return false
      })
    },
    correct_answers: function () {
      return this.choices.map((c) => c.right)
    },
    show_success_feedback() {
      /**
       * Whether provide success feedback for each checkbox.
       * It is true if the option is correctly checked and all
       * other right options are checked as well. False otherwise.
       * @returns: [ true | false ]
       */
      return this.choices.map(
        (c, i) => this.success[i] && c.right && this.success.every(Boolean),
      )
    },
  },
  methods: {
    is_correct_answer: function (i) {
      if (this.silent === true) return false
      return this.correct_answers[i]
    },
    is_checked: function (i) {
      return this.answer.includes(this.choices[i].value)
    },
    is_error: function (i) {
      if (this.silent) return false
      return this.success[i] === false
    },
    on_change: function (i) {
      this.$emit("update:answer", this.answer)

      if (this.silent) return
      if (process.server) return
      if (this.show_success_feedback[i] === true) {
        this.confetti_shoot(this.$refs.checkbox[i].$el.querySelector("input"))
      }
    },
    shuffle_array: function (in_array) {
      /**
       * Shuffle an array using the Fisher-Yates algorithm,
       * O(n), un-biased.
       */

      const out_array = in_array.slice()
      // clone the input array

      let currentIndex = out_array.length,
        randomIndex

      // While there remain elements to shuffle...
      while (currentIndex != 0) {
        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex)
        currentIndex--
        // And swap it with the current element.
        ;[out_array[currentIndex], out_array[randomIndex]] = [
          out_array[randomIndex],
          out_array[currentIndex],
        ]
      }

      return out_array
    },
  },
  watch: {
    answer(v) {
      this.$emit("input", v)
    },
    silent() {
      this.answer.map((v) =>
        this.on_change(this.choices.findIndex((c) => c.value === v)),
      )
    },
  },
}
</script>
