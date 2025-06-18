<script setup lang="ts">
const { $apiFetch } = useNuxtApp()
const { t } = useI18n()
const toasts = useToasts()

type Props = { exercise: string; nature: UserReport["nature"]; title: string }
const { exercise, nature, title } = defineProps<Props>()
const model = defineModel({ type: Boolean })

const EXPLANATION_MIN_LENGTH = 8

const valid = ref(false)
const explanation = ref("")
const disabled = ref(false)
const rules = {
  length: (len: number) => (v: string) => (v || "").length >= len,
}
const close = () => {
  model.value = false
}

const submit = async () => {
  disabled.value = true

  const response = await $apiFetch<UserReport>("reports/", {
    method: "POST",
    body: { exercise, nature, description: explanation.value },
  })
  if (response?.status !== 201) throw response

  const label = {
    misuse: "exercise.submit_misuse_confirm",
    mistake: "exercise.submit_mistake_confirm",
  }[nature]
  toasts.success(t(label))
  explanation.value = ""
  disabled.value = false
  close()
}

defineExpose({ close })
</script>

<template>
  <div>
    <v-dialog v-model="model" max-width="500px">
      <v-card :title="title">
        <template #prepend>
          <slot name="prepend" />
        </template>
        <v-card-text>
          <v-form
            :id="`report-${nature}`"
            v-model="valid"
            tag="form"
            ref="flag_form"
            :disabled="disabled"
          >
            <v-textarea
              autofocus
              @keypress.ctrl.enter="submit"
              v-model="explanation"
              rows="2"
              color="primary"
              variant="outlined"
              counter
              :rules="[rules.length(EXPLANATION_MIN_LENGTH)]"
              :label="t('exercise.explanation')"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="close">
            {{ t("main.cancel") }}
          </v-btn>
          <v-btn
            type="submit"
            :form="`report-${nature}`"
            color="primary"
            @click.prevent="submit"
            :disabled="disabled || !valid"
          >
            {{ t("main.submit") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
