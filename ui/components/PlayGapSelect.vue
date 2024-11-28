<script setup lang="ts">
import { ref, computed, watch, defineProps, defineEmits } from "vue"

type Props = {
  value: [string, Object]
  options: any[]
  shuffle: boolean
  once: boolean
  errorExplanation: string
  readonly: boolean
  silent: boolean
}

const props = defineProps<Props>()

const emit = defineEmits(["update:answer", "input"])

const select: Ref<HTMLElement | null> = ref(null)

const answer = ref(props.value)

// Computed properties
const icon = computed(() => {
  if (props.silent) return undefined
  if (success.value === undefined) return undefined
  return success.value ? "mdi-check-bold" : "mdi-close-thick"
})

const errorMessages = computed(() => {
  if (props.silent) return undefined
  if (success.value !== false) return undefined
  return props.errorExplanation
})

const choices = computed(() => {
  if (props.shuffle) return shuffle_array(props.options)
  return props.options
})

const longestChoiceLength = computed(() =>
  Math.max(...choices.value.map((s: any) => s.value.length)),
)

const gapWidth = computed(() => `${longestChoiceLength.value + 7}ch`)

const success = computed(() => {
  if ("right" in (answer.value || {})) {
    return answer.value.right
  }
  return undefined
})

// Methods
function shuffle_array(array: any[]) {
  const clonedArray = array.slice()
  let currentIndex = clonedArray.length,
    randomIndex

  while (currentIndex !== 0) {
    randomIndex = Math.floor(Math.random() * currentIndex)
    currentIndex--
    ;[clonedArray[currentIndex], clonedArray[randomIndex]] = [
      clonedArray[randomIndex],
      clonedArray[currentIndex],
    ]
  }

  return clonedArray
}

function onChange() {
  emit("update:answer", answer.value)

  if (props.silent) return
  if (typeof window === "undefined") return
  if (success.value === true) {
    // Uncomment and add confetti logic if needed
    // confettiShoot();
  }
}

// Watcher
watch(answer, (newValue) => {
  emit("input", newValue)
})
defineExpose({ answer, choices })
</script>

<template>
  <v-select
    ref="select"
    v-model="answer"
    :items="choices"
    class="gap-select"
    item-title="value"
    return-object
    :success="!props.silent && success === true"
    :error-messages="errorMessages"
    :error="!props.silent && success === false"
    :prepend-inner-icon="icon"
    @change="onChange"
    :readonly="props.readonly || (props.once && success !== undefined)"
    :style="`width: ${gapWidth}`"
    hide-details="auto"
    density="compact"
    variant="underlined"
  />
</template>

<style lang="scss">
.gap-select {
  position: relative;
  bottom: -0.6rem;
  padding: 0 0.2em;
  display: inline-block;
  .v-field {
    &--appended {
      padding-inline-end: initial;
    }
    &__append-inner {
      @media print {
        display: none;
      }
    }
  }
}

.print {
  @media print {
    display: initial;

    .choice {
      color: dimgrey;
      padding: 0.5ch;
      border: solid 1px silver;
      border-radius: 4px;
      margin: 0 1pt;
    }
  }
}
</style>
