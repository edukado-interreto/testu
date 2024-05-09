<script setup lang="ts">
const { t } = useI18n()
const { $http } = useNuxtApp()
const { data: raw_exercises, pending, error } = await $http("/v1/exercises/")
const exercises = computed(() => raw_exercises.value?.results)
const { data: authors_used } = await $http(
  "/v1/authors/?limit=999&ordering=username",
)
const { data: tags_used } = await $http("/v1/tags/?limit=999") // /v1/tags/used/
const { data: source_langs_used } = await $http("/v1/languages/source/")
const { data: learn_langs_used } = await $http("/v1/languages/learn/")
const tags_used_localized = computed(
  () =>
    tags_used.value?.results.map((tag) => ({
      value: tag.name,
      text: t(`tags.${tag.name}`),
      count: tag.count,
    })),
)
let search = ref({
  offset: 0,
  text: "",
  tags: [],
  created_by: "",
  src_langs: [],
  lang_learn: {
    langs: [],
    levels: [1, 6],
  },
  sort: "-likes,-created",
})
const update_filtered_exercises = () => {}
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
          <template v-slot:selection="{ item, index }">
            <span>{{ item.text }}</span>
            <span v-if="index < search.src_langs.length - 1">,&nbsp;</span>
          </template>
        </v-autocomplete>
      </v-col>
      <v-col cols="12" md="3">
        <v-autocomplete
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
          <template v-slot:prepend-item>
            <v-list-item @mousedown.prevent>
              <v-range-slider
                density="compact"
                :min="cefr_lbound"
                :max="cefr_ubound"
                :value="[cefr_lbound, cefr_ubound]"
                :tick-labels="cefr_levels"
                v-model="search.lang_learn.levels"
                @change="update_filtered_exercises"
              />
            </v-list-item>
          </template>
          <template v-slot:selection="{ item, index }">
            <span>{{ item.text }}</span>
            <span v-if="index < search.lang_learn.langs.length - 1">
              ,&nbsp;
            </span>
            <span v-else class="grey--text">
              &nbsp;{{ current_cefr_label }}
            </span>
          </template>
        </v-autocomplete>
      </v-col>

      <v-col cols="12" md="2">
        <v-autocomplete
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
          :items="authors_used?.value?.results || []"
          @change="update_filtered_exercises"
        />
      </v-col>
      <v-spacer />
      <v-col>
        <v-select
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
  </v-container>
</template>
