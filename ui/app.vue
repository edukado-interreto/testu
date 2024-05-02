<script setup lang="ts">
const nav_drawer: Ref = ref({ show: true })
const logged_in: Ref = ref(true)
const authUser: Ref = ref({ username: "username", email: "email" })
const embedded = false
const $t = (s) => s
const localePath = (s) => s
</script>

<template>
  <v-app>
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
      <template v-slot:prepend>
        <v-app-bar-nav-icon @click.stop="nav_drawer.show = !nav_drawer.show" />
      </template>

      <v-app-bar-title class="text--accent">
        <nuxt-link
          class="bg-transparent"
          variant="text"
          nuxt
          :to="localePath('/')"
        >
          <img src="/favicon.png" class="mx-3" height="40" />
          {{ $t("title") }}
        </nuxt-link>
      </v-app-bar-title>
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

      <div>LangageSwitcher</div>

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
    </v-app-bar>

    <NuxtPage />
  </v-app>
</template>

<style scoped lang="scss">
@import "vuetify/styles";

/* @import url("https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@600&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap");
*/

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
