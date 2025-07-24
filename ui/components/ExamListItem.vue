<script setup lang="ts">
const { item: exam } = defineProps<{ item: Exam }>()
const localePath = useLocalePath()
</script>

<template>
  <v-card
    :to="localePath({ name: 'exam-editor', query: { exam: exam.lid } })"
    nuxt
    class="mb-5"
  >
    <v-card-item>
      <v-card-title class="d-flex text-h6 font-weight-bold">
        <span>
          {{ exam.name }}
        </span>
        <v-spacer />
        <v-chip v-if="exam.accept_submission" size="small" color="primary" variant="flat">
          {{ $t("exam.accepts_submissions") }}
        </v-chip>
      </v-card-title>
      <v-card-subtitle v-if="exam.description">
        {{ exam.description }}
      </v-card-subtitle>
    </v-card-item>
    <v-divider />
    <v-card-text>
      <v-icon size="small">mdi-account</v-icon>
      {{ exam.created_by || $t("exercise.anonymous") }}
      <span>·</span>
      <v-icon size="small">mdi-clock</v-icon>
      {{ $d(new Date(exam.created), "long") }}
    </v-card-text>
  </v-card>
</template>
