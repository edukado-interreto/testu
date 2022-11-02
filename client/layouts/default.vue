<template>
  <v-app id="inspire">
    <v-app-bar
      app
      clipped-right
      clipped-left
      flat
      outlined
      style="border-bottom: 1px solid #d2d2d2 !important;"
      color="white"
    >
      <v-app-bar-nav-icon @click.stop="nav_drawer.show = !nav_drawer.show"/>
      
      <img src="/favicon.png" class="mx-3" height="40"/>
      <v-toolbar-title
        class="accent--text"
        v-text="title"
      />
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
            {{ $i18n.locale }}
            <v-icon class="ml-1">mdi-chevron-down</v-icon>
          </v-btn>
        </template>

        <v-list dense rounded>
          <v-subheader
            class="text--primary font-weight-black text-uppercase"
          >{{ $t("main.lang_menu_header") }}</v-subheader>
          <v-list-item
            v-for="lang in $i18n.localeCodes"
            nuxt
            :to="switchLocalePath(lang)"
            :class="{ 'v-list-item--active': lang == $i18n.locale }"
            :key="lang"
          >
            <v-list-item-content>
              <v-list-item-title>{{ $t(`langs.${lang}`) }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <!--
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
          -->
        </v-list>

      </v-menu>

      <div
        v-if="!logged_in"
        class="ml-3"
      >
        <v-btn
          class="mr-1 text-none grey lighten-4"
          text
          nuxt
          to="/login"
        >{{ $t("main.login") }}</v-btn>
        <v-btn
          class="text-none amber"
          text
          nuxt
          to="/signup"
        >{{ $t("main.signup") }}</v-btn>
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
              <v-list-item-title>{{authUser.username}}</v-list-item-title>
              <v-list-item-subtitle>{{authUser.email}}</v-list-item-subtitle>
            </v-list-item-content>

          </v-list-item>

          <v-divider></v-divider>

          <v-list-item
            to="/profile"
            router
            exact
            disabled
          >
            <v-list-item-action>
              <v-icon>mdi-cog</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{$t("main.settings")}}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-list-item
            @click="logout"
          >
            <v-list-item-action>
              <v-icon>mdi-logout</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{ $t("main.logout") }}</v-list-item-title>
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
      <v-list
      class="primary--text"
      >

        <v-list-item
          :to="localePath('/')"
          nuxt
          router
          exact
        >
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{$t("main.home")}}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item
          :to="localePath('/learn')"
          nuxt
          router
          exact
          disabled
        >
          <v-list-item-action>
            <v-icon>mdi-chart-bar</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{$t("main.my_learning")}}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item
          :to="localePath('/teach')"
          nuxt
          router
          exact
        >
          <v-list-item-action>
            <v-icon>mdi-briefcase</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{$t("main.my_teaching")}}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item
          :to="localePath('/about')"
          nuxt
          router
          exact
          disabled
        >
          <v-list-item-action>
            <v-icon>mdi-information</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{$t("main.about")}}</v-list-item-title>
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
      class="grey lighten-5"
    >
      <v-spacer></v-spacer>
      <div>
        <NuxtLink to="/terms" class="grey--text caption text-decoration-none font-weight-bold">
         {{ $t("main.terms") }}
        </NuxtLink>
        <span class="caption mx-1">·</span>
        <NuxtLink to="/privacy" class="caption text-decoration-none font-weight-bold">
         {{ $t("main.privacy") }}
        </NuxtLink>
      </div>
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
      return this.authUser && this.authUser.username !== undefined
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
