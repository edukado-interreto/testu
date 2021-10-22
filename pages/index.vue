<template>
  <div>
    <v-navigation-drawer
      app
      clipped
      right
      bottom
      disable-resize-watcher
      v-model="edit_drawer.show"
      width="45vw"
    >
      <v-list-item v-if="!$vuetify.breakpoint.mobile">
        <v-btn @click.stop="edit_drawer.show = false" icon><v-icon>mdi-chevron-right</v-icon></v-btn>
      </v-list-item>
      <v-container>
        <v-textarea
          v-model="sheet[0].code"
          auto-grow
        ></v-textarea>
      </v-container>
    </v-navigation-drawer>
    <v-container>
      <v-sheet v-for="(section, i) in sheet" class="mb-6" elevation="0" rounded>
          <v-row no-gutters class="mb-1">
            <v-col class="flex-grow-0 me-4">
              <v-btn
                x-small depressed style="height:100%;"
                @click="edit_drawer.show = true"
              ><v-icon small>mdi-pencil</v-icon></v-btn>
            </v-col>
            <v-col>
              <span class="headline"> 
                {{ i+1 }}. {{ section.title }}
                <span v-if="section.title === ''" class="font-italic">
                  (no title)
                </span>
              </span>
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col class="flex-grow-0 me-4">
              <v-btn
                x-small depressed style="height:100%;"
                @click="edit_drawer.show = true"
              ><v-icon small>mdi-pencil</v-icon></v-btn>
            </v-col>
            <v-col>
              <GapsEditor
                v-if="section.type == 'gapFilling'"
                :code="section.code"
              />
            </v-col>
          </v-row>
        <!--
        <v-card-actions>
          <v-spacer />
          <v-btn @click="edit_drawer.show = true">Edit</v-btn>
          <v-btn
            color="primary"
            nuxt
            to="/inspire"
          >
            Next
          </v-btn>
        </v-card-actions>
        -->
      </v-sheet>

      <v-btn
        color="primary"
        rounded
        @click="sheet.push({ type: 'gapFilling', code: 'Example [phrase|fraze].\n\nAnother [one|ones].', title: '' })"
      >
        <v-icon class="me-2">mdi-plus</v-icon>
        Add
      </v-btn>

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
  data: () => ({
    edit_drawer: {
      mini: false,
      show: false
    },
    sheet: [
      {
        type: "gapFilling",
        title: "Fill in the gaps",
        code: "To [be|is] or not to be, [that|those] is the question\n\nThe dog [has|is|gives] eaten [its|it's] food"
      },
      {
        type: "gapFilling",
        title: "Another time",
        code: "The [book|bok|buuk|boock] is on the [table|teble|thable]\n\n[|The] Jupiter and [the|] Earth are planets.\n\nLorem [ipsum|!@#] dolor sit amet."
      }
    ]
  })
}
</script>
