<template>
  <v-app id="inspire">
    <v-app-bar
      v-if="!embedded"
      :app="!embedded"
      clipped-right
      clipped-left
      flat
      outlined
      style="border-bottom: 1px solid #d2d2d2 !important"
      color="white"
      class="d-print-none"
    >
      <v-app-bar-nav-icon @click.stop="nav_drawer.show = !nav_drawer.show" />
      <v-btn class="text-none transparent" text nuxt :to="localePath('/')">
        <img src="/favicon.png" class="mx-3" height="40" />
        <v-toolbar-title class="accent--text" v-text="title" />
      </v-btn>
      <v-spacer />
      <h6
        class="catchphrase d-none d-md-block accent--text"
        v-text="$t('main.catchphrase')"
      />
      <v-spacer />

      <v-sheet id="top-social-icons" class="mx-1 d-none d-md-flex">
        <v-btn
          href="https://t.me/+8Z1dtayqGzk2Yzk0"
          target="_blank"
          class="mx-1"
          small
          icon
        >
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-img
                contain
                src="https://upload.wikimedia.org/wikipedia/commons/8/83/Telegram_2019_Logo.svg"
                max-height="28"
                max-width="28"
                v-bind="attrs"
                v-on="on"
              />
            </template>
            <span>Telegram</span>
          </v-tooltip>
        </v-btn>

        <v-btn
          href="https://www.facebook.com/profile.php?id=100086451753450"
          target="_blank"
          class="mx-1"
          small
          icon
        >
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-img
                v-bind="attrs"
                v-on="on"
                contain
                src="https://upload.wikimedia.org/wikipedia/en/0/04/Facebook_f_logo_%282021%29.svg"
                max-height="28"
                max-width="28"
              />
            </template>
            <span>Facebook</span>
          </v-tooltip>
        </v-btn>
      </v-sheet>

      <LanguageSwitcher />

      <div v-if="!logged_in" class="d-none d-md-block ml-3">
        <v-btn
          class="mr-1 text-none grey lighten-4"
          text
          nuxt
          :to="localePath('/login')"
        >
          {{ $t("main.login") }}
        </v-btn>
        <v-btn class="text-none amber" text nuxt :to="localePath('/signup')">
          {{ $t("main.signup") }}
        </v-btn>
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
              <v-list-item-title>{{ $t("main.settings") }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <v-list-item @click="logout">
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
      v-if="!embedded"
      :app="!embedded"
      v-model="nav_drawer.show"
      class="d-print-none"
      disable-resize-watcher
      clipped
    >
      <v-list class="primary--text">
        <v-list-item :to="localePath('/')" nuxt router exact>
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ $t("main.home") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item class="d-md-none" text nuxt :to="localePath('/login')">
          <v-list-item-action>
            <v-icon>mdi-login</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            {{ $t("main.login") }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item class="d-md-none" text nuxt :to="localePath('/signup')">
          <v-list-item-action>
            <v-icon>mdi-account-plus</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            {{ $t("main.signup") }}
          </v-list-item-content>
        </v-list-item>

        <v-list-item :to="localePath('/learn')" nuxt router exact>
          <v-list-item-action>
            <v-icon>mdi-chart-bar</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ $t("main.my_learning") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item :to="localePath('/teach')" nuxt router exact>
          <v-list-item-action>
            <v-icon>mdi-briefcase</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ $t("main.my_teaching") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item :to="localePath('/about')" nuxt router exact>
          <v-list-item-action>
            <v-icon>mdi-information</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ $t("main.about") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item :to="localePath('/why')" nuxt router exact>
          <v-list-item-action>
            <v-icon>mdi-star-shooting-outline</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ $t("main.why") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item :to="localePath('/guide')" nuxt router exact>
          <v-list-item-action>
            <v-icon>mdi-help-circle</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ $t("main.guide") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-subheader class="d-md-none">{{ $t("main.social") }}</v-subheader>
        <v-list-item
          class="d-md-none"
          href="https://t.me/+8Z1dtayqGzk2Yzk0"
          target="_blank"
        >
          <v-list-item-action>
            <v-img
              contain
              src="https://upload.wikimedia.org/wikipedia/commons/8/83/Telegram_2019_Logo.svg"
              max-height="32"
              max-width="32"
            />
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Telegram</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item
          class="d-md-none"
          href="https://www.facebook.com/profile.php?id=100086451753450"
          target="_blank"
        >
          <v-list-item-action>
            <v-img
              contain
              src="https://upload.wikimedia.org/wikipedia/en/0/04/Facebook_f_logo_%282021%29.svg"
              max-height="32"
              max-width="32"
            />
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Facebook</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <Nuxt />
    </v-main>
    <v-footer
      v-if="!embedded"
      :app="embedded"
      padless
      class="grey lighten-4 flex-column d-print-none"
    >
      <div
        id="erasmus"
        class="white d-sm-flex align-center"
        :class="nav_drawer.show ? 'drawer-open' : ''"
      >
        <v-spacer />
        <img src="/partners/erasmus.png" class="mx-3" height="26" alt="" />
        <p class="grey--text text--darken-1 ma-3" style="font-size: 0.9em">
          {{ $t("about.partners.european_commission") }}
        </p>
        <v-spacer />
      </div>

      <div class="px-4 py-2">
        <v-icon>mdi-creative-commons</v-icon>
        <a
          rel="license"
          href="https://creativecommons.org/publicdomain/zero/1.0/"
          target="_blank"
          style="font-family: monospace; font-weight: bold"
          class="grey--text caption text-decoration-none font-weight-bold"
        >
          CC0
        </a>
        <span class="caption mx-1">·</span>
        <v-icon>mdi-open-source-initiative</v-icon>
        <a
          href="https://gitlab.com/edukado-interreto/testu/"
          target="_blank"
          style="font-family: monospace; font-weight: bold"
          class="grey--text caption text-decoration-none font-weight-bold"
        >
          {{ $t("main.source_code") }}
        </a>
        <span class="caption mx-1">·</span>
        <NuxtLink
          :to="localePath('/terms')"
          class="grey--text caption text-decoration-none font-weight-bold"
        >
          {{ $t("main.terms") }}
        </NuxtLink>
        <span class="caption mx-1">·</span>
        <NuxtLink
          :to="localePath('/privacy')"
          class="caption text-decoration-none font-weight-bold"
        >
          {{ $t("main.privacy") }}
        </NuxtLink>
      </div>
      <CookieConsent />
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: "default",
  data: () => ({
    nav_drawer: {
      show: true,
    },
    title: "testu.eu",
  }),
  methods: {
    async logout() {
      await this.$auth.logout()
      this.$router.push("/")
    },
  },
  created: async function () {
    //await this.$store.dispatch("authenticator/CHECK_TOKENS");
    await this.$auth.checkTokens()
    try {
      const ret = await this.$auth.user(true)
    } catch (e) {
      if (e.response.status) {
        // unauthorized: the user is not logged in
      } else {
        console.error("this.$auth.user raised an exception")
        console.error({ ...e })
        throw e
      }
    }

    // set the initial value for the vuetify language.
    this.$vuetify.lang.current = this.$i18n.locale
  },
  computed: {
    embedded() {
      return window.location !== window.parent.location
    },
    logged_in() {
      return this.authUser?.username !== undefined
    },
    authUser() {
      return this.$store.getters["authenticator/authUser"]
    },
  },
}
</script>

<style lang="scss">
@media print {
  .v-image *, /* Vuetify v2 */
  .v-img * {
    print-color-adjust: exact; /* force printing background */
  }
}
</style>

<style scoped lang="scss">
@import "~vuetify/src/styles/settings/_variables";
@import "~vuetify/src/styles/settings/_colors";

@media print {
  .v-main {
    padding: 0 !important;
    width: 100% !important;
  }
}

.v-main {
  margin-bottom: 4em;
  min-height: 50vh;
}
.transparent.v-btn--active::before {
  opacity: 0 !important;
}
.catchphrase {
  font-family: "Roboto Slab", Roboto, serif;
  font-size: 120%;
  font-weight: 700;
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
  width: 100vw;

  p {
    max-width: 50rem;
  }

  &.drawer-open {
    @media #{map-get($display-breakpoints, 'md-and-up')} {
      padding-left: calc(256px + 6rem);
    }
  }
}
</style>
