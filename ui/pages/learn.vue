<script setup lang="ts">
import { useRouteQuery } from "@vueuse/router"

const { t, locale } = useI18n()
const localePath = useLocalePath()

useHead({ title: t("main.my_learning") })

definePageMeta({ middleware: ["authenticated"] })

const { $api } = useNuxtApp()

const PAGE_LENGTH = 30
const offset = useRouteQuery("offset", "0", { transform: Number })

const table = computed(() => {
  const items = submissions.value?.results.map(s => ({
    pk: s.pk,
    created: new Date(s.created),
    is_exam: !!s.exam_lid,
    exercise_name: s.exercise.name,
  }))
  const headers = [
    {
      text: t("learn.exercise"),
      value: "exercise_name",
      sortable: false,
    },
    { text: "", value: "is_exam", sortable: false },
    {
      text: t("learn.date"),
      value: "created",
      sortable: false,
    },
    { text: "", value: "actions", sortable: false },
  ]
  return { headers, items }
})

const {
  data: submissions,
  pending,
  refresh,
} = await useAsyncData<DRF<Submission>>(
  "submissions",
  () => $api("submissions/", { params: { offset: offset.value } }),
  { watch: [offset] },
)

const stats = computed(() => {
  const days: { [key: string]: number } = {}

  submissions.value?.results.forEach(s => {
    const dateWithoutTime = new Date(s.created).setHours(0, 0, 0, 0) // as int
    days[dateWithoutTime] = days[dateWithoutTime] + 1 || 1
  })
  // days = {1676588400000: 2, 1677106800000: 9}

  const days_array = Object.entries(days)
    .sort(
      (a, b) => a[0] - b[0], // oldest to newest
    )
    .map(a => ({
      day: new Date(a[0] * 1).toLocaleString(locale.value, {
        dateStyle: "short",
      }),
      value: a[1],
    }))
  // days_array = [
  //   { "day": "2/17/23", "value": 2 },
  //   { "day": "2/23/23", "value": 9 }
  // ]

  const empties = [...Array(7 - days_array.length)].map(a => ({
    day: "·",
    value: 0,
  }))
  days_array.unshift(...empties)
  // pad the array to 7 elements, prepending empty values if needed
  // days_array = [
  //   { "day": "·", "value": 0 },
  //   { "day": "·", "value": 0 },
  //   { "day": "·", "value": 0 },
  //   { "day": "·", "value": 0 },
  //   { "day": "·", "value": 0 },
  //   { "day": "2/17/23", "value": 2 },
  //   { "day": "2/23/23", "value": 9 }
  // ]

  return {
    labels: days_array.map(a => a.day),
    values: days_array.map(a => a.value),
  }
  // {
  //   "labels": [ "2/17/23", "2/23/23" ],
  //   "values": [ 2, 9 ]
  // }
})
const on_page_update = (page: number) => {
  offset.value = (page - 1) * PAGE_LENGTH
  refresh()
}
const x: SparklineItem = ""
</script>

<template>
  <v-container>
    <v-card max-width="600" elevation="1" class="mb-4">
      <v-card-text class="d-block d-sm-flex align-baseline">
        <div class="text-h6 font-weight-light text-grey text--darken-3">
          {{ $t("learn.recent") }}
        </div>
        <div class="subheading ms-0 ms-sm-4 text-grey">
          {{ $t("learn.submitted") }}
        </div>
      </v-card-text>
      <v-sheet>
        <v-sparkline
          :labels="stats.labels"
          :model-value="stats.values"
          :gradient="['red', 'orange', 'yellow']"
          stroke-linecap="round"
          :smooth="true"
          line-width="2"
          padding="16"
          auto-draw
          type="trend"
          height="60"
        />
      </v-sheet>
    </v-card>

    <v-data-table
      :items="table.items"
      :headers="table.headers"
      :items-per-page="PAGE_LENGTH"
      :server-items-length="submissions?.count"
      :footer-props="{ 'disable-items-per-page': true }"
      @update:page="on_page_update"
      :loading="pending"
    >
      <template v-slot:item.is_exam="{ item }">
        <v-chip color="primary" variant="flat" v-if="item.is_exam">
          {{ $t("learn.exam") }}
        </v-chip>
      </template>
      <template v-slot:item.created="{ item }">
        {{ $d(new Date(item.created), "long") }}
      </template>
      <template v-slot:item.actions="{ item }">
        <v-btn
          size="small"
          variant="tonal"
          nuxt
          :to="localePath({ name: 'review-id', params: { id: item.pk } })"
        >
          {{ $t("learn.review") }}
        </v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>
