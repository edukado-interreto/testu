<script setup lang="ts">
import { useI18n } from "vue-i18n"

const props = defineProps<{ value: string; label?: string }>()
const field = ref()
const { t } = useI18n()

function copyText() {
  const input = field.value?.$el?.querySelector("input")
  if (!input) return
  input.select()
  if (navigator.clipboard) {
    navigator.clipboard.writeText(props.value)
  } else {
    document.execCommand("copy")
  }
}
</script>

<template>
  <v-text-field
    ref="field"
    outlined
    density="compact"
    prepend-inner-icon="mdi-link-variant"
    append-inner-icon="mdi-content-copy"
    @click:append-inner="copyText"
    :model-value="props.value"
    :label="props.label"
    readonly
    :title="t('exam.copy')"
    hide-details
  />
</template>
