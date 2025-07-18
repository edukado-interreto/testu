<script setup lang="ts">
import { onBeforeRouteLeave } from "vue-router"
import type { LocationQueryValue } from "vue-router"
import type MsgBox from "@/components/MsgBox.vue"

const localePath = useLocalePath()

// composables
const route = useRoute()
const { t } = useI18n()
const { $api } = useNuxtApp()
const auth = useAuthStore()
const cefr = useCefr()
const { langs_table, langs_available } = useLangsAvailable()

const confirm_exit = ref(false)

definePageMeta({ middleware: ["authenticated"] })

// refs
const msgbox = useTemplateRef<typeof MsgBox>("msgbox")
const sheet_editor = useTemplateRef("sheet_editor")
const exercise_title_field = useTemplateRef("exercise_title_field")
const confirm_leave_dialog = useTemplateRef("confirm_leave_dialog")

// data
const beforeunload_event = ref(undefined)
const overwrite_id = ref<LocationQueryValue | undefined>()
const tags_available = ref<string[]>([])
const dirty = ref(false)
const sheet = ref<Unit[]>([])
const infobox = ref(0)
const details = reactive<Details>({
  title: "",
  src_lang: "en",
  description: "",
  unlisted: true,
  tags: [],
  age_range: [0, 18],
  lang_learn: {
    lang: undefined,
    cefr_level_range: [cefr.MIN, cefr.MAX],
  },
})
const loaded_sheet: Ref<string | null> = ref(null)
const loaded_details: Ref<string | null> = ref(null)

useHead({
  title: overwrite_id.value === undefined ? "New exercise" : "Edit exercise",
})

// computed
const tags_available_localized = computed(() =>
  tags_available.value.map(tag => ({
    title: t(`tags.${tag}`),
    value: tag,
  })),
)
const current_cefr_label = computed((): string => {
  return cefr.display(details.lang_learn.cefr_level_range)
})
const age_range_label = computed(() => {
  return details.age_range.map(n => n + (n == 18 ? "+" : ""))
})

const fetch = async () => {
  const { results } = await $api<DRF<Tag>>("/tags/?limit=999")
  tags_available.value = results.map(tag => tag.name)

  if (route.query.new_from) {
    await load_exercise(route.query.new_from as string)
    details["title"] = `Copy of ${details.title}` // TODO i18n
  }
  if (route.query.edit) {
    await load_exercise(route.query.edit as string)
    overwrite_id.value = route.query.edit as string
  }
}

const load_exercise = async (id: string) => {
  const exercise = await $api<Exercise>(`/exercises/${id}/`)
  sheet.value = exercise.data.sheet || []
  details.title = exercise.name
  details.description = exercise.description
  details.tags = [...exercise.tags].map(tag => tag.name)
  details.src_lang = exercise.src_lang
  if (exercise.lang_learn) {
    details.lang_learn.lang = exercise.lang_learn_lang
    details.lang_learn.cefr_level_range = [
      exercise.lang_learn_cefr_level_min,
      exercise.lang_learn_cefr_level_max,
    ]
  }
  details.age_range = [exercise.age_min, exercise.age_max]
  details.unlisted = !exercise.searchable

  loaded_sheet.value = JSON.stringify(sheet)
  loaded_details.value = JSON.stringify(details)
  // TODO set tags, age range and the other fields
}

const save = async () => {
  if (msgbox.value === null) return
  if (sheet.value.length == 0) {
    await msgbox.value.alert("Please add at least one unit")
    return
  }
  if (!details.title) {
    infobox.value = 0 // $refs.exercise_title_field doesn’t exist if alrealy expanded
    await msgbox.value.alert("Please provide a title for the exercise")
    if (exercise_title_field.value === null) return
    exercise_title_field.value.focus()
    return
  }
  const payload: BuildExercise = {
    name: details.title,
    description: details.description,
    tags: [...details.tags] as Tag[],
    src_lang: details.src_lang,
    lang_learn: false,
    age_min: details.age_range[0] as AgeMin,
    age_max: details.age_range[1] as AgeMax,
    searchable: !details.unlisted,
    data: {
      sheet: sheet.value.map((e, i) => ({
        ...e,
        _parsed: sheet_editor.value.unit[i].parsed,
        // inject the parsed exercises into the sheet object that will
        // be stored in the database. The code is parsed by the grand-children
        // components so we use $refs to access it here.
      })),
    },
    created_by: auth.user?.username as string,
  }
  if (details.lang_learn.lang) {
    payload.lang_learn = true
    payload.lang_learn_lang = details.lang_learn.lang
    payload.lang_learn_cefr_level_min = details.lang_learn.cefr_level_range[0]
    payload.lang_learn_cefr_level_max = details.lang_learn.cefr_level_range[1]
  }
  await auth.check_token()

  // setup the api call: a PUT request if editing
  // an existing exercise, i.e. when overwrite_id
  // contains an exercise id, or a POST request if
  // creating a new one otherwise
  const api = {
    path: "/exercises/",
    method: "POST",
  }
  console.log("overwrite_id:", overwrite_id.value)
  if (overwrite_id.value !== undefined) {
    api.path = `/exercises/${overwrite_id.value}/`
    api.method = "PUT"
  }

  try {
    const data = await $api(api.path, {
      method: api.method,
      body: payload,
    })
    console.info(" ret:", data)
    dirty.value = false
    loaded_sheet.value = JSON.stringify(data.sheet)
    navigateTo(localePath(`/exercise/${data.lid}`))
  } catch (e) {
    console.error({ ...e })
    const resp = e.response
    if (resp.status == 400) {
      const details = Object.entries(resp.data)
        .map(([k, v]) => `${k}: ${v.join(" ")}`)
        .join("\n")
      // { name: ['Field missing.', 'Other error.'], field2: ['Field too long.'] }
      // => 'name: Field missing. Other error.\nfield2: Field too long.'
      await msgbox.value.alert(`Server error:\n${details}`)
    }
    if (resp.status > 400) {
      await msgbox.value.alert(`Server error (${resp.status})`)
    }
  }
}

// methods
const confirm_leave = async () => {
  if (!dirty.value) return true
  return await confirm_leave_dialog.value?.open({
    title: t("editor.confirm_leave.title"),
    message: t("editor.confirm_leave.message"),
  })
}

const before_window_unload = async (e: Event) => {
  const leave = await confirm_leave()
  if (leave) return
  e.preventDefault()
  e.returnValue = false // Event cancelled or prevented
}

onMounted(() => async () => {
  window.addEventListener("beforeunload", before_window_unload, {
    capture: true,
  })
})
onBeforeUnmount(() => {
  window.removeEventListener("beforeunload", before_window_unload)
})
onBeforeRouteLeave((to, from) => {
  return confirm_leave()
})

watch(sheet, sheet => {
  console.info("Sheet:", sheet)
  if (loaded_sheet.value) return
  dirty.value = loaded_sheet.value !== JSON.stringify(sheet)
})

watch(details, details => {
  if (loaded_details.value) return
  dirty.value = loaded_details.value !== JSON.stringify(details)
})
</script>

<template>
  <div style="position: relative">
    <MsgBox ref="msgbox"></MsgBox>

    <v-btn
      @click="$emit('save')"
      class="top-right-button d-flex mt-4 ms-auto me-8 px-5 z-4"
      variant="elevated"
      color="primary"
    >
      <v-icon class="mr-2">mdi-content-save</v-icon>
      {{ t("editor.save") }}
    </v-btn>

    <SheetEditor
      v-model:sheet="sheet"
      ref="sheet_editor"
      class="mt-8"
      @save="save"
    />

    <v-expansion-panels class="mt-9" v-model="infobox">
      <v-expansion-panel>
        <v-expansion-panel-title>
          <template #="{ expanded }">
            {{ $t("editor.details") }}
            <span class="ml-5 text-disabled" v-if="!expanded">
              <span v-if="details.title">{{ details.title }}</span>
              <span v-else class="font-italic">{{ $t("exercise.untitled") }}</span>
            </span>
          </template>
        </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-text-field
            :label="$t('editor.title')"
            v-model="details.title"
            maxlength="100"
            variant="outlined"
            ref="exercise_title_field"
          />
          <v-text-field
            :label="$t('editor.description')"
            v-model="details.description"
            variant="outlined"
          />
          <v-autocomplete
            :label="$t('editor.tags')"
            small-chips
            deletable-chips
            multiple
            v-model="details.tags"
            :items="tags_available_localized"
            variant="outlined"
          />
          <v-autocomplete
            :label="$t('exercise.language')"
            v-model="details.src_lang"
            :items="langs_available"
            variant="outlined"
            color="primary"
          />
          <v-autocomplete
            :label="$t('exercise.target_language')"
            v-model="details.lang_learn.lang"
            :items="langs_available"
            variant="outlined"
            color="primary"
            clearable
          >
            <template #selection="{ item, index }">
              <span>{{ item.title }}</span>
              <span class="text-medium-emphasis">
                &nbsp;{{ current_cefr_label }}
              </span>
            </template>
          </v-autocomplete>
          <v-range-slider
            v-model="details.lang_learn.cefr_level_range"
            :label="t('editor.cefr_levels_label')"
            :min="cefr.MIN"
            :max="cefr.MAX"
            :step="1"
            :ticks="cefr.LABELS"
            show-ticks="always"
            class="my-3"
            color="primary"
            dense
          />
          <v-range-slider
            v-model="details.age_range"
            :label="`${t('editor.age_range')} (${age_range_label.join(' – ')})`"
            min="0"
            max="18"
            :step="1"
            show-ticks="always"
            thumb-color="blue"
            thumb-label
            class="my-3"
            color="primary"
            dense
          />
          <v-checkbox
            :label="$t('editor.unlisted')"
            v-model="details.unlisted"
          ></v-checkbox>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <v-btn class="ma-7" color="primary" large variant="elevated" @click="save">
      <v-icon class="mr-2">mdi-content-save</v-icon>
      {{ $t("editor.save") }}
    </v-btn>

    <!-- {{ details }} -->

    <confirm-leave-dialog
      ref="confirm_leave_dialog"
      modelValue:message="chien"
    />
  </div>
</template>

<style scoped>
.pre-line {
  white-space: pre-line;
}
.code {
  font-family: monospace;
}
.top-right-button {
  position: sticky;
  top: calc(64px + 8px);
  z-index: 2;
}
</style>
