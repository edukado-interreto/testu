<script setup lang="ts">
const { confetti_shoot } = useConfettiShoot()

const emit = defineEmits(["input", "update:answer"])
const props = defineProps<{
  value: string
  options: string[]
  shuffle: boolean // bool: whether shuffle the options
  ignore_case: boolean // bool: whether to ignore the case
  once: boolean // bool: if true, allow only one try
  errorExplanation: boolean // string: message to display when picked answer is wrong
  readonly: boolean
  silent: boolean
}>()

const answer: Ref<string | undefined> = ref(undefined)

created(() => {
  // This will preload the answer on create.
  // Note that if the parent component changes
  // the prop 'value' afterwards, it will not
  // update the internal 'answer' variable.
  answer.value = props.value
})

const icon = computed(() => {
  if (props.silent) return
  if (props.success === undefined) return
  return props.success ? "mdi-check-bold" : "mdi-close-thick"
})

const error_messages = computed(() => {
  if (props.silent) return
  if (props.success !== false) return
  return props.errorExplanation
})

const choices = computed(() => {
  /**
       * Return the array of the possible answers to choose from.
       + The array contains objects in the form:
       * { "value": <string>, "right": <bool> }
       */

  // shuffle makes no sense in open answers

  //if (props.shuffle) {
  //  return props.shuffle_array(
  //    props.options
  //  )
  //}

  return props.options
})
const longest_choice_length = computed(() => {
  /**
   * Return the length in character of the longest
   * answer that one can choice (to calculate gap width)
   * @returns {int}
   */
  return Math.max(...props.choices.map((s) => s.value.length))
})
const gap_width = computed(() => {
  /**
   * Returns the css value used to set the gap width
   * @returns {str}
   */

  if (props.longest_choice_length === 0) return "30ch"
  // open answer without options, return a standard size
  // that should fit for a generic answer

  return props.longest_choice_length + 7 + "ch"
  // FIXME
  // heuristic calculation: to display the string "0"
  // into the v-select, a minimum width of 8ch was
  // found to be required. Hence, assuming that any
  // character has roughly the same width of "0", we
  // do the math on the longest answer's length.
  // Note that this assumption is by no mean accurate
  // and changing the styling or the icon slots etc.
  // of the v-select will have an inpact on it.
})
const success = computed(() => {
  /**
   * @returns: true | false | undefined
   */

  const adapt_str = (s) => (s && props.ignore_case ? s.toLowerCase() : s)

  const current_option = props.options.find(
    (e) => adapt_str(e.value) === adapt_str(props.answer),
  )

  if (props.options.every((o) => o.right === true)) {
    // the options list contains only one (or more) right option(s),
    // e.g.: "2+2 = [+4]" or "red is a [+color|+colour]".
    // In this case, we consider wrong (success = false) any
    // other answers apart from the empty string (success = undefined).
    if (!props.answer) return undefined
    return !!current_option
  }

  if (!current_option) return undefined

  return current_option.right
})

const on_change = () => {
  emit("update:answer", answer)

  if (silent) return
  if (process.server) return
  if (success === true) {
    confetti_shoot(props.$refs.select.$refs["input-slot"])
  }
}

watch(answer, (value) => {
  emit("input", value)
})
</script>

<template>
  <v-text-field
    ref="select"
    dense
    :style="'display:inline-block; width: ' + gap_width"
    v-model="answer"
    :success="!silent && success === true"
    :error-messages="error_messages"
    hide-details="auto"
    :error="!silent && success === false"
    :prepend-inner-icon="icon"
    @input="on_change"
    :readonly="readonly || (once && success !== undefined)"
/>
</template>
