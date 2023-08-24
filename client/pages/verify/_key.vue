<template>
  <v-row class="mt-5">
    <v-spacer />
    <v-col cols="7">
      <h2 class="mb-8">{{ $t("login.verify_email") }}</h2>

      <div v-show="error_messages.length > 0">
        <v-alert class="mt-2 alert-pre-line" type="error">
          <ul style="list-style: none; padding: 0">
            <li v-for="(error, i) in error_messages" :key="i">
              {{ error }}
            </li>
          </ul>
        </v-alert>
        <v-form @submit.prevent="resend_link" v-show="!submitted" ref="form">
          <v-text-field
            v-model="email"
            name="email"
            type="email"
            :label="$t('login.email')"
            prepend-icon="mdi-account"
            :rules="[(v) => /.+@.+\..+/.test(v) || $t('login.mail_invalid')]"
            validate-on-blur
            required
          />
          <v-btn
            type="submit"
            class="mx-auto my-6 secondary"
            :disabled="!email"
            @click="resend_link"
            v-text="$t('login.resend_link')"
          />
        </v-form>
      </div>
    </v-col>
    <v-spacer />
  </v-row>
</template>

<script>
export default {
  data: () => ({
    email: "",
    error_messages: [],
    submitted: false,
  }),
  name: "Signup",
  head() {
    return {
      title: this.$t("login.verify_email"),
    }
  },
  methods: {
    async verify_email() {
      const url = "/auth/register/verify-email/"
      const key = this.$route.params.key

      try {
        await this.$auth.axios.post(url, { key })
      } catch (e) {
        if (e.response.status === 404) {
          this.error_messages.push(
            this.$t("login.verify_token_used_or_invalid"),
          )
          return
        }
      }
      this.$router.push({ path: "/login", query: { verified: null } })
    },
    async resend_link() {
      if (!this.email || !this.$refs.form.validate()) return

      const url = "/auth/register/resend-email/"
      const email = this.email

      try {
        const ret = await this.$auth.axios.post(url, { email })
        if (ret.status === 200) this.submitted = true
      } catch (e) {
        // Always returns 200 even for stupid email
        console.warn(e)
      }
    },
  },
  mounted() {
    ;(async () => {
      await this.verify_email()
    })()
  },
}
</script>
