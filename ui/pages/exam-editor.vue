<script setup lang="ts">
import { useRoute, useRouter } from "vue-router"
import { useI18n } from "vue-i18n"
const { $api } = useNuxtApp()

const localePath = useLocalePath()
const route = useRoute()
const router = useRouter()
const { t } = useI18n()

const msgbox = ref()
const is_saving = ref(false)
const is_toggling_accept_submission = ref(false)
const infobox = ref<number | undefined>(0)
const exam = reactive<any>({ accept_submission: true })
const submissions = ref<any[]>([])

const breadcrumbs = computed(() => [
  {
    title: t("main.my_teaching"),
    href: localePath({ name: "teach" }),
  },
  {
    title: t("teach.exams"),
    href: localePath({ name: "teach", hash: "#exams" }),
  },
  { title: exam.name || t("exam.untitled"), disabled: true },
])

const sharable_link = computed(() => {
  if (!exam.lid) return ""
  return new URL(
    localePath({ name: "exam-id", params: { id: exam.lid } }),
    window.location.origin,
  ).href
})

async function fetch_exam_submissions(id: string) {
  const { data, error } = await useApiFetch<Submission[]>(
    `exams/${id}/submissions/`,
  )
  if (data.value) {
    submissions.value = data.value.map(s => ({
      ...s,
      created: new Date(s.created),
    }))
  }
}

async function fetchExam() {
  const exam_id = route.query.exam as string | undefined
  const new_from = route.query.new_from as string | undefined
  if (new_from) {
    exam.exercise_lid = new_from
  }
  if (exam_id) {
    infobox.value = undefined
    const { data } = await useApiFetch<Exam>(`exams/${exam_id}/`)
    if (data.value) {
      Object.assign(exam, data.value)
      exam.created = new Date(exam.created)
      await fetch_exam_submissions(exam_id)
    }
  }
}

onMounted(fetchExam)
watch(() => route.query.exam, fetchExam)

async function delete_exam() {
  if (!exam.lid) return
  if (!(await msgbox.value?.confirm(t("exam.delete_confirm")))) return
  try {
    await useApiFetch(`/v1/exams/${exam.lid}/`, { method: "DELETE" })
  } catch (e: any) {
    await msgbox.value?.alert(t("exam.delete_error"))
    return
  }
  await navigateTo(localePath({ name: "teach", hash: "#exams" }))
}

async function toggle_accept_submission(value: boolean) {
  if (!exam.lid) return
  const confirm_text = value
    ? t("exam.accept_confirm")
    : t("exam.reject_confirm")
  if (!(await msgbox.value?.confirm(confirm_text))) {
    exam.accept_submission = !value
    return
  }
  is_toggling_accept_submission.value = true
  try {
    await useApiFetch(`/v1/exams/${exam.lid}/`, {
      method: "PATCH",
      body: { accept_submission: value },
    })
  } catch (e: any) {
    exam.accept_submission = !value
    await msgbox.value?.alert(t("exam.toggle_error"))
  } finally {
    is_toggling_accept_submission.value = false
  }
}

async function save() {
  if (!exam.name) {
    await msgbox.value?.alert(t("exam.name_required"))
    return
  }
  is_saving.value = true
  const path = exam.lid ? `exams/${exam.lid}/` : "exams/"
  const method = exam.lid ? "PUT" : "POST"

  try {
    const created_exam = await $api<Exam>(path, { method, body: { ...exam } })
    if (created_exam) {
      if (!exam.lid) {
        router.replace({ query: { exam: created_exam.lid } })
        infobox.value = undefined
      }
      Object.assign(exam, created_exam)
      exam.created = new Date(exam.created)
      window.scrollTo({ top: 0, behavior: "smooth" })
    }
  } catch (e: any) {
    if (e?.response?.status === 400 && e.response.data) {
      const details = Object.entries(e.response.data)
        .map(([k, v]) => `${k}: ${(v as string[]).join(" ")}`)
        .join("\n")
      await msgbox.value?.alert(`${t("exam.server_error")}\n${details}`)
    } else {
      await msgbox.value?.alert(
        `${t("exam.server_error")} (${e?.response?.status})`,
      )
    }
  } finally {
    is_saving.value = false
  }
}
</script>

<template>
  <v-container>
    <MsgBox ref="msgbox" />
    <v-breadcrumbs class="pt-0 pl-0" :items="breadcrumbs">
      <template #divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>
    <v-row>
      <v-col>
        <h1 :class="{ 'font-italic': !exam.name }">
          {{ exam.name || t("exam.untitled") }}
        </h1>
      </v-col>
      <v-spacer />
      <v-col cols="auto">
        <v-menu>
          <template #activator="{ props }">
            <v-btn icon variant="text" v-bind="props" :disabled="!exam.lid">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item color="error" @click="delete_exam">
              <template #prepend>
                <v-avatar>
                  <v-icon class="text-error">mdi-delete</v-icon>
                </v-avatar>
              </template>
              <v-list-item-title class="text-error font-weight-bold">
                {{ $t("exam.delete") }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-col>
    </v-row>
    <p class="text-caption" v-if="exam.created">
      {{ $t("exam.created", { date: $d(exam.created, "short") }) }}
    </p>
    <v-row no-gutters class="mt-4">
      <v-col cols="12" sm="6">
        <v-btn
          prepend-icon="mdi-file-outline"
          size="large"
          color="primary"
          variant="text"
          :to="
            localePath({
              name: 'exercise-id',
              params: { id: exam.exercise_lid },
            })
          "
        >
          {{ $t("exam.goto_exercise") }}
        </v-btn>
      </v-col>
      <v-col v-if="exam.lid">
        <CopyTextField v-model="sharable_link" :label="t('exam.link')" />
      </v-col>
      <v-col v-if="exam.lid" class="flex-shrink-1 flex-grow-0">
        <v-btn
          :disabled="!exam.lid"
          :to="localePath({ name: 'exam-id', params: { id: exam.lid } })"
          class="text-primary"
          nuxt
          variant="text"
        >
          {{ t("exam.view") }}
        </v-btn>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="auto">
        <v-switch
          :disabled="!exam.lid"
          :label="t('exam.accept_submissions')"
          v-model="exam.accept_submission"
          @change="toggle_accept_submission"
          :loading="is_toggling_accept_submission"
          color="primary"
        />
      </v-col>
      <v-spacer />
    </v-row>
    <div v-if="submissions.length > 0" class="mt-5 mb-15">
      <ExamSubmissions :submissions="submissions" />
    </div>
    <template v-else>
      <div
        v-if="exam.lid"
        class="pa-9 text-h5 text-grey bg-grey-lighten-4 rounded mb-10"
      >
        <v-icon large class="text-grey me-1 pb-1">mdi-inbox</v-icon>
        {{ $t("exam.no_submissions") }}
      </div>
    </template>
    <v-expansion-panels class="mt-9" v-model="infobox">
      <v-expansion-panel>
        <v-expansion-panel-title>
          <template #="{ expanded }">
            {{ t("exam.details") }}
            <span class="ml-5 text-disabled" v-if="!expanded">
              <span v-if="exam.name">{{ exam.name }}</span>
              <span v-else class="font-italic">{{ t("exam.untitled") }}</span>
            </span>
          </template>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-text-field
            :label="t('exam.name')"
            v-model="exam.name"
            maxlength="100"
            variant="underlined"
          />
          <v-textarea
            :label="t('exam.description')"
            v-model="exam.description"
            auto-grow
            variant="underlined"
            rows="1"
          />
          <v-btn
            class="my-3 text-primary"
            large
            :loading="is_saving"
            text
            @click="save"
          >
            <v-icon class="mr-2">mdi-content-save</v-icon>
            {{ t("editor.save") }}
          </v-btn>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>

<style scoped>
a {
  text-decoration: none;
}
</style>
