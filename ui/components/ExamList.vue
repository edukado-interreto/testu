<script setup lang="ts">
const { $api } = useNuxtApp()

const auth = useAuthStore()
const toasts = useToasts()
const page = shallowRef(1)
const page_length = ref(50)
const offset = computed(() => (page.value - 1) * page_length.value)

const user = computed(() => auth.user)

const params = computed(() => ({
  limit: page_length.value,
  offset: offset.value,
  created_by: auth.user?.username,
}))

const {
  data: exams,
  error,
  status,
  refresh,
} = await useAsyncData(
  "exams",
  () => $api<DRF<Exercise>>("exams/", { query: params.value }),
  { server: false, watch: [params] },
)
const loading = computed(() => {
  if (!status?.value) return true
  return ["pending", "idle"].includes(status.value)
})
</script>

<template>
  <v-data-iterator
    v-if="exams"
    class="mt-5"
    :items="exams.results"
    :items-per-page="page_length"
    :server-items-length="exams.count"
    :footer-props="{ 'disable-items-per-page': true }"
    :loading="loading"
  >
    <template #default="{ items }">
      <ExamListItem v-for="item in items" :item="item.raw" :key="item.lid" />
    </template>
  </v-data-iterator>
</template>
