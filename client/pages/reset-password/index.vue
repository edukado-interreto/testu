<template>
  <v-row class="mt-5">
    <v-spacer />
    <v-col cols="7">
      <h2 class="mb-8">{{ $t("login.password_reset") }}</h2>
      <v-form
        ref="form"
        v-model="valid"
        :disabled="submitted"
        @submit.prevent="submit"
      >
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
          class="mt-2 primary"
          :disabled="!email || submitted"
          v-text="$t('login.password_reset')"
        />
        <div v-show="error_messages.length > 0">
          <v-alert class="mt-2 alert-pre-line" type="error">
            <ul style="list-style: none; padding: 0">
              <li v-for="(error, i) in error_messages" :key="i">
                {{ error }}
              </li>
            </ul>
          </v-alert>
        </div>
      </v-form>
      <v-alert class="mt-6" type="success" v-if="submitted">
        {{ $t("login.password_reset_sent") }}
      </v-alert>
    </v-col>
    <v-spacer />
  </v-row>
</template>

<script>
export default {
  name: "ResetPasswordForm",
  data: () => ({
    email: "",
    error_messages: [],
    valid: undefined,
    submitted: false,
  }),
  methods: {
    validate() {
      return this.$refs.form.validate()
    },
    async submit() {
      if (!this.validate()) return
      const url = "/auth/password/reset/"
      try {
        const response = await this.$auth.axios.post(url, { email: this.email })
        if (response.status == 200) {
          this.error_messages = []
          this.submitted = true
        }
      } catch (e) {
        if (e.response.status === 400) {
          this.error_messages = Object.values(e.response.data).flat()
        }
      }
    },
  },
  mounted() {
    const email = this.$route.query?.email
    if (email) {
      this.email = email
      this.$router.replace(this.$route.path)
    }
  },
}
</script>
