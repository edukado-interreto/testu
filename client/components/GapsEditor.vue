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
  name: 'GapsEditor',
  props: [ 'code', 'shuffle' ],
  data: () => ({
  }),
  computed: {
    parsed: function(v) {
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
