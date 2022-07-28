<template>
  <v-row>
    <v-col class="text-center">
      <blockquote class="blockquote">This page is available only for signed in users</blockquote>
      {{ user.email }}
    </v-col>
  </v-row>
</template>
<script>
export default {
  data: () => ({
    user: {}
  }),
  mounted: async function() {
    this.user = await this.$auth.user(true)
  },
  middleware: 'redirects',
  meta: {
    requiresAuth: true
  }
}
</script>
