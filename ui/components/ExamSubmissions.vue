<script setup lang="ts">
const { submissions } = defineProps<{ submissions: Submission[] }>()
const current = shallowRef(0)

const display = (submission: Submission) => {
  return (
    (submission.created_by || `${submission.guest} (guest)`) +
    ` (${new Date(submission.created).toLocaleString()})`
  )
}
const submissions_items = computed(() =>
  submissions
    .sort((a, b) => (b.created < a.created ? 1 : -1))
    .map((subm, i) => ({ value: i, title: display(subm), data: subm })),
)

const nth_of_total = computed(() => {
  const len = submissions_items.value.length
  if (len === 0) return [0, 0]
  return [current.value + 1, len]
})

const current_submission = computed(
  () => submissions_items.value[current.value]?.data,
)
</script>

<template>
  <v-row class="sticky mb-6">
    <v-col>
      <v-select
        variant="outlined"
        density="compact"
        :items="submissions_items"
        v-model="current"
        hide-details
      />
    </v-col>
    <v-col class="d-flex align-center">
      <v-btn
        icon="mdi-chevron-left"
        variant="text"
        @click="current--"
        :disabled="current === 0"
      />
      <span class="mx-2">
        {{
          $t("main.of", { current: nth_of_total[0], total: nth_of_total[1] })
        }}
      </span>
      <v-btn
        icon="mdi-chevron-right"
        variant="text"
        @click="current++"
        :disabled="current === submissions_items.length - 1"
      />
    </v-col>
  </v-row>
  <SheetReview
    v-if="current_submission"
    :key="current_submission.pk"
    :submission="current_submission"
  />
</template>

<style scoped>
.sticky {
  position: sticky;
  top: 56px;
  z-index: 1;
  background: white;
  box-shadow: 0 12px 12px white;
}
</style>
