<template>
  <v-container>
    <v-tabs v-model="tab">
      <v-tab>{{ $t("teach.exercises") }}</v-tab>
      <v-tab>{{ $t("teach.exams") }}</v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab" class="pa-1 mt-5">
      <!-- exercises -->
      <v-tab-item>
        <v-data-iterator
          class="mt-5"
          :items="exercises.results"
          :items-per-page="page_length"
          :server-items-length="exercises.count"
          :footer-props="{ 'disable-items-per-page': true }"
          @update:page="on_page_update"
          :loading="loading"
        >
          <template v-slot:default="props">
            <ExerciseListItem
              v-for="item in props.items"
              :item="item"
              :key="item.lid"
            ></ExerciseListItem>
          </template>
        </v-data-iterator>
      </v-tab-item>

      <!-- exams -->
      <v-tab-item>
        <ExamList></ExamList>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>
<script>
import langs_available from "~/mixins/langs_available.js"
import cefr from "~/mixins/cefr.js"
export default {
  name: "Teach",
  head() {
    return {
      title: this.$t("main.my_teaching"),
    }
  },
  mixins: [langs_available, cefr],
  data: () => ({
    exercises: [],
    page_length: 15,
    loading: false,
  }),
  computed: {
    tab: {
      get() {
        return this.$route.hash == "#exams" ? 1 : 0
      },
      set(val) {
        this.$router.replace({ hash: val === 1 ? "#exams" : "" })
      },
    },
    current_username() {
      const authUser = this.$store.getters["authenticator/authUser"]
      if (!authUser) return null
      return authUser.username
    },
  },
  methods: {
    async get_exercises_from_api(params_obj) {
      const query = new URLSearchParams()

      query.set("limit", this.page_length)
      query.set("created_by", this.current_username)
      for (const k in params_obj) query.set(k, params_obj[k])
      const url = `/v1/exercises/?${query.toString()}`
      console.log(`fetching ${url}`)

      this.loading = true
      const resp = await this.$auth.axios.get(url)
      this.loading = false
      this.exercises = resp.data
      // {
      //   "count": 7,
      //   "next": "http://…/api/v1/exercises/?limit=2&offset=2",
      //   "previous": null,
      //   "results": [ … ]
      // }
    },
    on_page_update(page) {
      const offset = (page - 1) * this.page_length
      this.get_exercises_from_api({ offset })
    },
  },
  async fetch() {
    await this.get_exercises_from_api()
  },
  fetchOnServer: true,
  fetchKey: "exercises",
  middleware: "redirects",
  meta: {
    requiresAuth: true,
  },
}
</script>
