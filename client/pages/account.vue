<template>
  <v-container v-if="user">
    <h1>{{ $t("account.title") }}</h1>

    <v-sheet
      class="mx-auto mt-12"
      style="width: 20vw; min-width: 20em; height: 40vh"
    >
      <dl>
        <dd>{{ $t("login.username") }}</dd>
        <dt>{{ user.username }}</dt>
        <dd>{{ $t("login.email") }}</dd>
        <dt>{{ user.email }}</dt>
      </dl>
    </v-sheet>
    <v-card outlined class="mt-12">
      <v-card-title class="red white--text">
        {{ $t("account.danger_zone") }}
      </v-card-title>
      <v-card-text class="d-flex flex-column">
        <v-dialog v-model="delete_dialog" width="50vw" style="min-width: 20em">
          <template #activator="{ on, attrs }">
            <v-btn
              color="red"
              class="mx-auto my-8 white--text"
              v-bind="attrs"
              v-on="on"
            >
              {{ $t("account.delete_btn") }}
            </v-btn>
          </template>
          <v-card>
            <v-card-text class="pt-12">
              <p class="text-h6 text-center">
                {{ $t("account.delete_description") }}
              </p>
            </v-card-text>
            <v-card-actions class="pb-10">
              <v-spacer />
              <v-btn
                @click="delete_account"
                color="red"
                class="white--text px-8 py-5"
              >
                <v-icon left>mdi-fire</v-icon>
                {{ $t("account.delete_confirm_btn") }}
              </v-btn>
              <v-spacer />
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-card-text>
    </v-card>
  </v-container>
  <v-container v-else>
    <v-sheet color="grey lighten-4 mt-12 pa-6" rounded="xl">
      <p class="text-center grey--text" v-text="$t('login.no_account_yet')" />
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
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      delete_dialog: false,
    }
  },
  computed: {
    user() {
      return this.$store.getters["authenticator/authUser"]
    },
  },
  methods: {
    async delete_account() {
      this.$auth.axios.delete("/auth/user/delete/")
      this.$router.push("/")
      await this.$auth.logout()
    },
  },
  middleware: "redirects",
  meta: {
    requiresAuth: true,
  },
}
</script>

<style lang="scss" scoped>
dl {
  dd {
    color: rgba(black, 60%);
    font-size: 70%;
  }
  dt {
    margin-bottom: 1.3rem;
  }
}
</style>
