<template>
  <v-data-iterator
    class="mt-5"
    :items="exams.results"
    :items-per-page="page_length"
    :server-items-length="exams.count"
    :footer-props="{ 'disable-items-per-page': true }"
    @update:page="on_page_update"
    :loading="loading"
  >
    <template v-slot:default="props">
      <ExamListItem
        v-for="item in props.items"
        :item="item"
        :key="item.lid"
      ></ExamListItem>
    </template>
  </v-data-iterator>
</template>
<script>
export default {
  data: () => ({
    exams: [],
    loading: false,
    page_length: 15,
  }),
  computed: {
    user() {
      const authUser = this.$store.getters["authenticator/authUser"]
      if (!authUser) return null
      return authUser
    },
  },
  methods: {
    async get_exams_from_api(params_obj) {
      const query = new URLSearchParams()

      query.set("limit", this.page_length)
      for (const k in params_obj) query.set(k, params_obj[k])
      const url = `/v1/exams/?${query.toString()}`
      console.log(`fetching ${url}`)

      this.loading = true
      const resp = await this.$auth.axios.get(url)
      this.loading = false
      this.exams = resp.data
    },
    on_page_update(page) {
      const offset = (page - 1) * this.page_length
      this.get_exams_from_api({ offset })
    },
  },
  async fetch() {
    await this.get_exams_from_api({ created_by: this.user.username })
  },
  fetchOnServer: true,
  fetchKey: "exams",
}
</script>
