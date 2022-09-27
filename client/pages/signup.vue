<template>
  <v-row class="mt-5">
    <v-spacer></v-spacer>
    <v-col
      v-if="submitted"
      cols="7"
    >
      <p>
        Thank you for signing up.
      </p>
      <p>
        Please check your inbox to confirm your registration.
      </p>
    </v-col>
    <v-col
      v-else
      cols="7"
    >
      <v-form
        ref="signup_form"
        v-model="valid"
        :lazy-validation="true"
        @submit.prevent="register_new_user"
      >
        <h1 class="text-h5 mb-5">Register to TestU</h1>
        <v-text-field
          outlined
          dense
          v-model="username"
          label="User name"
          :rules="[ v => v !== '' || 'Required field' ]"
          required
        ></v-text-field><v-text-field
          outlined
          dense
          v-model="email"
          label="E-mail"
          :rules="[ v => /.+@.+\..+/.test(v) || 'E-mail must be valid' ]"
          required
        ></v-text-field>
        <v-text-field
          outlined
          dense
          v-model="password"
          label="Password"
          type="password"
          :rules="[ v => v !== '' || 'Required field' ]"
          required
        ></v-text-field>
        <v-btn
          type="submit"
          class="primary mt-2"
        >Sign up</v-btn>
        <v-alert
          class="mt-2"
          type="error"
          v-show="!!error_message"
        >
          {{ error_message }}
        </v-alert>
      </v-form>

      <div class="text--secondary mt-8">
      Already have an account?
      <NuxtLink to="/login">Log in</NuxtLink>
      </div>

    </v-col>
    <v-spacer></v-spacer>
  </v-row>
</template>
<script>
  export default {
    data: () => ({
      username: '',
      email: '',
      password: '',
      valid: undefined,
      submitted: false,
      error_message: '',
    }),
    name: 'Signup',
    head() {
      return {
        title: 'SignUp'
      }
    },
    methods: {
      async register_new_user() {
        if (!this.validate()) return;
        const ret = await fetch('/api/auth/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password
          })
        })

        let ret_json;
        try {
          ret_json = await ret.json();
        } catch {
        }

        console.error({ ret, ret_json })

        if (ret.status >= 400) {
          this.error_message = `Error ${ret.status}. ${ret_json}`
          return
        }

        this.submitted = true

      },
      validate() {
        return this.$refs.signup_form.validate()
      },
    }
  }
</script>
