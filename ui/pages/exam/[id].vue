<script setup lang="ts">
import { useRoute, useRouter } from "vue-router"
import { useI18n } from "vue-i18n"
import { useNuxtApp } from "#app"
import { useApiFetch } from "~/composables/useApiFetch"
import { useAuthStore } from "~/stores/useAuth"

const route = useRoute()
const router = useRouter()
const { t, d } = useI18n()
const { $localePath } = useNuxtApp()
const auth = useAuthStore()

const msgbox = ref()
const id = computed(() => route.params.id as string)
const exam = reactive<any>({})
const exercise = reactive<any>({})
const is_submitting = ref(false)
const submitter_display_name = ref("")
const display_name_vmodel = ref("")
const submitted = ref(false)
const all_silent = ref(true)
const all_readonly = ref(false)

const embedded = computed(
  () =>
    typeof window !== "undefined" && window.location !== window.parent.location,
)
const logged_in = computed(() => auth.user && auth.user.username !== undefined)
const current_username = computed(() => auth.user?.username || null)

const should_exercise_be_shown = computed(() => {
  if (current_username.value == exam.created_by) return true
  if (!exam.accept_submission) return false
  if (submitter_display_name.value || logged_in.value) return true
  return false
})

function localePath(path: string) {
  return $localePath ? $localePath(path) : path
}

function unit_component(type: string) {
  switch (type) {
    case "multiple_choice":
      return UnitMultipleChoice
    case "pairing":
      return UnitPairing
    case "open_answer":
      return UnitOpenAnswer
    default:
      return UnitDefault
  }
}

async function fetchExamAndExercise() {
  const { data: examData } = await useApiFetch<any>(`/v1/exams/${id.value}`)
  if (examData.value) {
    Object.assign(exam, examData.value)
    exam.created = new Date(exam.created)
    const { data: exerciseData } = await useApiFetch<any>(
      `/v1/exercises/${exam.exercise_lid}`,
    )
    if (exerciseData.value) {
      Object.assign(exercise, exerciseData.value)
    }
  }
}

onMounted(fetchExamAndExercise)

function login() {
  router.push(localePath("/login"))
}

function liked() {
  // Optionally handle like event
}

async function submit() {
  is_submitting.value = true
  // Implement submission logic here
  // ...
  is_submitting.value = false
  submitted.value = true
}
</script>

<template>
  <v-container>
    <MsgBox ref="msgbox" />
    <v-alert
      icon="mdi-school"
      text
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

    <div v-if="!submitter_display_name && !logged_in && exam.accept_submission">
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
            outlined
            density="compact"
            v-model="display_name_vmodel"
            :label="t('exam.display_name')"
            placeholder="Choose a display name…"
            persistent-placeholder
          >
            <template #append-outer>
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
          <LikeButton icon :item="exam" @liked="liked" />
          <v-btn
            class="primary--text"
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
          {{ d(new Date(exam.created), "dt") }}
        </v-col>
      </v-row>

      <v-sheet v-if="exam.description" class="mb-7">
        {{ exam.description }}
      </v-sheet>

      <h2>{{ exercise.name }}</h2>

      <v-sheet v-if="exercise.description" class="mt-3 mb-7">
        {{ exercise.description }}
      </v-sheet>

      <v-sheet v-for="(unit, i) in exercise.data?.sheet || []" :key="unit._key">
        <div class="headline my-4">
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
          :ref="`unit-${unit._key}`"
        />
      </v-sheet>

      <v-alert text color="primary" class="mb-0 mt-10" v-if="submitted">
        {{ t("exam.well_done") }}
      </v-alert>

      <v-btn
        @click="submit"
        class="mt-9 primary d-print-none"
        :disabled="submitted || !exam.accept_submission"
        :loading="is_submitting"
      >
        {{ t("main.submit") }}
      </v-btn>
    </div>
  </v-container>
</template>
