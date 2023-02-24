<template>
  <v-container>

    <v-chip small class="info mb-4">
      <template v-if="submission.exam_lid">
        <v-icon small dark class="me-2">mdi-school</v-icon> Exam review
      </template>
      <template v-else>
        Exercise review
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
      These are the exercise solutions you submitted on
      {{ submission_formatted_date }}.
      <ul class="my-3">
        <li v-if="submission.exam_lid">
          <NuxtLink :to="localePath(`/exam/${submission.exam_lid}`)">Go to the exam</NuxtLink>
        </li>
        <li v-else>
          <NuxtLink :to="localePath(`/exercise/${submission.exercise.lid}`)">Go to the exercise</NuxtLink>
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
  },
  computed: {
    submission_formatted_date() {
      return (new Date(this.submission.created)).toLocaleString('en-US')
    }
  }
}
</script>
<style scoped>
  li { line-height: 2em; }
</style>
