<script setup lang="ts">
import { KeepAlive } from "vue"

onMounted(async () => {})

definePageMeta({ middleware: ["authenticated"] })

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const localePath = useLocalePath()
const { $api } = useNuxtApp()

useHead({ title: t("main.my_teaching") })

const page = shallowRef(1)
const page_length = ref(50)
const offset = computed(() => (page.value - 1) * page_length.value)

// Computed properties
const tab = computed({
  get() {
    return route.hash === "#exams" ? 1 : 0
  },
  set(val: number) {
    router.replace({ hash: val === 1 ? "#exams" : "" })
  },
})

const params = computed(() => ({
  limit: page_length.value,
  offset: offset.value,
  created_by: auth.user?.username,
}))

const {
  data: exercises,
  error,
  status,
  refresh,
} = await useAsyncData(
  "exercises",
  () => $api<DRF<Exercise>>("exercises/", { query: params.value }),
  { server: false, watch: [params] },
)
const loading = computed(() => {
  if (!status?.value) return true
  return ["pending", "idle"].includes(status.value)
})
</script>

<template>
  <v-container>
    <v-tabs v-model="tab" color="primary">
      <v-tab>{{ $t("teach.exercises") }}</v-tab>
      <v-tab>{{ $t("teach.exams") }}</v-tab>
    </v-tabs>

    <KeepAlive>
      <v-tabs-window v-model="tab" class="pa-1 mt-5">
        <!-- exercises -->
        <v-tabs-window-item id="exercises">
          <v-btn
            class="text-primary mt-3"
            :to="localePath('/editor')"
            size="large"
            variant="flat"
            nuxt
          >
            <v-icon class="mr-1">mdi-plus</v-icon>
            {{ $t("home.create_exercise") }}
          </v-btn>

          <v-data-table
            v-if="exercises"
            class="mt-5"
            :items="exercises.results"
            :items-per-page="page_length"
            :server-items-length="exercises.count"
            :footer-props="{ 'disable-items-per-page': true }"
            :loading="loading"
            hide-default-header
          >
            <template #item="{ item }">
              <ExerciseListItem class="ma-1" :item="item" :key="item.lid" />
            </template>
          </v-data-table>
        </v-tabs-window-item>

        <!-- exams -->
        <v-tabs-window-item id="exams">
          <ExamList />
        </v-tabs-window-item>
      </v-tabs-window>
    </KeepAlive>
  </v-container>
</template>
