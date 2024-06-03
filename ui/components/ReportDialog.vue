<script setup lang="ts">
const { $api } = useNuxtApp()
const { t } = useI18n()

const props = defineProps<{ exercise: string; nature: "mistake" | "misuse" }>()
const emit = defineEmits<{ input: [value: boolean] }>()

const toasts: Component | null = ref(null)

const description = ref("")
const disabled = ref(false)

const close = () => emit("input", false)

const submit = async () => {
  disabled.value = true

  const response = await $api("/v1/reports/", {
    method: "POST",
    body: {
      exercise: props.exercise,
      nature: props.nature,
      description: description.value,
    },
  })
  if (response?.status !== 201) throw response

  toasts.success(t(`exercise.submit_${props.nature}_confirm`))
  description.value = ""
  disabled.value = false
  close()
}
</script>

<template>
  <div>
    <v-dialog v-bind="$attrs" max-width="500px">
      <v-card>
        <v-form ref="flag_form" :disabled="disabled">
          <v-card-title><slot /></v-card-title>
          <v-card-text>
            <v-textarea
              @keypress.ctrl.enter="submit"
              v-model="description"
              rows="2"
              outlined
              :label="$t('exercise.explanation')"
            />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn @click="close">
              {{ $t("main.cancel") }}
            </v-btn>
            <v-btn
              type="submit"
              color="primary"
              @click.prevent="submit"
              :disabled="disabled"
            >
              {{ $t("main.submit") }}
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
    <Toast ref="toasts" />
  </div>
</template>
