<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant="miniVariant"
      fixed
      app
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      fixed
      app
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-btn
        v-if="false"
        icon
        @click.stop="miniVariant = !miniVariant"
      >
        <v-icon>mdi-{{ `chevron-${miniVariant ? 'right' : 'left'}` }}</v-icon>
      </v-btn>
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <v-btn
        icon
        disabled
      >
        <v-icon>mdi-account</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
    <v-footer
      app
    >
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>

    <v-sheet
      style="position: fixed; bottom: 0; width: 100%; z-index: 6;"
      elevation="5"
    >
      <v-toolbar dense>
        <v-toolbar-title>Item editor</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="bottomDrawer = !bottomDrawer">
          <v-icon :class="{ rotated: bottomDrawer }">mdi-chevron-up</v-icon>
        </v-btn>

      </v-toolbar>

      <v-expand-transition>
        <v-card
          tile
          style="height:30vh; overflow:auto;"
          v-if="bottomDrawer"
        >
          <v-card-text>
            <p> Sit quia dolorum obcaecati nam repudiandae Quibusdam ea possimus animi dicta aspernatur! Mollitia assumenda dicta possimus at reiciendis Nam deserunt cupiditate odit non atque blanditiis Fugiat distinctio excepturi optio cupiditate harum? Officiis aspernatur </p>
          </v-card-text>
        </v-card>
      </v-expand-transition>

    </v-sheet>

  </v-app>
</template>

<script>
export default {
  data () {
    return {
      bottomDrawer: true,
      drawer: false,
      items: [
        {
          icon: 'mdi-apps',
          title: 'Welcome',
          to: '/'
        },
        {
          icon: 'mdi-chart-bubble',
          title: 'Inspire',
          to: '/inspire'
        }
      ],
      miniVariant: false,
      rightDrawer: false,
      title: 'testu.eu'
    }
  }
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
