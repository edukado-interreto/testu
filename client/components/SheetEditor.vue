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
      <template v-slot:prepend>
        <v-toolbar dense flat>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                @click="edit(current.index-1)"
                :disabled="current.index == 0"
                icon
              ><v-icon>mdi-chevron-up</v-icon>
              </v-btn>
            </template>
            <span>Edit previous</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                @click="edit(current.index+1)"
                :disabled="current.index == sheet.length-1"
                icon
              ><v-icon>mdi-chevron-down</v-icon></v-btn>
            </template>
            <span>Edit next</span>
          </v-tooltip>

          <v-divider vertical class="mx-2"></v-divider>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                @click="remove"
                icon><v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
            <span>Delete</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                @click="move(-1)"
                :disabled="current.index == 0"
                icon
              ><v-icon>mdi-transfer-up</v-icon></v-btn>
            </template>
            <span>Move up</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                @click="move(+1)"
                :disabled="current.index == sheet.length-1"
                icon
              ><v-icon>mdi-transfer-down</v-icon></v-btn>
            </template>
            <span>Move down</span>
          </v-tooltip>

          <v-spacer></v-spacer>

          <v-tooltip left>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                @click="edit_drawer.show = false"
                icon
              ><v-icon>mdi-close</v-icon></v-btn>
            </template>
            <span>Close editor</span>
          </v-tooltip>

        </v-toolbar>
      </template>
      <v-container class="mt-2">
        <v-select
          outlined
          dense
          label="Type"
          :items="available_types"
          v-model="current.data.type"
        ></v-select>
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
        >
          <template v-slot:append>
            <v-menu offset-y>
              <template v-slot:activator="{on, attrs}">
                <v-icon v-bind="attrs" v-on="on">mdi-dots-vertical</v-icon>
              </template>
              <v-list>
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon>mdi-image</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>
                    Insert image
                  </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon>mdi-volume-high</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>
                    Insert sound
                  </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-list-item-icon>
                    <v-icon>mdi-movie</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>
                    Insert video
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
        </v-textarea>
        <v-toolbar
          dense
          flat
          color="grey lighten-4"
          class="rounded-b-0 rounded-t-lg"
        >

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                icon
                @click="append_new_sentence"
              >
                <v-icon>mdi-playlist-plus</v-icon>
              </v-btn>
            </template>
            <span>Add sentence</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                icon
                @click.stop="add_gap_dialog_show(true)"
                :disabled="current.data.type == 'pairing'"
              >
                <v-icon>mdi-tray-plus</v-icon>
              </v-btn>
            </template>
            <span>Insert gap</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                icon
                @click="add_pair_dialog=true"
                :disabled="current.data.type != 'pairing'"
              >
                <v-icon>mdi-code-equal</v-icon>
              </v-btn>
            </template>
            <span>Add matching pair</span>
          </v-tooltip>
          <v-dialog
            v-model="add_pair_dialog"
            max-width="750"
          >
            <v-card>
              <v-form
                ref="add_pair_form"
                lazy-validation
                @submit.prevent="add_pair_insert_click"
              >
                <v-card-title>New matching pair</v-card-title>
                <v-card-text>
                  <v-text-field
                    v-model="add_pair_first_item"
                    autofocus
                    label="First item"
                    :rules="[ val => (!val) ? 'Please type some text' : true ]"
                  ></v-text-field>
                  <v-text-field
                    v-model="add_pair_second_item"
                    label="Second item"
                    :rules="[ val => (!val) ? 'Please type some text' : true ]"
                  ></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    type="submit"
                  >Insert pair</v-btn>
                  <v-btn text @click="add_pair_dialog=false">Cancel</v-btn>
                </v-card-actions>
              </v-form>
            </v-card>
          </v-dialog>

          <v-divider vertical inset class="mx-2"></v-divider>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                icon
                @click="$refs.image_uploader.click()"
                :disabled="current.data.type != 'pairing'"
                :loading="image_uploading"
              >
                <v-icon>mdi-image</v-icon>
              </v-btn>
            </template>
            <span>Insert image</span>
          </v-tooltip>
          <input
            type="file"
            class="d-none"
            ref="image_uploader"
            @change="image_uploader_onchange"
            accept="image/*"
          >

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                icon
                @click="$refs.audio_uploader.click()"
                :disabled="current.data.type != 'pairing'"
                :loading="audio_uploading"
              >
                <v-icon>mdi-volume-high</v-icon>
              </v-btn>
            </template>
            <span>Insert sound</span>
          </v-tooltip>
          <input
            type="file"
            class="d-none"
            ref="audio_uploader"
            @change="audio_uploader_onchange"
            accept="audio/*"
          >

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                icon
                @click="insert_video_dialog=true"
                :disabled="current.data.type != 'pairing'"
              >
                <v-icon>mdi-movie</v-icon>
              </v-btn>
            </template>
            <span>Insert video</span>
          </v-tooltip>

          <v-dialog
            v-model="insert_video_dialog"
            max-width="750"
          >
            <v-card>
              <v-form
                lazy-validation
                @submit.prevent="insert_video_insert_click"
                ref="insert_video_form"
              >
                <v-card-title>Insert video</v-card-title>
                <v-card-text>
                  <v-text-field
                    v-model="insert_video_url"
                    autofocus
                    label="Video URL"
                    :rules="[ val => (/^https?:/i).test(val) ? true : 'Please type a valid url' ]"
                  ></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    type="submit"
                  >Insert video</v-btn>
                  <v-btn text @click="insert_video_dialog=false">Cancel</v-btn>
                </v-card-actions>
              </v-form>
            </v-card>
          </v-dialog>

          <v-dialog
            v-model="add_gap_dialog"
            max-width="750"
          >
            <v-card>
              <v-form ref="new_gap_form">
                <v-card-title>New gap</v-card-title>
                <v-card-text>
                  <OptionsSelector
                    v-model="new_gap_options"
                    firstchecked
                    :rules="[ val => (val.length == 0) ? 'Please insert at least one option' : true ]"
                    autofocus
                  ></OptionsSelector>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    @click="insert_gap_click"
                  >Insert gap</v-btn>
                  <v-btn text @click="add_gap_dialog_show(false)">Cancel</v-btn>
                </v-card-actions>
              </v-form>
            </v-card>

          </v-dialog>

        </v-toolbar>
        <v-textarea
          placeholder="Start typing a sentence…"
          ref="textarea"
          v-model="current.data.code"
          auto-grow
          outlined
          hide-details="auto"
          class="code rounded-t-0 rounded-b-md"
        ></v-textarea>

        <v-switch
          v-model="current.data.shuffle"
          :disabled="current.data.type == 'open_answer'"
          label="Shuffle options"
          prepend-icon="mdi-shuffle"
          class="mt-6 mb-0"
        ></v-switch>

        <v-switch
          v-model="current.data.ignore_case"
          :disabled="current.data.type != 'open_answer'"
          label="Ignore case"
          prepend-icon="mdi-case-sensitive-alt"
          class="mt-0"
        ></v-switch>

      </v-container>
    </v-navigation-drawer>
    <v-container>
        <div
          class="mb-5 pa-9"
          v-if="sheet.length == 0"
          key="no_units"
          style="border: 4px dashed #e7e7e7"
        >
          <div class="text--disabled text-h6">Empty exercise</div>
          <span class="text--disabled">Add a new unit to begin</span>
        </div>

      <v-slide-y-transition group>
        <div
          v-for="(section, i) in sheet"
          :key="keyed(sheet, i)"
        >
          <!--
          The outer <div> is needed to have both the
          sliding animation when the v-sheets are moved
          (<v-slide-y-transition group>) and the fading
          animation of the v-sheet's elevation when
          toggling edit mode (.transition-swing).
          -->
          <v-sheet
            :elevation="i == current.index ? 8 : 0"
            :ref="`section-${keyed(sheet, i)}`"
            class="mb-4 transition-swing"
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
                    Untitled unit
                  </span>
                </div>
                <div
                  v-if="section.description"
                  class="body-2 mb-4 pre-line"
                >
                  <RichContent
                    :text="section.description"
                  >
                  </RichContent>
                </div>
                <component
                  :is="unit_component(section.type)"
                  :code="section.code"
                  :shuffle="section.shuffle"
                  :ignore_case="section.ignore_case"
                  ref="unit"
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
          </div>
      </v-slide-y-transition>

      <v-btn
        @click="add('default')"
        class="mt-3"
        :elevation="0"
      >
        <v-icon class="me-2">mdi-plus</v-icon>
        Add unit
      </v-btn>


    </v-container>
  </div>
</template>
<script>
import { nanoid } from 'nanoid'
import unit_component from '~/mixins/unit_component.js'
export default {
  name: 'SheetEditor',
  mixins: [
    unit_component,
  ],
  props: ['sheet'],
  data: () => ({
    available_types: [
      { text: 'Default', value: 'default' },
      { text: 'Open answer', value: 'open_answer' },
      { text: 'Multiple choice', value: 'multiple_choice' },
      { text: 'Sort and match', value: 'pairing' },
    ],
    new_gap_options: [],
    add_gap_dialog: false,

    add_pair_dialog: false,
    add_pair_first_item: '',
    add_pair_second_item: '',

    insert_video_dialog: false,
    insert_video_url: '',

    image_uploading: false,
    audio_uploading: false,

    edit_drawer: {
      show: false
    },
    current: {
      index: undefined,
      data: {},
    },
    /* sheet: [
      {
        type: "default",
        title: "Fill in the gaps",
        code: "To [be|is] or not to be, [that|those] is the question\n\nThe dog [has|is|gives] eaten [its|it's] food"
      },
      {
        type: "default",
        title: "Another time",
        code: "The [book|bok|buuk|boock] is on the [table|teble|thable]\n\n[|The] Jupiter and [the|] Earth are planets.\n\nLorem [ipsum|!@#] dolor sit amet."
      }
    ] */
  }),
  methods: {
    append_new_sentence() {
      const input = this.$refs.textarea.$refs.input
      const code = this.current.data.code.trimEnd()

      if (code !== "") {
        this.current.data.code = code + "\n\n"
      }

      requestAnimationFrame(() => {
        input.selectionStart = this.current.data.code.length
        input.focus()
      })
    },
    doubleRequestAnimationFrame(f) {
      // force the browser to re-render the DOM before
      // calling the callback function.
      // See:
      // https://github.com/vuejs/vue/issues/9200
      // https://github.com/twickstrom/vue-force-next-tick
      return window.requestAnimationFrame(
        () => window.requestAnimationFrame(
          f
        )
      )
    },
    add_gap_dialog_show(show) {
      if (show) {
        this.add_gap_dialog = true
      } else {
        this.add_gap_dialog = false
      }
    },
    insert_gap_click() {
      // Using double requestAnimationFrame will ensure that
      // the value of the OptionsSelectors is updated even
      // if the user doesn't press Enter or blurs the input.
      this.doubleRequestAnimationFrame(() => {
        if (!this.$refs.new_gap_form.validate()) return
        this.insert_gap()
      })
    },
    insert_gap() {

      // TODO:
      // ensure ltr string concatenanion
      // http://stackoverflow.com/q/29988144/
      const new_gap = "[" + this.new_gap_options.map(
        opt => opt.right ? '+'+opt.value : opt.value
      ).join("|") + "]"

      this.inject_snippet(new_gap)

      this.add_gap_dialog = false

    },
    add_pair_insert_click() {

      if (!this.$refs.add_pair_form.validate()) return

      const input = this.$refs.textarea.$refs.input
      let code = this.current.data.code.trimEnd()

      if (code !== "") {
        code += "\n\n"
      }

      code += `${this.add_pair_first_item } == ${this.add_pair_second_item}`

      this.current.data.code = code

      requestAnimationFrame(() => {
        input.selectionStart = this.current.data.code.length
        input.focus()
      })

      this.add_pair_dialog = false
    },
    insert_video_insert_click() {
      if (!this.$refs.insert_video_form.validate()) return
      this.inject_snippet(
        `{video:${this.insert_video_url}}`
      )
      this.insert_video_dialog = false
    },
    async image_uploader_onchange(e) {

      const file = e.target.files[0]
      if (!file) return

      const formData = new FormData()
      formData.append("file", file)
      formData.append("type", "image")

      this.image_uploading = true

      const resp = await fetch('/api/v1/upload/', {
        method: 'post',
        body: formData
      })

      let resp_json = null
      let error = null
      try {
        resp_json = await resp.json()
        error = resp_json.error
      } catch(e) {
        error = "Unattended server response"
      } finally {
        this.image_uploading = false
      }
      if (resp.status >= 400) {
        alert(error)
        return
      }
      //console.log({resp, resp_json})
    
      this.inject_snippet(
        `{img:${resp_json.name}}`
      )
    },
    async audio_uploader_onchange(e) {

      const file = e.target.files[0]
      if (!file) return

      const formData = new FormData()
      formData.append("file", file)
      formData.append("type", "audio")

      this.audio_uploading = true

      const resp = await fetch('/api/v1/upload/', {
        method: 'post',
        body: formData
      })

      let resp_json = null
      let error = null
      try {
        resp_json = await resp.json()
        error = resp_json.error
      } catch(e) {
        error = "Unattended server response"
      } finally {
        this.audio_uploading = false
      }
      if (resp.status >= 400) {
        alert(error)
        return
      }
      //console.log({resp, resp_json})
    
      this.inject_snippet(
        `{sound:${resp_json.name}}`
      )
    },
    inject_snippet(snippet) {
      // insert in the current code a snippet at the
      // current cursor position, move the cursor
      // after the snippet and focus the textarea
      const input = this.$refs.textarea.$refs.input
      const start = input.selectionStart
      const code = this.current.data.code
      this.current.data.code = code.slice(
        0, input.selectionStart
      ) + snippet + code.slice(
        input.selectionEnd
      )
      requestAnimationFrame(() => {
        input.selectionStart = start + snippet.length
        input.selectionEnd   = start + snippet.length
        input.focus()
      })
    },
    keyed(iterable, i) {
      if ("_key" in iterable[i]) {
        return iterable[i]._key
      }
      iterable[i]._key = nanoid()
      return iterable[i]._key
    },
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
      this.current.data = this.sheet[i]
      this.$nextTick(function() {
        // scroll to the currently edited section
        this.$vuetify.goTo(
          this.$refs[`section-${this.keyed(this.sheet, i)}`][0],
          { offset: 15 }
        )
        // Ideally we could just use this.$refs.sheet[i], since we can have
        // something like <v-sheet ref="sheet" v-for="..."> in the template.
        // Unfortunately this would break when reordering the items, because
        // "v-for refs do not guarantee the same order as your source Array"
        // (https://github.com/vuejs/vue/issues/4952#issuecomment-280661367)
        // so we are using the sections' key to build unique refs, that will
        // be arrays anyway, so then we scroll to their first and only item.
      })
    },
    add(type) {
      this.sheet.push({
        type: 'default',
        title: '',
        code: '' //This is an [example|eksample] phrase.\n\n[This|These] is another one.',
      })
      this.edit(this.sheet.length - 1)
    },
  },
  watch: {
    add_gap_dialog: function(val) {
      if (val) {
        this.new_gap_options = []
      } else {
        requestAnimationFrame(() => {
          this.$refs.textarea.focus()
        })
      }
    },
    add_pair_dialog: function(val) {
      if (val) {
        this.add_pair_first_item = ''
        this.add_pair_second_item = ''
      } else {
        this.$refs.add_pair_form.resetValidation()
        requestAnimationFrame(() => {
          this.$refs.textarea.focus()
        })
      }
    },
    insert_video_dialog: function(val) {
      if (val) {
        this.insert_video_url = ''
      } else {
        this.$refs.insert_video_form.resetValidation()
        requestAnimationFrame(() => {
          this.$refs.textarea.focus()
        })
      }
    },
    'edit_drawer.show': function(val) {
      if (val === false) {
        this.current.index = undefined
      }
    },
    //'current.data': {
    //
    //  // this watcher is not needed because when entering edit mode we assign
    //  // to this.current.data a reference to this.sheet[this.current.index],
    //  // so the changes to the former are actually performed on the latter
    //
    //  handler: function() {
    //    this.$set(
    //      this.sheet,
    //      this.current.index,
    //      this.current.data
    //    )
    //  },
    //  deep: true
    //}
  }
}
</script>
<style scoped>
  .pre-line { white-space: pre-line; }
  .code { font-family: monospace; }
</style>
