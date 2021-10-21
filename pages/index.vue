<template>
  <div>
    <v-navigation-drawer
      app
      right
      bottom
      clipped
      v-model="drawer"
      :mini-variant.sync="mini"
      disable-resize-watcher
      disable-route-watcher
    >
      <v-list-item dense v-if="!$vuetify.breakpoint.mobile">
        <v-btn @click.stop="mini = !mini" icon><v-icon>mdi-chevron-{{ mini ? 'left' : 'right' }}</v-icon></v-btn>
      </v-list-item>
      <v-container v-show="!mini">
        <v-textarea
          v-model="code"
          auto-grow
        ></v-textarea>
      </v-container>
    </v-navigation-drawer>
    <v-container>
      <v-card>
        <v-card-title class="headline">
          {{ title }}
        </v-card-title>
        <v-card-text>
          <GapsEditor :code="code" />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="primary"
            nuxt
            to="/inspire"
          >
            Next
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </div>
</template>
<script>
export default {
  name: 'Index',
  head() {
    return {
      title: 'Home page'
    }
  },
  methods: {
  },
  data: () => ({
    mini: false,
    drawer: true,
    title: "Fill in the gaps",
    code: "To [be|is] or not to be, [that|those] is the question\n\nThe dog [has|is|gives] eaten [its|it's] food",
    sheet: [
      {
        type: "gapFilling",
        title: "Fill in the gaps",
        code: "To [be|is] or not to be, [that|those] is the question\n\nThe dog [has|is|gives] eaten [its|it's] food"
      }
    ]
  })
}
</script>
