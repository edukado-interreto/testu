<script setup lang="ts">
import { useAuthStore } from "~/stores/useAuth"
import { useApiFetch } from "~/composables/useApiFetch"
import { useToasts } from "~/stores/useToasts"
import ExamListItem from "./ExamListItem.vue"

const auth = useAuthStore()
const toasts = useToasts()
const page_length = 15
const page = ref(1)
const exams = ref({ results: [], count: 0 })
const loading = ref(false)

const user = computed(() => auth.user)

async function getExams(params: Record<string, any> = {}) {
  if (!user.value) return
  const query = new URLSearchParams()
  query.set("created_by", user.value.username)
  query.set("limit", String(page_length))
  for (const k in params) query.set(k, params[k])
  const url = `/v1/exams/?${query.toString()}`
  loading.value = true
  try {
    const { data, error } = await useApiFetch<any>(url)
    if (error.value) throw error.value
    exams.value = data.value
  } catch (e: any) {
    toasts.error("Failed to load exams")
  } finally {
    loading.value = false
  }
}

function onPageUpdate(newPage: number) {
  page.value = newPage
  const offset = (newPage - 1) * page_length
  getExams({ offset })
}

watchEffect(() => {
  if (user.value) getExams({ offset: (page.value - 1) * page_length })
})
</script>

<template>
  <v-data-iterator
    class="mt-5"
    :items="exams.results"
    :items-per-page="page_length"
    :server-items-length="exams.count"
    :footer-props="{ 'disable-items-per-page': true }"
    @update:page="onPageUpdate"
    :loading="loading"
  >
    <template #default="{ items }">
      <ExamListItem v-for="item in items" :item="item" :key="item.lid" />
    </template>
  </v-data-iterator>
</template>
