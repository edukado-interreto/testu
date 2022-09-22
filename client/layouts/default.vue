<template>
  <v-app id="inspire">
    <v-app-bar
      app
      clipped-right
      clipped-left
      height="72"
      flat
    >
      <v-app-bar-nav-icon @click.stop="nav_drawer.show = !nav_drawer.show"/>
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <!-- {{ authUser }} -->
      <v-menu
        offset-y
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            text
            v-bind="attrs"
            v-on="on"
            class="text-none px-1 mr-1"
          >
            <v-icon class="mr-1">mdi-translate</v-icon>
            en
            <v-icon class="ml-1">mdi-chevron-down</v-icon>
          </v-btn>
        </template>

        <v-list dense rounded>
          <v-subheader
            class="text--primary font-weight-black text-uppercase"
          >Interface language</v-subheader>
          <v-list-item @click="" class="v-list-item--active">
            <v-list-item-content>
              <v-list-item-title>English</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="">
            <v-list-item-content>
              <v-list-item-title>Esperanto</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="">
            <v-list-item-content>
              <v-list-item-title>French</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="">
            <v-list-item-content>
              <v-list-item-title>Italian</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>

      </v-menu>

      <div
        v-if="!logged_in"
        class="ml-3"
      >
        <v-btn
          class="mr-1 text-none white"
          text
          nuxt
          to="/login"
        >Log in</v-btn>
        <v-btn
          class="text-none primary"
          text
        >Sign up</v-btn>
      </div>

      <v-menu
        v-if="logged_in"
        offset-y
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>

        <v-list dense>
          <v-list-item>
            <v-list-item-avatar>
              <v-icon>mdi-account</v-icon>
              <!--img
                src="https://cdn.vuetifyjs.com/images/john.jpg"
                alt="John"
              -->
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title>{{authUser.id}}</v-list-item-title>
              <v-list-item-subtitle>{{authUser.email}}</v-list-item-subtitle>
            </v-list-item-content>

          </v-list-item>

          <v-divider></v-divider>

          <v-list-item
            to="/profile"
            router
            exact
          >
            <v-list-item-action>
              <v-icon>mdi-cog</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Account settings</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-list-item
            @click="logout"
          >
            <v-list-item-action>
              <v-icon>mdi-logout</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

        </v-list>

      </v-menu>



    </v-app-bar>
    <v-navigation-drawer
      v-model="nav_drawer.show"
      disable-resize-watcher
      app
      clipped
    >
      <v-list>

        <v-list-item
          to="/"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item
          to="/learn"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>mdi-chart-bar</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>My learning</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item
          to="/teach"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>mdi-briefcase</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>My teaching</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item
          to="/about"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>mdi-information</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>About</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

      </v-list>
    </v-navigation-drawer>
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer
      app
    >
      <span>TestU Online – sandbox 0.1</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'default',
  data: () => ({
    nav_drawer: {
      show: true
    },
    title: 'testu.eu'
  }),
  methods: {
    async logout() {
      await this.$auth.logout()
      this.$router.push('/')
    },
  },
  mounted: async function() {
    await this.$store.dispatch("authenticator/CHECK_TOKENS");
    try {
      await this.$auth.user(true)
    } catch {
      console.error('this.$auth.user raised an exception')
    }
  },
  computed: {
    logged_in() {
      return this.authUser && this.authUser.id !== undefined
    },
    authUser() {
      return this.$store.getters['authenticator/authUser']
    }
  },
}
</script>
<style scoped>
  #toc .active {
    font-weight: bold;
    color: red;
  }
  .rotated {
    transform: rotate(-180deg);
  }
</style>
