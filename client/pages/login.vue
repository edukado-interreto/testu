<template>
  <v-container>
    <v-row class="mt-5">
      <v-spacer />
      <v-col cols="7">
        <v-alert type="success" v-if="'verified' in $route.query">
          {{ $t("login.email_is_verified") }}
        </v-alert>
        <v-alert type="success" v-if="'reset' in $route.query">
          {{ $t("login.password_reset_done") }}
        </v-alert>
        <v-form
          ref="login_form"
          v-model="valid"
          :lazy-validation="true"
          @submit.prevent="login"
        >
          <v-text-field
            v-model="email"
            name="email"
            type="email"
            :label="$t('login.email')"
            prepend-icon="mdi-account"
            :rules="[(v) => /.+@.+\..+/.test(v) || $t('login.mail_invalid')]"
            validate-on="blur"
            required
          />
          <v-text-field
            v-model="password"
            :label="$t('login.password')"
            type="password"
            prepend-icon="mdi-lock"
            :rules="[(v) => v !== '' || $t('login.required_field')]"
            required
          />
          <v-btn type="submit" class="primary mt-2">
            {{ $t("login.login") }}
          </v-btn>
          <v-btn
            class="secondary mt-2 ms-2"
            :to="`/reset-password/?email=${email}`"
            v-show="!!error_message"
          >
            {{ $t("login.password_reset") }}
          </v-btn>
          <v-alert class="mt-6" type="error" v-show="!!error_message">
            {{ error_message }}
          </v-alert>
        </v-form>
      </v-col>
      <v-spacer />
    </v-row>
    <v-row>
      <v-col class="mx-auto col-8 col-lg-6">
        <v-sheet color="grey lighten-4 mt-12 pa-6" rounded="xl">
          <p
            class="text-center grey--text"
            v-text="$t('login.no_account_yet')"
          />
          <p class="text-center mt-4">
            <v-btn
              class="text-none amber px-8"
              text
              nuxt
              :to="localePath('/signup')"
            >
              {{ $t("main.signup") }}
            </v-btn>
          </p>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    email: "",
    password: "",
    valid: undefined,
    error_message: "",
  }),
  name: "Login",
  head() {
    return {
      title: this.$t("login.page_title"),
    }
  },
  methods: {
    validate() {
      return this.$refs.login_form.validate()
    },
    login_error_hdl(e) {
      this.error_message = e.join("\n")
    },
    login: async function () {
      if (!this.validate()) return
      try {
        const response = await this.$auth.login({
          email: this.email,
          password: this.password,
        })

        // this "if" is needed because even on failure vue-auth-jwt returns
        // an array of errors instead of throwing an exception.
        // Open issue: https://github.com/johnckealy/vue-auth-jwt/issues/2

        if (response.status && response.status == 200) {
          this.$router.push({
            path: this.$store.state.authenticator.redirectUrl,
          })
          return
        }
        this.login_error_hdl(response)
      } catch (e) {
        // to be future proof when vue-auth-jwt will be fixed
        this.login_error_hdl(e.errorMessages)
      }
    },
  },
}
</script>
