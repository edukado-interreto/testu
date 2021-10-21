<template>
  <div class="editor">
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
    <div v-if="false"><pre>{{ parsed }}</pre></div>
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
  pre {
    white-space: break-spaces;
  }
  li {
    line-height: 3.5em;
    height: auto;
  }
</style>
