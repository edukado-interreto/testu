<template>
  <div class="editor">
    <div class="gap_demo">
      <ol>
        <li
          v-for="(phrase, i) in parsed"
          :key="i"
          class="pre-line"
        >
          <template v-for="(token, j) in phrase">
            <PlayGapSelect
              :key="j"
              v-if="token.token === 'gap'"
              :options="token.options"
              :value="token.answer"
              :shuffle="shuffle"
              :error-explanation="token.errorExplanation"
              :readonly="readonly"
              ref="gap"
              @answer="on_answer($event, i, j)"
              :silent="silent"
            ></PlayGapSelect>
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
export default {
  name: 'UnitDefault',
  props: [ 'code', 'shuffle', 'solved', 'readonly', 'silent' ],
  data: () => ({
    score_awarded: 0
  }),
  methods: {
    on_answer(answer, i, j) {
      // We use this event to update the amount of
      // right answers. We access the computed
      // 'success' prop of each child component
      // to get the amount of successful answers.
      console.log(answer.value, i, j)
      this.score_awarded = this.$refs.gap.filter(
        c => !!c.success
      ).length
    },
    get_solved() {
      // inject the answers into "parsed"
      // and return the whole object
      let i = 0
      return this.parsed.map(
        s => s.map(t => {
          if (t.token != 'gap') return t
          t.answer = this.$refs.gap[i].answer
          i++
          return t
        })
      )
    }
  },
  computed: {
    score_available() {
      return this.parsed.flatMap(
        row => row.filter(t => t.token === 'gap')
      ).length
    },
    parsed: function() {

      if (this.solved !== undefined) return this.solved
      // if the parent component provided a 'solved' prop,
      // bypass 'code' and load the 'solved' object which
      // contains the already parsed 'code' with answers
      // included.

      let ret = this.code.split(
        "\n\n"
      ).map(s => {
        return s.split(/[\[\]]/gi).map((value, i) => {
          if (i % 2 == 0) {
            // is text
            return { token: 'text', value }
          } else {
            // is gap
            if (!value) return { value: "" }
            let ret = {
              token: 'gap',
              options: []
            }
            value.split("|").forEach((v, i, a) => {

              // a prepending '+' in an option marks
              // a right answer: set ret.right accordingly
              // and remove the leading '+' from the option
              let right = false
              if (v[0] == '+') {
                right = true
                v = v.slice(1)
              }

              // a '~' in the last option introduces a
              // message to show when a wrong answer is given,
              // e.g. [cat|+fish|dog~It can swim!]
              // remove that message from the option and use
              // it as ret.errorExplanation
              if (i === a.length-1) {
                [ v, ret.errorExplanation ] = v.split("~")
              }

              ret.options.push({
                value: v,
                right
              })
            })
            return ret
          }
        }).filter(t => t.value != "")
      });
      return ret
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
