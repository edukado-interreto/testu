<template>
  <v-app id="inspire">
    <v-app-bar
      app
      clipped-right
      height="72"
      flat
    >
      <v-app-bar-nav-icon @click.stop="nav_drawer.show = !nav_drawer.show" />
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <v-btn
        icon
        disabled
      >
        <v-icon>mdi-account</v-icon>
      </v-btn>
    </v-app-bar>
    <v-navigation-drawer
      v-model="nav_drawer.show"
      app
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in nav_drawer.items"
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
  </v-app>
</template>

<script>
export default {
  data () {
    return {
      nav_drawer: {
        show: null,
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
      },
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
