<script setup lang="ts">
const [route, localePath] = [useRoute(), useLocalePath()]
const { t, d } = useI18n()
const { $api } = useNuxtApp()
const auth = useAuthStore()
const unit_component = useUnitComponent()

const msgbox = ref()
const id = computed(() => route.params.id as string)
const exercise = shallowRef<Exercise | null>(null)
const is_submitting = ref(false)
const submitter_display_name = ref("")
const display_name_vmodel = ref("")
const submitted = ref(false)
const all_silent = ref(true)
const all_readonly = ref(false)
const units: Ref<{ [key: `unit-${string}`]: UnitComponent }> = ref({})
const append_unit = (el: unknown, unit: Unit) => {
  if (el) units.value[`unit-${unit._key}`] = el as UnitComponent
}

const embedded = computed(
  () =>
    typeof window !== "undefined" && window.location !== window.parent.location,
)
const current_username = computed(() => auth.user?.username || null)

const {
  data: exam,
  refresh,
  status,
} = await useLazyAsyncData("exams", () => $api<Exam>(`exams/${id.value}`), {
  server: false,
})

const should_exercise_be_shown = computed(() => {
  if (!exam.value) return false
  if (current_username.value == exam.value.created_by) return true
  if (!exam.value.accept_submission) return false
  if (submitter_display_name.value || auth.logged_in) return true
  return false
})

watch(exam, async () => {
  if (exam.value) {
    exam.value.created = new Date(exam.value.created)
    exercise.value = await $api<Exercise>(
      `exercises/${exam.value.exercise_lid}`,
    )
  }
})
const loading = computed(() => {
  if (!status?.value) return true
  return ["pending", "idle"].includes(status.value)
})

function login() {
  navigateTo(localePath({ name: "login" }))
}

// create the submission object to be sent to the server
const create_submission = () => {
  if (!exam.value || !exercise.value) return null

  const submission: NewSubmission = {
    created: new Date(),
    exercise_lid: exam.value.exercise_lid,
    exam_lid: exam.value.lid,
    exercise: { ...exercise.value },
  }
  submission.exercise.data.sheet = exercise.value.data.sheet.map(unit => ({
    ...unit,
    solved: units.value[`unit-${unit._key}`].get_solved(),
  }))

  if (current_username.value) {
    submission.created_by = current_username.value
  } else {
    submission.guest = submitter_display_name.value
  }

  return submission
}

async function submit() {
  is_submitting.value = true
  const submission = create_submission()
  const confirmed = await msgbox.value.confirm(t("exam.confirm"))
  console.info(confirmed)
  if (!submission || !confirmed) return false

  await $api("submissions/", { method: "post", body: submission })

  is_submitting.value = false
  submitted.value = true
}
</script>

<template>
  <v-container v-if="exam">
    <MsgBox ref="msgbox" />
    <v-alert
      icon="mdi-school"
      variant="tonal"
      color="primary"
      prominent
      class="mb-8 pa-sm-12 d-print-none"
    >
      <template v-if="exam.accept_submission">
        <div class="text-h6">
          {{ t("exam.is_exam") }}
        </div>
        <div>
          {{ t("exam.visible_by", { name: exam.created_by }) }}
        </div>
      </template>
      <template v-else>
        <div class="text-h6">
          {{ t("exam.now_new_submissions") }}
        </div>
      </template>
    </v-alert>

    <div
      v-if="
        !submitter_display_name && !auth.logged_in && exam.accept_submission
      "
    >
      <p v-if="!embedded" class="text-center text-body-2 mt-12 mb-7">
        {{ t("exam.please_log_in") }}
      </p>
      <v-row justify="center" class="mt-3">
        <v-col v-if="!embedded" cols="12" sm="4" md="2" align="center">
          <v-btn color="primary" block @click="login">
            {{ t("main.login") }}
          </v-btn>
        </v-col>
        <v-col v-if="!embedded" cols="12" sm="1" md="1" align="center">
          {{ t("exam.or") }}
        </v-col>
        <v-col cols="12" sm="6" md="4" align="center">
          <v-text-field
            variant="outlined"
            density="compact"
            v-model="display_name_vmodel"
            :label="t('exam.display_name')"
            placeholder="Choose a display name…"
            persistent-placeholder
          >
            <template #append>
              <v-btn
                small
                @click="submitter_display_name = display_name_vmodel"
              >
                {{ t("main.ok") }}
              </v-btn>
            </template>
          </v-text-field>
        </v-col>
      </v-row>
    </div>

    <div v-if="should_exercise_be_shown">
      <v-row>
        <v-col>
          <h1>{{ exam.name }}</h1>
        </v-col>
        <v-spacer class="d-print-none" />
        <v-col cols="auto" class="d-print-none">
          <LikeButton icon :item="exam" @liked="refresh" />
          <v-btn
            class="ms-2 text-primary"
            v-if="current_username == exam.created_by"
            text
            nuxt
            :to="localePath(`/exam_editor?exam=${id}`)"
          >
            <v-icon class="me-1">mdi-pencil</v-icon>
            {{ t("main.edit") }}
          </v-btn>
        </v-col>
      </v-row>

      <v-row dense class="text-caption mb-6 d-print-none">
        <v-col cols="auto">
          <v-icon small>mdi-account</v-icon>
          {{ exam.created_by || t("exercise.anonymous") }}
        </v-col>
        <v-col cols="auto">
          <v-icon small>mdi-clock</v-icon>
          {{ d(new Date(0), "dt") }}
        </v-col>
      </v-row>

      <v-sheet v-if="exam.description" class="mb-7">
        {{ exam.description }}
      </v-sheet>

      <section v-if="exercise">
        <h2>{{ exercise.name }}</h2>

        <v-sheet v-if="exercise.description" class="mt-3 mb-7">
          {{ exercise.description }}
        </v-sheet>

        <v-sheet
          v-for="(unit, i) in exercise.data?.sheet || []"
          :key="unit._key"
        >
          <div class="text-h4 my-4">
            {{ i + 1 }}. {{ unit.title }}
            <span v-if="unit.title === ''" class="font-italic">
              {{ t("sheet_editor.untitled_unit") }}
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
            :ref="(el: VueElement) => append_unit(el, unit)"
          />
        </v-sheet>
      </section>
      <v-progress-linear color="primary" indeterminate v-else />

      <v-alert
        variant="tonal"
        color="primary"
        class="mb-0 mt-10"
        v-if="submitted"
      >
        {{ t("exam.well_done") }}
      </v-alert>

      <v-btn
        @click="submit"
        color="primary"
        class="mt-9 d-print-none"
        :disabled="submitted || !exam.accept_submission"
        :loading="is_submitting"
      >
        {{ t("main.submit") }}
      </v-btn>
    </div>
  </v-container>
</template>
