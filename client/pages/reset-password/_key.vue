<template>
  <v-row class="mt-5">
    <v-spacer />
    <v-col cols="7">
      <h2 class="mb-8">{{ $t("login.password_reset") }}</h2>

      <v-form @submit.prevent="submit" :disabled="submitted" ref="form">
        <v-text-field
          v-model="password"
          name="password"
          :type="show ? 'text' : 'password'"
          :label="$t('login.password')"
          prepend-icon="mdi-lock"
          :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append="show = !show"
          required
        />
        <v-btn
          type="submit"
          class="mt-2 primary"
          :disabled="!password"
          v-text="$t('login.password_reset')"
        />
        <v-btn
          class="secondary mt-2 ms-2"
          @click="reset_password"
          v-show="invalid"
        >
          {{ $t("login.resend_link") }}
        </v-btn>
      </v-form>
      <div v-show="error_messages.length > 0">
        <v-alert class="mt-6 alert-pre-line" type="error">
          <ul style="list-style: none; padding: 0">
            <li v-for="(error, i) in error_messages" :key="i">
              {{ error }}
            </li>
          </ul>
        </v-alert>
      </div>
    </v-col>
    <v-spacer />
  </v-row>
</template>

<script>
export default {
  name: "ResetPassword",
  data: () => ({
    password: "",
    error_messages: [],
    show: false,
    invalid: false,
    submitted: false,
  }),
  head() {
    return {
      title: this.$t("login.password_reset"),
    }
  },
  methods: {
    async submit() {
      const url = "/auth/password/reset/confirm/"
      const [uid, token] = this.$route.params.key.split(":")
      const pw = this.password
      try {
        const response = await this.$auth.axios.post(url, {
          new_password1: pw,
          new_password2: pw,
          uid,
          token,
        })
        if (response.status == 200) {
          this.submitted = true
          this.$router.push({ path: "/login", query: { reset: null } })
        }
      } catch (e) {
        if (e.response.status == 400) {
          const errors = Object.keys(e.response.data)
          if (errors.includes("token") || errors.includes("uid")) {
            this.error_messages = [
              this.$t("login.verify_token_used_or_invalid"),
            ]
            this.invalid = true
          } else if (errors.includes("new_password2")) {
            this.error_messages = e.response.data.new_password2
          }
        }
        return
      }
    },
  },
}
</script>
