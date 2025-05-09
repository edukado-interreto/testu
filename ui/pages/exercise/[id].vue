<script setup lang="ts">
import type MsgBox from "~/components/MsgBox.vue"

const { $api } = useNuxtApp()
const { t } = useI18n()
const localePath = useLocalePath()
const route = useRoute()
const router = useRouter()

const unit_component = useUnitComponent()

const auth = useAuthStore()

const id = computed(() => route.params.id as string)
const url = computed(() => `exercises/${id.value}/`)
const { status, data: exercise, refresh } = useApiFetch<Exercise>(url.value)

const msgbox: Ref<InstanceType<typeof MsgBox> | null> = ref(null)
const units: Ref<{ [key: `unit-${string}`]: UnitComponent }> = ref({})
const append_unit = (el: UnitComponent, unit: Unit) => {
  units.value[`unit-${unit._key}`] = el
}
const all_readonly = ref(false)
const all_silent = ref(true)
const mistake_dialog = ref(false)
const misuse_dialog = ref(false)
const submitted = ref(false)

const user_logged_in = computed(() => {
  return !!auth.user
})
const user_is_creator = computed(() => {
  if (!auth.user || exercise === null) return false
  return exercise.value?.created_by === auth.user.username
})

const create_exam = async () => {
  if (!exercise.value) return
  if (
    !user_is_creator.value &&
    !(await msgbox.value?.confirm(t("exercise.create_exam_confirm"), ""))
  )
    return
  router.push(localePath(`/exam_editor?new_from=${exercise.value.lid}`))
}
const remove = async () => {
  if (!(await msgbox.value?.confirm(t("exercise.delete_confirm"), ""))) return

  try {
    await $api(`exercises/${id}`, { method: "DELETE" })
    router.push(localePath("/"))
  } catch (e: Error | unknown) {
    console.error({ ...e })
    await msgbox.value?.alert(`Error ${e.response.status}`, "")
  }
}

const create_submission = (): NewSubmission => {
  if (!exercise.value) throw Error("Exercise shouldn’t be null or undefined")

  // Create the submission object to be sent to the server
  const submission: NewSubmission = {
    guest: auth.user?.username ? undefined : "x", // TODO: display name
    created: new Date(),
    exercise_lid: id.value,
    exam_lid: null,
    exercise: { ...exercise.value },
  }

  submission.exercise.data.sheet = exercise.value.data.sheet.map((unit) => ({
    ...unit,
    solved: units.value[`unit-${unit._key}`]?.get_solved(),
  }))

  return submission
}
const liked = async () => await refresh()

const submit = async () => {
  // show the results of the quiz

  submitted.value = true
  window.scrollTo({ top: 0, behavior: "smooth" })

  all_silent.value = false
  all_readonly.value = true

  if (!user_logged_in) return

  const submission = create_submission()
  try {
    await $api("submissions/", {
      method: "POST",
      body: JSON.stringify(submission),
    })
  } catch (e: Error | unknown) {
    console.error({ ...e })
    await msgbox.value?.alert(t("exercise.error"), JSON.stringify(e))
  }
}

const window_print = () => window.print()

useHead({ title: exercise.value?.name })
</script>

<template>
  <v-container v-if="status === 'pending'" class="d-flex">
    <v-spacer />
    <v-progress-circular indeterminate color="primary" size="70" width="3" />
    <v-spacer />
  </v-container>
  <v-container v-if="exercise">
    <MsgBox ref="msgbox" />
    <v-row>
      <v-col>
        <h1>{{ exercise?.name }}</h1>
      </v-col>
      <v-col cols="auto" class="d-print-none">
        <v-btn
          @click="window_print"
          variant="text"
          prepend-icon="mdi-printer"
          color="primary"
        >
          {{ $t("exercise.pdf") }}
        </v-btn>
        <LikeButton icon :item="exercise" @liked="liked" />
        <v-menu offset-y>
          <template v-slot:activator="{ props }">
            <v-btn
              icon="mdi-dots-vertical"
              class="d-print-none"
              variant="text"
              :disabled="!user_logged_in"
              v-bind="props"
            />
          </template>
          <v-list v-if="user_logged_in">
            <v-list-item
              nuxt
              @click="create_exam"
              prepend-icon="mdi-school"
              :title="t('exercise.create_exam')"
            />
            <v-list-item
              :to="localePath(`/editor?new_from=${exercise.lid}`)"
              :title="t('exercise.create_copy')"
              prepend-icon="mdi-content-copy"
            />
            <v-list-item
              v-if="user_is_creator"
              :to="localePath(`/editor?edit=${exercise.lid}`)"
              :title="t('exercise.edit')"
              prepend-icon="mdi-pencil"
            />
            <v-list-item
              v-if="user_is_creator"
              class="error--text font-weight-'old"
              @click="remove"
              :title="t('exercise.delete')"
              prepend-icon="mdi-delete"
            />
            <v-list-item
              v-if="!user_is_creator"
              @click="() => (mistake_dialog = !mistake_dialog)"
              :title="t('exercise.mistake')"
              prepend-icon="mdi-format-strikethrough-variant"
            />
            <v-list-item
              v-if="!user_is_creator"
              @click="() => (misuse_dialog = !misuse_dialog)"
              :title="t('exercise.misuse')"
              prepend-icon="mdi-alert-box"
            />
          </v-list>
        </v-menu>
      </v-col>
    </v-row>

    <ExerciseFooterAttributes :exercise="exercise" class="mb-6" />
    <v-sheet v-if="exercise.description" class="mb-7">
      {{ exercise.description }}
    </v-sheet>

    <v-sheet v-for="(unit, i) in exercise.data.sheet" :key="unit._key">
      <div class="headline my-4">
        <span v-if="exercise.data.sheet.length > 1">{{ i + 1 }}.</span>
        <span class="font-weight-medium">{{ unit.title }}</span>
        <span v-if="unit.title === ''" class="font-italic">
          {{ $t("sheet_editor.untitled_unit") }}
        </span>
      </div>
      <div v-if="unit.description" class="body-2 mb-4 pre-line">
        <RichContent :text="unit.description" />
      </div>
      <component
        :is="unit_component(unit.type)"
        :code="unit.code"
        :shuffle="unit.shuffle"
        :ignore_case="unit.ignore_case"
        :silent="all_silent"
        :readonly="all_readonly"
        :ref="(el: UnitComponent) => append_unit(el, unit)"
      />
    </v-sheet>

    <v-btn
      @click="submit"
      type="submit"
      class="mt-9 d-print-none"
      :color="submitted ? 'grey' : 'primary'"
      :disabled="submitted"
      v-text="t('exercise.check')"
    />

    <ReportDialog
      nature="mistake"
      :exercise="exercise.lid"
      v-model="mistake_dialog"
    >
      <v-icon class="pe-3" color="warning">
        mdi-format-strikethrough-variant
      </v-icon>
      {{
        $t("exercise.report_mistake_to_creator", {
          username: exercise.created_by,
        })
      }}
    </ReportDialog>

    <ReportDialog
      nature="misuse"
      :exercise="exercise.lid"
      v-model="misuse_dialog"
    >
      <v-icon class="pe-3" color="error">mdi-alert-box</v-icon>
      {{ $t("exercise.report_misuse_to_administrators") }}
    </ReportDialog>
  </v-container>
</template>

<style scoped>
.pre-line {
  white-space: pre-line;
}
</style>
