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
              :token="token"
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
  props: [ 'code' ],
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
            let ret = { token: 'gap' }
            let options = value.split("|")
            ret.rights = options.slice(0, 1)
            ret.wrongs = options.slice(1)
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
    margin-bottom: 1.5em;
    line-height: 3em;
  }
  .pre-line { white-space: pre-line; }
</style>
