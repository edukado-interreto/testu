<template>
  <div class="editor">
    <div class="gap_demo">
      <ol>
        <li v-for="(phrase, i) in parsed" :key="i" class="pre-line">
          <template v-for="(token, j) in phrase">
            <UnitMultipleChoiceCheckbox
              :key="j"
              v-if="token.token === 'gap'"
              :options="token.options"
              :value="token.answer"
              :shuffle="solved === undefined ? shuffle : false"
              :error-explanation="token.errorExplanation"
              :readonly="readonly"
              ref="gap"
              @answer="on_answer($event, i, j)"
              :silent="silent"
            ></UnitMultipleChoiceCheckbox>
            <span
              :key="j"
              v-if="token.token === 'text'"
              v-text="token.value"
            ></span>
          </template>
        </li>
      </ol>
    </div>
  </div>
</template>
<script>
import tokenize from "~/mixins/tokenize.js"
export default {
  name: "UnitMultipleChoice",
  props: ["code", "shuffle", "solved", "readonly", "silent"],
  mixins: [tokenize],
  data: () => ({
    score_awarded: 0,
  }),
  methods: {
    on_answer(answer, i, j) {
      // We use this event to update the amount of
      // right answers. We access the computed
      // 'success' prop of each child component
      // to get the amount of successful answers.
      this.score_awarded = this.$refs.gap.filter((c) => !!c.success).length
    },
    get_solved() {
      // inject the answers into "parsed"
      // and return the whole object
      let i = 0
      const parsed_filled = this.parsed.map((s) =>
        s.map((t) => {
          if (t.token != "gap") return t
          const new_t = JSON.parse(JSON.stringify(t))
          new_t.answer = this.$refs.gap[i].answer
          new_t.options = this.$refs.gap[i].choices
          i++
          return new_t
        }),
      )
      return {
        parsed: parsed_filled,
      }
    },
  },
  computed: {
    score_available() {
      return this.parsed.flatMap((row) => row.filter((t) => t.token === "gap"))
        .length
    },
    parsed: function () {
      if (this.solved !== undefined) return this.solved.parsed
      // if the parent component provided a 'solved' prop,
      // bypass 'code' and load the 'solved' object which
      // contains the already parsed 'code' with includes
      // the answers and keeps the options shuffling order

      if (!this.code) return []

      return this.tokenize(this.code)
    },
  },
}
</script>
<style scoped>
li {
  margin-bottom: 1.25em;
  line-height: 2.25em;
}
.pre-line {
  white-space: pre-line;
}
</style>
