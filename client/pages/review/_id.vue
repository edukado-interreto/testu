<template>
  <v-container>

    <v-chip small class="info mb-4">
      <template v-if="submission.exam_lid">
        <v-icon small dark class="me-2">mdi-school</v-icon>
        {{ $t('review.exam') }}
      </template>
      <template v-else>
        {{ $t('review.exercise') }}
      </template>
    </v-chip>

    <h1>{{ submission.exercise.name }}</h1>

    <v-sheet v-if="submission.exercise.description" class="mt-5 mb-7">
      {{ submission.exercise.description }}
    </v-sheet>

    <SheetReview
      :submission="submission"
      :silent="!!submission.exam_lid"
    ></SheetReview>

    <v-alert type="info" text class="mt-12">
      {{ $t('review.submitted_on', { date: $d(new Date(submission.created), 'dt') }) }}
      <ul class="my-3">
        <li v-if="submission.exam_lid">
          <NuxtLink :to="localePath(`/exam/${submission.exam_lid}`)">{{ $t('review.go_exam') }}</NuxtLink>
        </li>
        <li v-else>
          <NuxtLink :to="localePath(`/exercise/${submission.exercise.lid}`)">{{ $t('review.go_exercise') }}</NuxtLink>
        </li>
      </ul>
    </v-alert>

  </v-container>
</template>
<script>
export default {
  data: () => ({
  }),
  async asyncData({ $auth, params, route }) {
    const id = (process.server) ? route.params.id : params.id;
    const submission = (
      await $auth.axios.get(`/v1/submissions/${id}`)
    ).data
    return {
      id,
      submission
    }
  }
}
</script>
<style scoped>
  li { line-height: 2em; }
</style>
