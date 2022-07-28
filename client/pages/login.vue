<template>
  <v-row>
    <v-col class="text-center">
      <v-form>
        <v-text-field
          v-model="email"
          label="E-mail"
          required
        ></v-text-field>
        <v-text-field
          v-model="password"
          label="Password"
          required
        ></v-text-field>
        <v-btn
          @click="login"
        >Login</v-btn>
      </v-form>
    </v-col>
  </v-row>
</template>
<script>
  export default {
    data: () => ({
      email: '',
      password: ''
    }),
    methods: {
      login: async function() {
        try {
          const response = await this.$auth.login({
            email: this.email,
            password: this.password
          });
          console.log("neniu eraro");
          console.log(response);
          //redirect(
          //  this.$store.state.authenticator.redirectUrl
          //);
        } catch {
          console.log("error handling");
          console.log(response);
        }
      }
    }
  }
</script>
