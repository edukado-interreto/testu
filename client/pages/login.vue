<template>
  <v-row>
    <v-col class="text-center">
      <v-form
        ref="login_form"
        v-model="valid"
        lazy-validation
      >
        <v-text-field
          v-model="email"
          label="E-mail"
          :rules="[ v => /.+@.+\..+/.test(v) || 'E-mail must be valid' ]"
          required
        ></v-text-field>
        <v-text-field
          v-model="password"
          label="Password"
          :rules="[ v => v !== '' || 'Required field' ]"
          required
        ></v-text-field>
        <v-btn
          @click="login"
        >Login</v-btn>
        <v-alert
          class="mt-2"
          type="error"
          v-show="!!error_message"
        >
          {{ error_message }}
        </v-alert>
      </v-form>
    </v-col>
  </v-row>
</template>
<script>
  export default {
    data: () => ({
      email: '',
      password: '',
      valid: undefined,
      error_message: '',
    }),
    methods: {
      validate() {
        return this.$refs.login_form.validate()
      },
      login_error_hdl(e) {
        this.error_message = e.join('\n');
      },
      login: async function() {
        if (!this.validate()) return;
        try {
          const response = await this.$auth.login({
            email: this.email,
            password: this.password
          });

          // this "if" is needed because even on failure vue-auth-jwt returns
          // an array of errors instead of throwing an exception.
          // Open issue: https://github.com/johnckealy/vue-auth-jwt/issues/2

          if (response.status && response.status == 200) {
            this.$router.push({
              path: this.$store.state.authenticator.redirectUrl
            });
            return;
          }
          this.login_error_hdl(response);

        } catch(e) {
          // to be future proof when vue-auth-jwt will be fixed
          this.login_error_hdl(e.errorMessages);
        }
      }
    }
  }
</script>
