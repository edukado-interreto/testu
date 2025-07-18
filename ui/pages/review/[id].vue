<script setup lang="ts">
const { $api } = useNuxtApp()
const localePath = useLocalePath()

const id = computed(() => useRoute().params.id as string)
const url = computed(() => `submissions/${id.value}/`)
const { data: submission } = await useLazyAsyncData(
  url.value,
  () => $api<Submission>(url.value),
  { server: false },
)
</script>

<template>
  <v-container v-if="submission">
    <v-chip size="small" color="info" variant="flat" class="mb-4">
      <template v-if="submission.exam_lid">
        <v-icon size="small" dark class="me-2">mdi-school</v-icon>
        {{ $t("review.exam") }}
      </template>
      <template v-else>
        {{ $t("review.exercise") }}
      </template>
    </v-chip>

    <h1>{{ submission.exercise.name }}</h1>

    <v-sheet v-if="submission.exercise.description" class="mt-5 mb-7">
      {{ submission.exercise.description }}
    </v-sheet>

    <SheetReview :submission="submission" :silent="!!submission.exam_lid" />

    <v-alert type="info" variant="text" class="mt-12">
      {{
        $t("review.submitted_on", {
          date: $d(new Date(submission.created), "long"),
        })
      }}
      <ul class="my-3">
        <li v-if="submission.exam_lid">
          <NuxtLink :to="localePath(`/exam/${submission.exam_lid}`)">
            {{ $t("review.go_exam") }}
          </NuxtLink>
        </li>
        <li v-else>
          <NuxtLink :to="localePath(`/exercise/${submission.exercise.lid}`)">
            {{ $t("review.go_exercise") }}
          </NuxtLink>
        </li>
      </ul>
    </v-alert>
  </v-container>
</template>

<style scoped>
li {
  line-height: 2em;
}
</style>
