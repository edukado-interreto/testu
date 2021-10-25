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
        <v-text-field
          v-model="current.title"
          label="Title"
          @input="update('title')"
          outlined
        ></v-text-field>
        <v-textarea
          v-model="current.description"
          rows="1"
          auto-grow
          label="Description"
          @input="update('description')"
          outlined
        ></v-textarea>
        <v-textarea
          v-model="current.code"
          label="Content"
          @input="update('code')"
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
      show: false
    },
    current: {
      index: undefined,
      title: '',
      code: '',
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
  }),
  methods: {
    edit(i) {
      this.current.index = i
      this.edit_drawer.show = true
      this.$nextTick(function() {
        this.$vuetify.goTo(
          this.$refs.sheet[i],
          { offset: 15 }
        )
      })
      this.current.title = this.sheet[i].title
      this.current.description = this.sheet[i].description
      this.current.code = this.sheet[i].code
    },
    add(type) {
      this.sheet.push({
        type: 'gapFilling',
        title: '',
        code: 'Example [phrase|fraze].\n\nAnother [one|ones].',
      })
      this.edit(this.sheet.length - 1)
    },
    update(node) {
      this.$set(this.sheet[this.current.index], node, this.current[node])
      /*
      if (node === 'code') {
        this.$set(this.sheet[this.current.index], 'code', this.current.code)
      }
      */
    }
  },
  watch: {
    'edit_drawer.show': function(val) {
      if (val === false) {
        this.current.index = undefined
      }
    }
  }
}
</script>
<style scoped>
  .pre-line { white-space: pre-line; }
</style>
