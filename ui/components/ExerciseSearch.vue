<script setup lang="ts">
import {
  reactiveComputed,
  useDebounceFn,
  useThrottleFn,
  watchDebounced,
} from "@vueuse/core"

const { $api } = useNuxtApp()
const { t } = useI18n()
const localePath = useLocalePath()
const { langs_available } = useLangsAvailable()
const cefr = useCefr()

// Search
const TYPING_DEBOUNCE_MS = 300
const PAGE_SIZE = 20
const page = shallowRef(1)

const limit = ref(PAGE_SIZE)
const offset = computed(() => (page.value - 1) * PAGE_SIZE)
const name = ref("") // debounced by search_text
const tags = ref<Tag[]>([])
const created_by = ref("")
const src_langs = ref<Lang[]>([])
const learn_langs = ref<Lang[]>([])
const levels = ref<CefrRange>([cefr.MIN, cefr.MAX])
const sort = ref<Search["sort"]>("-created")

const debounce = useDebounceFn((value: string) => value, TYPING_DEBOUNCE_MS)

const search_text = computed({
  get: () => name.value,
  set(value) {
    debounce(value).then(value => {
      if (value !== undefined) name.value = value
    })
  },
})

watchDebounced(
  [name, tags, created_by, src_langs, learn_langs, levels, sort],
  () => {
    if (page.value !== 1) page.value = 1
  },
  { debounce: TYPING_DEBOUNCE_MS },
)

const params = computed(() => ({
  limit: limit.value, // API default limit is 300
  offset: or_undefined(offset),
  name: or_undefined(name),
  tags: or_undefined(tags),
  created_by: or_undefined(created_by),
  src_lang: or_undefined(src_langs),
  lang_learn_lang: or_undefined(learn_langs),
  cefr_level_min: non_empty(learn_langs) ? levels.value[0] : undefined,
  cefr_level_max: non_empty(learn_langs) ? levels.value[1] : undefined,
  ordering: sort.value,
}))

const {
  data: response,
  error,
  status,
  refresh,
} = await useAsyncData(
  "exercises",
  () => $api<DRF<Exercise>>("exercises/", { query: params.value }),
  { server: false, watch: [params] },
)
const loading = computed(() => {
  if (!status?.value) return true
  return ["pending", "idle"].includes(status.value)
})
const { data: authors_used } = useLazyAsyncData(
  "authors_used",
  () =>
    $api<DRF<Author>>("authors/", {
      query: { limit: 999, ordering: "username" },
    }),
  { server: false, transform: payload => payload.results },
)
const { data: tags_used } = useLazyAsyncData(
  "tags_used",
  () => $api<DRF<Tag>>("tags/", { query: { limit: 999 } }),
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

const total_pages = computed(() =>
  Math.ceil((response?.value?.count || 0) / limit.value),
)
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
</script>

<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-chip-group
          multiple
          selected-class="text-primary"
          show-arrows
          v-model="tags"
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
          v-model="search_text"
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
          v-model="src_langs"
          :items="source_langs_localized"
          :label="$t('exercise.language')"
          density="compact"
          variant="outlined"
          hide-details
          auto-select-first
          clearable
          multiple
        >
          <template #selection="{ item, index }">
            <span>{{ item?.title }}</span>
            <span v-if="index < src_langs.length - 1">,&nbsp;</span>
          </template>
        </v-autocomplete>
      </v-col>
      <v-col cols="12" md="3">
        <v-autocomplete
          id="exercise-target-language"
          v-model="learn_langs"
          :items="learn_langs_localized"
          :label="$t('exercise.target_language')"
          prepend-inner-icon="mdi-chat"
          density="compact"
          variant="outlined"
          hide-details
          multiple
          clearable
        >
          <template #prepend-item>
            <v-list-item @mousedown.prevent>
              <v-range-slider
                v-model="levels"
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
            <span v-if="index < learn_langs.length - 1">,&nbsp;</span>
            <span v-else class="text-medium-emphasis">
              &nbsp;{{ cefr.display(levels) }}
            </span>
          </template>
        </v-autocomplete>
      </v-col>

      <v-col cols="12" md="2">
        <v-autocomplete
          id="exercise-author"
          v-model="created_by"
          :items="authors_used || []"
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
        />
      </v-col>
      <v-spacer />
      <v-col cols="12" md="3">
        <v-select
          id="sorting"
          v-model="sort"
          :items="[
            { value: '-likes,-created', title: $t('sort.rated') },
            { value: '-created', title: $t('sort.recent') },
          ]"
          :label="$t('sort.sort')"
          density="compact"
          variant="underlined"
          prepend-inner-icon="mdi-sort"
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

    <div v-if="status === 'error'">
      <pre class="text-error">
      ERROR LOADING EXERCISES!

      {{ error }}
      </pre>
    </div>

    <v-data-iterator
      class="mt-5"
      :items="response?.results"
      :items-per-page="limit"
      :server-items-length="response?.count"
      :loading="loading"
    >
      <template #loader>
        <v-skeleton-loader class="my-4" type="list-item-three-line@5" />
      </template>
      <template #="{ items }">
        <ExerciseListItem
          v-for="item in items"
          :item="item.raw"
          :key="item.raw.id"
        />
      </template>
      <template #footer>
        <v-pagination v-model="page" :length="total_pages" class="my-4" />
      </template>
    </v-data-iterator>
  </v-container>
</template>
