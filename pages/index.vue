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
      <v-toolbar dense flat>
        <v-btn @click="move(-1)" :disabled="current.index == 0" icon><v-icon>mdi-arrow-up</v-icon></v-btn>
        <v-btn @click="move(+1)" :disabled="current.index == sheet.length-1" icon><v-icon>mdi-arrow-down</v-icon></v-btn>
        <v-btn @click="remove" icon><v-icon>mdi-delete</v-icon></v-btn>
      </v-toolbar>
      <v-container class="mt-2">
        <v-text-field
          v-model="current.data.title"
          label="Title"
          outlined
        ></v-text-field>
        <v-textarea
          v-model="current.data.description"
          rows="1"
          auto-grow
          label="Description"
          outlined
        ></v-textarea>
        <v-textarea
          v-model="current.data.code"
          label="Content"
          auto-grow
          outlined
        ></v-textarea>
      </v-container>
    </v-navigation-drawer>
    <v-container>
      <v-sheet
        v-for="(section, i) in sheet"
        :elevation="i == current.index ? 8 : 0"
        ref="sheet"
        class="mb-6 transition-swing"
        rounded
      >
        <v-row no-gutters>
          <v-col
            class="flex-grow-0"
          >
              <v-btn
                x-small
                depressed
                @click="(i != current.index) ? edit(i) : (edit_drawer.show = false)"
                :color="(i != current.index) ? undefined : 'primary'"
                style="height: 100%; border-radius: 4px 0 0 4px;"
              >
                <v-icon small>
                  {{ (i != current.index) ? 'mdi-pencil' : 'mdi-check-bold' }}
                </v-icon>
              </v-btn>
          </v-col>
          <v-col class="ms-4">
            <div class="headline my-4"> 
              {{ i+1 }}. {{ section.title }}
              <span v-if="section.title === ''" class="font-italic">
                (no title)
              </span>
            </div>
            <div
              v-if="section.description"
              class="body-2 mb-4 pre-line"
            >{{ section.description }}</div>
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
        @click="add('gapFilling')"
        class="mt-3"
      >
        <v-icon class="me-2">mdi-plus</v-icon>
        Gap filling
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
      show: false
    },
    current: {
      index: undefined,
      data: {},
    },
    sheet: [],
    /*
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
    */
  }),
  methods: {
    move(offset) {
      const from = this.current.index
      const to = from + offset
      this.sheet[from] = this.sheet.splice(to, 1, this.sheet[from])[0]
      // swap array[from] with array[to]
      this.edit(to)
    },
    remove() {
      this.sheet.splice(this.current.index, 1)
      if (this.sheet.length === 0) {
        this.edit_drawer.show = false
        return
      }
      this.edit(
        Math.min(
          this.current.index,
          this.sheet.length - 1
        )
      )
    },
    edit(i) {
      this.current.index = i
      this.edit_drawer.show = true
      this.$nextTick(function() {
        this.$vuetify.goTo(
          this.$refs.sheet[i],
          { offset: 15 }
        )
      })
      this.current.data = this.sheet[i]
    },
    add(type) {
      this.sheet.push({
        type: 'gapFilling',
        title: '',
        code: 'This is an [example|eksample] phrase.\n\n[This|These] is another one.',
      })
      this.edit(this.sheet.length - 1)
    },
  },
  watch: {
    'edit_drawer.show': function(val) {
      if (val === false) {
        this.current.index = undefined
      }
    },
    'current.data': {
      handler: function() {
        this.$set(
          this.sheet,
          this.current.index,
          this.current.data
        )
      },
      deep: true
    }
  }
}
</script>
<style scoped>
  .pre-line { white-space: pre-line; }
</style>
