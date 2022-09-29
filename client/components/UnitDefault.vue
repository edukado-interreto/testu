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
              :shuffle="shuffle"
              :error-explanation="token.errorExplanation"
              ref="gap"
              @answer="on_answer($event, i, j)"
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
    {{ score_awarded }} / {{ score_available }}
  </div>
</template>
<script>
export default {
  name: 'UnitDefault',
  props: [ 'code', 'shuffle' ],
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
    }
  },
  computed: {
    score_available() {
      return this.parsed.flatMap(
        row => row.filter(t => t.token === 'gap')
      ).length
    },
    parsed: function() {
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
