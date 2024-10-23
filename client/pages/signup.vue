<template>
  <v-row class="mt-5">
    <v-spacer></v-spacer>
    <v-col v-if="submitted" cols="7">
      <p>
        {{ $t("login.signup_thanks") }}
      </p>
      <p>
        {{ $t("login.check_inbox") }}
      </p>
    </v-col>
    <v-col v-else cols="7">
      <v-form
        ref="signup_form"
        v-model="valid"
        :lazy-validation="true"
        @submit.prevent="register_new_user"
      >
        <h1 class="text-h5 mb-5">{{ $t("login.signup") }}</h1>
        <v-text-field
          outlined
          dense
          v-model="username"
          :label="$t('login.username')"
          :rules="[(v) => v !== '' || $t('login.required_field')]"
          required
        ></v-text-field>
        <v-text-field
          outlined
          dense
          v-model="email"
          :label="$t('login.email')"
          :rules="[(v) => /.+@.+\..+/.test(v) || $t('login.mail_invalid')]"
          type="email"
          name="email"
          validate-on="blur"
          required
        ></v-text-field>
        <v-text-field
          outlined
          dense
          v-model="password"
          :label="$t('login.password')"
          type="password"
          :rules="[(v) => v !== '' || $t('login.required_field')]"
          required
        ></v-text-field>
        <v-btn type="submit" class="primary mt-2">
          {{ $t("main.signup") }}
        </v-btn>
        <v-alert
          class="mt-2 alert-pre-line"
          type="error"
          v-show="error_messages.length > 0"
        >
          <ul style="list-style: none; padding: 0">
            <li v-for="(error, i) in error_messages">
              {{ error }}
            </li>
          </ul>
        </v-alert>
      </v-form>

      <div class="text--secondary mt-8">
        {{ $t("login.already_registered") }}
        <NuxtLink to="/login">{{ $t("main.login") }}</NuxtLink>
      </div>
    </v-col>
    <v-spacer></v-spacer>
  </v-row>
</template>
<script>
export default {
  data: () => ({
    username: "",
    email: "",
    password: "",
    valid: undefined,
    submitted: false,
    error_messages: [],
  }),
  name: "Signup",
  head() {
    return {
      title: this.$t("login.signup"),
    }
  },
  methods: {
    async register_new_user() {
      if (!this.validate()) return

      this.error_messages = []

      try {
        const ret = await this.$auth.axios.post("/auth/register/", {
          username: this.username,
          email: this.email,
          password1: this.password,
          password2: this.password,
        })
        this.submitted = true
      } catch (e) {
        if (e.response.status === 400) {
          this.error_messages = Object.values(e.response.data).flat()
          return
        }
        this.error_messages = [`Server error (${e.response.status})`]
        console.error({ ...e })
      }
    },
    validate() {
      return this.$refs.signup_form.validate()
    },
  },
}
</script>
