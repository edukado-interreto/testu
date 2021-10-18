<template>
  <div class="editor">
    <textarea class="editor_area" v-model="code"></textarea>
    <div class="gap_demo">
      <ol>
        <li v-for="phrase in parsed">
          <template v-for="token in phrase">
            <PlayGapSelect
              v-if="token.token === 'gap'"
              :token="token"
            ></PlayGapSelect>
            <span v-if="token.token === 'text'">{{token.value}}</span>
          </template>
        </li>
      </ol>
    </div>
    <div class="code"><pre>{{ parsed }}</pre></div>
  </div>
</template>
<script>
export default {
  name: 'GapsEditor',
  data: () => ({
    code: "To [be|is] or not to be, [that|those] is the question\n\nThe dog [has|is|gives] eaten [its|it's] food"
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
  pre {
    white-space: break-spaces;
  }
  .editor_area {
    width: 500px;
    height: 120px;
    margin: .5em;
    padding: .5em;
    border: 0;
    font-family: monospace;
    font-size: 12pt;
    line-height: 1.2em;
  }
</style>
