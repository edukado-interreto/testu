<template>
  <div class="editor">
    {{ test }}
    <div class="gap_demo">
      <draggable
        v-model="test"
      >
        <v-slide-y-transition group>
          <div v-for="pair in test" :key="pair.id"><v-card-text>{{pair.name}}</v-card-text></div>
        </v-slide-y-transition group>
      </draggable>
    </div>
  </div>
</template>
<script>
import draggable from 'vuedraggable'
export default {
  components: {
    draggable
  },
  name: 'UnitPairing',
  props: [ 'code', 'shuffle' ],
  data: () => ({
    score_awarded: 0,
    test: [
      { name:'cane', id: 0 },
      { name:'mucca', id: 1 },
      { name:'casa', id: 2 },
      { name:'topo', id: 3 },
    ],
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
      ).map((s, i) => {
        let [src, dst] = s.split("=").map(s => s.trim())
        if (dst === undefined) {
          dst = `${i+1}`
        }
        return [src, dst]
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
