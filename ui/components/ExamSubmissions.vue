<script setup lang="ts">
import SheetReview from "./SheetReview.vue"

const props = defineProps<{ submissions: any[] }>()
const submissionsIndex = ref(0)

const submissionsItems = computed(() =>
  [...props.submissions]
    .sort((a, b) => b.created - a.created)
    .map((e, i) => ({
      value: i,
      text:
        (e.created_by || `${e.guest} (guest)`) +
        " (" +
        new Date(e.created).toLocaleString("en-US") +
        ")",
      data: e,
    })),
)

const nthOfTotal = computed(() => {
  const of = "of"
  const len = submissionsItems.value.length
  if (len === 0) return `0 ${of} 0`
  return `${submissionsIndex.value + 1} ${of} ${len}`
})

const currentSubmission = computed(
  () => submissionsItems.value[submissionsIndex.value]?.data,
)
</script>

<template>
  <div>
    <v-row class="sticky mb-6">
      <v-col>
        <v-select
          outlined
          density="compact"
          :items="submissionsItems"
          v-model="submissionsIndex"
          hide-details
        />
      </v-col>
      <v-col class="d-flex align-center">
        <v-btn
          icon
          @click="submissionsIndex--"
          :disabled="submissionsIndex === 0"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
        <span class="mx-2">{{ nthOfTotal }}</span>
        <v-btn
          icon
          @click="submissionsIndex++"
          :disabled="submissionsIndex === submissionsItems.length - 1"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <SheetReview
      v-if="currentSubmission"
      :key="currentSubmission.pk"
      :submission="currentSubmission"
    />
  </div>
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
