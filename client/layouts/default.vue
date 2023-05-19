<template>
  <v-app id="inspire">
    <v-app-bar
      app
      clipped-right
      clipped-left
      flat
      outlined
      style="border-bottom: 1px solid #d2d2d2 !important"
      color="white"
      class="d-print-none"
    >
      <v-app-bar-nav-icon @click.stop="nav_drawer.show = !nav_drawer.show" />

      <img src="/favicon.png" class="mx-3" height="40" />
      <v-toolbar-title class="accent--text" v-text="title" />
      <v-spacer />
      <!-- {{ authUser }} -->
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn text v-bind="attrs" v-on="on" class="text-none px-1 mr-1">
            <v-icon class="mr-1">mdi-translate</v-icon>
            <span class="d-none d-sm-inline">{{
              locale_names[$i18n.locale]
            }}</span>
            <v-icon class="ml-1">mdi-chevron-down</v-icon>
          </v-btn>
        </template>

        <v-list dense rounded>
          <v-subheader class="text--primary font-weight-black text-uppercase">{{
            $t('main.lang_menu_header')
          }}</v-subheader>
          <v-list-item
            v-for="lang in $i18n.localeCodes"
            nuxt
            :to="switchLocalePath(lang)"
            :class="{ 'v-list-item--active': lang == $i18n.locale }"
            :key="lang"
          >
            <v-list-item-content>
              <v-list-item-title>{{ locale_names[lang] }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>

      <div v-if="!logged_in" class="ml-3">
        <v-btn
          class="mr-1 text-none grey lighten-4"
          text
          nuxt
          :to="localePath('/login')"
          >{{ $t('main.login') }}</v-btn
        >
        <v-btn class="text-none amber" text nuxt :to="localePath('/signup')">{{
          $t('main.signup')
        }}</v-btn>
      </div>

      <v-menu v-if="logged_in" offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
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
              <v-list-item-title>{{ authUser.username }}</v-list-item-title>
              <v-list-item-subtitle>{{ authUser.email }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-divider></v-divider>

          <v-list-item to="/profile" router exact disabled>
            <v-list-item-action>
              <v-icon>mdi-cog</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{ $t('main.settings') }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-list-item @click="logout">
            <v-list-item-action>
              <v-icon>mdi-logout</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>{{ $t('main.logout') }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-navigation-drawer
      v-model="nav_drawer.show"
      class="d-print-none"
      disable-resize-watcher
      app
      clipped
    >
      <v-list class="primary--text">
        <v-list-item :to="localePath('/')" nuxt router exact>
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ $t('main.home') }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item :to="localePath('/learn')" nuxt router exact>
          <v-list-item-action>
            <v-icon>mdi-chart-bar</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ $t('main.my_learning') }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item :to="localePath('/teach')" nuxt router exact>
          <v-list-item-action>
            <v-icon>mdi-briefcase</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ $t('main.my_teaching') }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item :to="localePath('/about')" nuxt router exact>
          <v-list-item-action>
            <v-icon>mdi-information</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ $t('main.about') }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <Nuxt />
    </v-main>
    <v-footer absolute app padless class="grey lighten-4 d-print-none">
      <div
        id="erasmus"
        class="white d-sm-flex align-center"
        :class="nav_drawer.show ? 'drawer-open' : ''"
      >
        <img src="/partners/erasmus.png" class="mx-3" height="26" alt="" />
        <p class="grey--text text--darken-1 ma-3" style="font-size: 0.9em">
          {{ $t('about.partners.european_commission') }}
        </p>
      </div>
      <v-spacer></v-spacer>
      <div class="px-4 py-2">
        <NuxtLink
          :to="localePath('/terms')"
          class="grey--text caption text-decoration-none font-weight-bold"
        >
          {{ $t('main.terms') }}
        </NuxtLink>
        <span class="caption mx-1">·</span>
        <NuxtLink
          :to="localePath('/privacy')"
          class="caption text-decoration-none font-weight-bold"
        >
          {{ $t('main.privacy') }}
        </NuxtLink>
      </div>
      <CookieConsent />
    </v-footer>
  </v-app>
</template>

<script>
import locale_names from '~/i18n/locale_names.json';

export default {
  name: 'default',
  data: () => ({
    nav_drawer: {
      show: true,
    },
    title: 'testu.eu',
    locale_names,
  }),
  methods: {
    async logout() {
      await this.$auth.logout();
      this.$router.push('/');
    },
  },
  created: async function () {
    //await this.$store.dispatch("authenticator/CHECK_TOKENS");
    await this.$auth.checkTokens();
    try {
      const ret = await this.$auth.user(true);
      console.log('this.$auth.user:', ret);
      console.log('computed authUser', this.authUser);
    } catch (e) {
      if (e.response.status) {
        // unauthorized: the user is not logged in
        console.log('user not logged in');
      } else {
        console.error('this.$auth.user raised an exception');
        console.error({ ...e });
        throw e;
      }
    }

    // set the initial value for the vuetify language.
    this.$vuetify.lang.current = this.$i18n.locale;
  },
  computed: {
    logged_in() {
      return this.authUser?.username !== undefined;
    },
    authUser() {
      return this.$store.getters['authenticator/authUser'];
    },
  },
};
</script>
<style scoped lang="scss">
@import '~vuetify/src/styles/settings/_variables';

@media print {
  .v-main {
    padding: 0 !important;
    width: 100% !important;
  }
}

#toc .active {
  font-weight: bold;
  color: red;
}
.rotated {
  transform: rotate(-180deg);
}

.v-navigation-drawer {
  max-height: 100vh !important;
}

#erasmus {
  padding: 4rem 6rem 1rem;

  &.drawer-open {
    @media #{map-get($display-breakpoints, 'md-and-up')} {
      padding-left: calc(256px + 6rem);
    }
  }
}
</style>
