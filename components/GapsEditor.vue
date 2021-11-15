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
            value.split("|").forEach(v => {
              let right = false
              if (v[0] == '+') {
                right = true
                v = v.slice(1)
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
