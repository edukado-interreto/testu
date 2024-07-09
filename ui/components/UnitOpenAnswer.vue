<script setup lang="ts">
const tokenize = useTokenize()
const props = defineProps<{
  code: string
  shuffle: boolean
  solved: { parsed: string[] }
  readonly: boolean
  silent: boolean
  ignore_case: boolean
}>()

const score_awarded = ref(0)

const gaps: Ref<Element[]> = ref([])

const on_answer = (answer, i, j) => {
  // We use this event to update the amount of
  // right answers. We access the computed
  // 'success' prop of each child component
  // to get the amount of successful answers.
  props.score_awarded = gaps.value.filter((c) => !!c.success).length
}
const get_solved = () => {
  // inject the answers into "parsed"
  // and return the whole object
  let i = 0
  const parsed_filled = parsed.map((phrase) =>
    phrase.map((token) => {
      if (token.token != "gap") return token
      token.answer = gaps.value[i].answer
      i++
      return token
    }),
  )
  return {
    parsed: parsed_filled,
  }
}
const score_available = computed(() => {
  return parsed.flatMap((line) => line.filter((t) => t.token === "gap")).length
})
const parsed: ComputedRef<Token[][]> = computed(() => {
  if (props.solved !== undefined) return props.solved.parsed
  // if the parent component provided a 'solved' prop,
  // bypass 'code' and load the 'solved' object which
  // contains the already parsed 'code' with answers
  // included.

  return tokenize(props.code)
})
</script>

<template>
  <div class="editor">
    <div class="gap_demo">
      <ol>
        <li v-for="(phrase, i) in parsed" :key="i" class="pre-line">
          <template v-for="(token, j) in phrase">
            <UnitOpenAnswerTextField
              :key="j"
              v-if="token.token === 'gap'"
              :options="token.options || []"
              :value="token.answer || ''"
              :shuffle="shuffle"
              :ignore_case="ignore_case"
              :once="false"
              :error-explanation="token.errorExplanation"
              :readonly="readonly"
              :ref="(el) => gaps.push(el)"
              :silent="silent"
              :success="token.right || false"
              @answer="on_answer($event, i, j)"
            />
            <span :key="j" v-if="token.token === 'text'" v-text="token.value" />
          </template>
        </li>
      </ol>
    </div>
  </div>
</template>

<style scoped>
li {
  margin-bottom: 1.25em;
  line-height: 2.25em;
}
.pre-line {
  white-space: pre-line;
}
</style>
