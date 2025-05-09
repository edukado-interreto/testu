<script setup lang="ts">
const { $api } = useNuxtApp()
const { t } = useI18n()
const localePath = useLocalePath()
const { langs_available } = useLangsAvailable()
const cefr = useCefr()

const loading = ref(false)
const page_length = ref(0)
const on_page_update = () => {}

const INITIAL_LIMIT = 20
const initial_limit = ref(20)
const no_exercise = ref(true)
const exercise_limit = computed(() =>
  initial_limit.value ? `?limit=${initial_limit.value}` : "",
)

const {
  data: exercises,
  status,
  refresh,
} = useLazyAsyncData(
  "exercises",
  () => $api<DRF<Exercise>>(`exercises/${exercise_limit.value}`),
  { server: false },
)
watch(
  exercises,
  async (incoming, previous) => {
    no_exercise.value = false
    if (exercises.value?.results.length == initial_limit.value) {
      initial_limit.value = 0
      await refresh()
    }
  },
  { once: true },
)

const { data: authors_used } = useLazyAsyncData(
  "authors_used",
  () => $api<DRF<Author>>("authors/?limit=999&ordering=username"),
  { server: false, transform: payload => payload.results },
)
const { data: tags_used } = useLazyAsyncData(
  "tags_used",
  () => $api<DRF<Tag>>("tags/?limit=999"),
  { server: false, transform: payload => payload.results },
)
const { data: source_langs_used } = useLazyAsyncData(
  "source_langs_used",
  () => $api<Lang[]>("languages/source/"),
  { server: false },
)
const { data: learn_langs_used } = useLazyAsyncData(
  "learn_langs_used",
  () => $api<Lang[]>("languages/learn/"),
  { server: false },
)

const iterator_key = ref("")
const source_langs_localized = computed(() => {
  if (!source_langs_used?.value) return []
  const codes = source_langs_used.value.map(l => l.code)
  return langs_available.filter(e => codes.includes(e.value))
})
const learn_langs_localized = computed(() => {
  if (!learn_langs_used?.value) return []
  const codes = learn_langs_used.value.map(l => l.code)
  return langs_available.filter(e => codes.includes(e.value))
})
const tags_used_localized = computed(() =>
  tags_used.value?.map(tag => ({
    value: tag.name,
    text: t(`tags.${tag.name}`),
    count: tag.count,
  })),
)
const search = ref<Search>({
  offset: 0,
  text: "",
  tags: [],
  created_by: "",
  src_langs: [],
  lang_learn: {
    langs: [],
    levels: [cefr.MIN, cefr.MAX],
  },
  sort: "-created",
})
const current_cefr_label = computed(() => {
  return cefr.display(search.value.lang_learn.levels)
})
const update_filtered_exercises = () => {
  return search.value
}
</script>

<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-chip-group
          multiple
          selected-class="text-primary"
          show-arrows
          v-model="search.tags"
          @change="update_filtered_exercises"
        >
          <v-chip
            v-for="tag in tags_used_localized"
            :key="tag.value"
            :value="tag.value"
          >
            {{ tag.text }}
          </v-chip>
        </v-chip-group>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="12" md="7">
        <v-text-field
          id="search-text"
          v-model="search.text"
          @keyup.enter="update_filtered_exercises"
          :label="$t('home.search_exercise')"
          append-inner-icon="mdi-magnify"
          density="comfortable"
          variant="underlined"
          hide-details
        />
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="3">
        <v-autocomplete
          id="exercise-language"
          :label="$t('exercise.language')"
          density="compact"
          variant="outlined"
          hide-details
          auto-select-first
          clearable
          multiple
          v-model="search.src_langs"
          :items="source_langs_localized"
          @change="update_filtered_exercises"
        >
          <template #selection="{ item, index }">
            <span>{{ item.text }}</span>
            <span v-if="index < search.src_langs.length - 1">,&nbsp;</span>
          </template>
        </v-autocomplete>
      </v-col>
      <v-col cols="12" md="3">
        <v-autocomplete
          id="exercise-target-language"
          :label="$t('exercise.target_language')"
          @change="update_filtered_exercises"
          prepend-inner-icon="mdi-chat"
          density="compact"
          variant="outlined"
          hide-details
          multiple
          v-model="search.lang_learn.langs"
          :items="learn_langs_localized"
          clearable
        >
          <template #prepend-item>
            <v-list-item @mousedown.prevent>
              <v-range-slider
                v-model="search.lang_learn.levels"
                @change="update_filtered_exercises"
                :min="cefr.MIN"
                :max="cefr.MAX"
                :step="1"
                :value="[cefr.MIN, cefr.MAX]"
                :thumb-size="16"
                :track-size="2"
                :ticks="cefr.LABELS"
                class="mx-4"
                show-ticks="always"
                color="primary"
              />
            </v-list-item>
          </template>
          <template #selection="{ item, index }" class="text-body-2">
            <span>{{ item.title }}</span>
            <span v-if="index < search.lang_learn.langs.length - 1">
              ,&nbsp;
            </span>
            <span v-else class="text-medium-emphasis">
              &nbsp;{{ current_cefr_label }}
            </span>
          </template>
        </v-autocomplete>
      </v-col>

      <v-col cols="12" md="2">
        <v-autocomplete
          id="exercise-author"
          :label="$t('exercise.author')"
          prepend-inner-icon="mdi-human-male-board"
          density="compact"
          variant="outlined"
          hide-details
          auto-select-first
          clearable
          hide-no-data
          item-title="username"
          item-value="username"
          v-model="search.created_by"
          :items="authors_used || []"
          @change="update_filtered_exercises"
        />
      </v-col>
      <v-spacer />
      <v-col cols="12" md="3">
        <v-select
          id="sorting"
          density="compact"
          variant="underlined"
          :label="$t('sort.sort')"
          prepend-inner-icon="mdi-sort"
          v-model="search.sort"
          :items="[
            { value: '-likes,-created', title: $t('sort.rated') },
            { value: '-created', title: $t('sort.recent') },
          ]"
          @change="update_filtered_exercises"
        />
      </v-col>
    </v-row>

    <v-btn
      class="mt-3"
      color="primary"
      size="large"
      variant="text"
      prepend-icon="mdi-plus"
      :to="localePath('/editor')"
    >
      {{ $t("home.create_exercise") }}
    </v-btn>

    <div v-if="status === 'error'">ERROR LOADING EXERCISES!</div>

    <v-skeleton-loader
      v-if="['pending', 'idle'].includes(status) && no_exercise"
      class="my-4"
      type="list-item-three-line@5"
    ></v-skeleton-loader>
    <div v-else>
      <v-data-iterator
        class="mt-5"
        :key="iterator_key"
        :items="exercises?.results"
        :items-per-page="page_length"
        :server-items-length="exercises?.count"
        :footer-props="{ 'disable-items-per-page': true }"
        @update:page="on_page_update"
        :loading="loading"
      >
        <template #default="{ items }">
          <ExerciseListItem
            v-for="item in items"
            :item="item.raw"
            :key="item.raw.id"
          />
        </template>
      </v-data-iterator>
    </div>
  </v-container>
</template>
