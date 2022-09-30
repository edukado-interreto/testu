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
    >
      <template v-slot:label>
        <span class="black--text">{{ choice.value }}</span>
        <v-icon
          v-if="success[i] === true"
          class="mx-1"
          color="success"
        >mdi-check-bold</v-icon>
        <v-icon
          v-if="success[i] === false"
          class="mx-1"
          color="error"
        >mdi-close-thick</v-icon>
      </template>
    </v-checkbox>
  </div>
  <!--v-select
    ref="select"
    dense
    :style="'display:inline-block; width: ' + gap_width"
    :items="choices"
    item-text="value"
    item-value="value"
    return-object
    v-model="answer"
    :success="success === true"
    :error-messages="success === false ? errorExplanation : undefined"
    hide-details="auto"
    :error="success === false"
    :prepend-inner-icon="success === undefined ? undefined : (success ? 'mdi-check-bold' : 'mdi-close-thick')"
    @change="on_change"
    :readonly="once && success !== undefined"
  >
  </v-select-->
</template>
<script>
import confetti_shoot from '~/mixins/confetti_shoot.js'
export default {
  name: 'UnitMultipleChoiceCheckbox',
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
    answer: []
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
    success: function() {
      /**
       * @returns: [ true | false ]
       */
      return this.choices.map(c => {
        const checked = this.answer.includes(c.value)
        if (checked && c.right === true) return true
        if (!checked && c.right === false) return true
        return false
      })
    }
  },
  methods: {
    on_change: function(i) {

      this.$emit('answer', this.answer)

      if (process.server) return
      if (this.success[i] === true) {
        this.confetti_shoot(
          this.$refs.checkbox[i].$el.querySelector('input')
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
}
</script>
