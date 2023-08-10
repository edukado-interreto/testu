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
                @click="edit(current.index - 1)"
                :disabled="current.index == 0"
                icon
              >
                <v-icon>mdi-chevron-up</v-icon>
              </v-btn>
            </template>
            <span>{{ $t("sheet_editor.edit_previous") }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                @click="edit(current.index + 1)"
                :disabled="current.index == sheet.length - 1"
                icon
              >
                <v-icon>mdi-chevron-down</v-icon>
              </v-btn>
            </template>
            <span>{{ $t("sheet_editor.edit_next") }}</span>
          </v-tooltip>

          <v-divider vertical class="mx-2"></v-divider>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn v-bind="attrs" v-on="on" @click="remove" icon>
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
            <span>{{ $t("sheet_editor.delete") }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                @click="move(-1)"
                :disabled="current.index == 0"
                icon
              >
                <v-icon>mdi-transfer-up</v-icon>
              </v-btn>
            </template>
            <span>{{ $t("sheet_editor.move_up") }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                @click="move(+1)"
                :disabled="current.index == sheet.length - 1"
                icon
              >
                <v-icon>mdi-transfer-down</v-icon>
              </v-btn>
            </template>
            <span>{{ $t("sheet_editor.move_down") }}</span>
          </v-tooltip>

          <v-spacer></v-spacer>

          <v-tooltip left>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                @click="edit_drawer.show = false"
                icon
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </template>
            <span>{{ $t("sheet_editor.close") }}</span>
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
          :label="$t('sheet_editor.title')"
          outlined
        ></v-text-field>
        <v-textarea
          v-model="current.data.description"
          ref="unit_description"
          rows="1"
          auto-grow
          :label="$t('editor.description')"
          outlined
          :loading="description_loading"
        >
          <template v-slot:append>
            <v-menu offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-icon
                  v-bind="attrs"
                  v-on="on"
                  :disabled="description_loading"
                >
                  mdi-dots-vertical
                </v-icon>
              </template>
              <v-list>
                <InsertMedia
                  v-slot="s"
                  type="image"
                  @load_start="description_loading = true"
                  @load_end="description_loading = false"
                  :input_el="
                    $refs.unit_description
                      ? [$refs.unit_description.$refs, 'input']
                      : null
                  "
                  :model="current ? [current.data, 'description'] : null"
                >
                  <v-list-item @click="s.click">
                    <v-list-item-icon>
                      <v-icon>mdi-image</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>
                      {{ $t("sheet_editor.insert_image") }}
                    </v-list-item-title>
                  </v-list-item>
                </InsertMedia>
                <InsertMedia
                  v-slot="s"
                  type="audio"
                  @load_start="description_loading = true"
                  @load_end="description_loading = false"
                  :input_el="
                    $refs.unit_description
                      ? [$refs.unit_description.$refs, 'input']
                      : null
                  "
                  :model="current ? [current.data, 'description'] : null"
                >
                  <v-list-item @click="s.click">
                    <v-list-item-icon>
                      <v-icon>mdi-volume-high</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>
                      {{ $t("sheet_editor.insert_sound") }}
                    </v-list-item-title>
                  </v-list-item>
                </InsertMedia>
                <v-list-item v-if="false">
                  <v-list-item-icon>
                    <v-icon>mdi-movie</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>
                    {{ $t("sheet_editor.insert_video") }}
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
              <v-btn v-bind="attrs" v-on="on" icon @click="append_new_sentence">
                <v-icon>mdi-playlist-plus</v-icon>
              </v-btn>
            </template>
            <span>{{ $t("sheet_editor.add_sentence") }}</span>
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
            <span>{{ $t("sheet_editor.insert_gap") }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                icon
                @click="add_pair_dialog = true"
                :disabled="current.data.type != 'pairing'"
              >
                <v-icon>mdi-code-equal</v-icon>
              </v-btn>
            </template>
            <span>{{ $t("sheet_editor.add_matching_pair") }}</span>
          </v-tooltip>
          <v-dialog v-model="add_pair_dialog" max-width="750">
            <v-card>
              <v-form
                ref="add_pair_form"
                lazy-validation
                @submit.prevent="add_pair_insert_click"
              >
                <v-card-title>
                  {{ $t("sheet_editor.new_matching_pair") }}
                </v-card-title>
                <v-card-text>
                  <v-text-field
                    v-model="add_pair_first_item"
                    autofocus
                    :label="$t('sheet_editor.first_item')"
                    :rules="[(val) => (!val ? 'Please type some text' : true)]"
                  ></v-text-field>
                  <v-text-field
                    v-model="add_pair_second_item"
                    :label="$t('sheet_editor.second_item')"
                    :rules="[(val) => (!val ? 'Please type some text' : true)]"
                  ></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" type="submit">
                    {{ $t("sheet_editor.insert_pair") }}
                  </v-btn>
                  <v-btn text @click="add_pair_dialog = false">
                    {{ $t("main.cancel") }}
                  </v-btn>
                </v-card-actions>
              </v-form>
            </v-card>
          </v-dialog>

          <v-divider vertical inset class="mx-2"></v-divider>

          <InsertMedia
            v-slot="s"
            type="image"
            @load_start="image_uploading = true"
            @load_end="image_uploading = false"
            :input_el="$refs.textarea ? [$refs.textarea.$refs, 'input'] : null"
            :model="[this.current.data, 'code']"
          >
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  v-bind="attrs"
                  v-on="on"
                  icon
                  @click="s.click"
                  :disabled="current.data.type != 'pairing'"
                  :loading="image_uploading"
                >
                  <v-icon>mdi-image</v-icon>
                </v-btn>
              </template>
              <span>{{ $t("sheet_editor.insert_image") }}</span>
            </v-tooltip>
          </InsertMedia>

          <InsertMedia
            v-slot="s"
            type="audio"
            @load_start="audio_uploading = true"
            @load_end="audio_uploading = false"
            :input_el="$refs.textarea ? [$refs.textarea.$refs, 'input'] : null"
            :model="[this.current.data, 'code']"
          >
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  v-bind="attrs"
                  v-on="on"
                  icon
                  @click="s.click"
                  :disabled="current.data.type != 'pairing'"
                  :loading="audio_uploading"
                >
                  <v-icon>mdi-volume-high</v-icon>
                </v-btn>
              </template>
              <span>{{ $t("sheet_editor.sound") }}</span>
            </v-tooltip>
          </InsertMedia>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                icon
                @click="insert_video_dialog = true"
                :disabled="current.data.type != 'pairing'"
              >
                <v-icon>mdi-movie</v-icon>
              </v-btn>
            </template>
            <span>{{ $t("sheet_editor.insert_video") }}</span>
          </v-tooltip>

          <v-dialog v-model="insert_video_dialog" max-width="750">
            <v-card>
              <v-form
                lazy-validation
                @submit.prevent="insert_video_insert_click"
                ref="insert_video_form"
              >
                <v-card-title>
                  {{ $t("sheet_editor.insert_video") }}
                </v-card-title>
                <v-card-text>
                  <v-text-field
                    v-model="insert_video_url"
                    autofocus
                    label="Video URL"
                    :rules="[
                      (val) =>
                        /^https?:/i.test(val)
                          ? true
                          : $t('sheet_editor.valid_url'),
                    ]"
                  ></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" type="submit">
                    {{ $t("sheet_editor.insert_video") }}
                  </v-btn>
                  <v-btn text @click="insert_video_dialog = false">
                    {{ $t("main.cancel") }}
                  </v-btn>
                </v-card-actions>
              </v-form>
            </v-card>
          </v-dialog>

          <v-dialog v-model="add_gap_dialog" max-width="750">
            <v-card>
              <v-form ref="new_gap_form">
                <v-card-title>{{ $t("sheet_editor.new_gap") }}</v-card-title>
                <v-card-text>
                  <OptionsSelector
                    v-model="new_gap_options"
                    firstchecked
                    :rules="[
                      (val) =>
                        val.length === 0
                          ? 'Please insert at least one option'
                          : true,
                    ]"
                    autofocus
                  ></OptionsSelector>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" @click="insert_gap_click">
                    {{ $t("sheet_editor.insert_gap") }}
                  </v-btn>
                  <v-btn text @click="add_gap_dialog_show(false)">
                    {{ $t("main.cancel") }}
                  </v-btn>
                </v-card-actions>
              </v-form>
            </v-card>
          </v-dialog>
        </v-toolbar>
        <v-textarea
          :placeholder="$t('sheet_editor.start_typing')"
          ref="textarea"
          v-model="current.data.code"
          auto-grow
          outlined
          hide-details="auto"
          class="code rounded-t-0 rounded-b-md"
        ></v-textarea>

        <v-switch
          v-model="current.data.shuffle"
          :disabled="current.data.type === 'open_answer'"
          :label="$t('sheet_editor.shuffle_options')"
          prepend-icon="mdi-shuffle"
          class="mt-6 mb-0"
        ></v-switch>

        <v-switch
          v-model="current.data.ignore_case"
          :disabled="current.data.type !== 'open_answer'"
          :label="$t('sheet_editor.ignore_case')"
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
        <div class="text--disabled text-h6">
          {{ $t("sheet_editor.empty_exercise") }}
        </div>
        <span class="text--disabled">
          {{ $t("sheet_editor.add_unit_to_begin") }}
        </span>
      </div>

      <v-slide-y-transition group>
        <div v-for="(section, i) in sheet" :key="keyed(sheet, i)">
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
              <v-col class="flex-grow-0">
                <v-btn
                  x-small
                  depressed
                  @click="
                    i != current.index ? edit(i) : (edit_drawer.show = false)
                  "
                  :color="i != current.index ? undefined : 'primary'"
                  style="height: 100%; border-radius: 4px 0 0 4px"
                >
                  <v-icon small>
                    {{ i != current.index ? "mdi-pencil" : "mdi-check-bold" }}
                  </v-icon>
                </v-btn>
              </v-col>
              <v-col class="ms-4">
                <div class="headline my-4">
                  {{ i + 1 }}. {{ section.title }}
                  <span v-if="section.title === ''" class="font-italic">
                    {{ $t("sheet_editor.untitled_unit") }}
                  </span>
                </div>
                <div v-if="section.description" class="body-2 mb-4 pre-line">
                  <RichContent :text="section.description"></RichContent>
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
          </v-sheet>
        </div>
      </v-slide-y-transition>

      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn class="mt-3" :elevation="0" v-bind="attrs" v-on="on">
            <v-icon class="me-2">mdi-plus</v-icon>
            {{ $t("sheet_editor.add_unit") }}
          </v-btn>
        </template>
        <v-list>
          <v-list-item
            v-for="(item, index) in snippets"
            :key="index"
            @click="add(item.unit)"
          >
            <v-list-item-icon>
              <v-img
                width="80"
                height="60"
                contain
                :src="require(`@/assets/snippet_thumb/${item.img}`)"
              >
                <template #placeholder>
                  <v-sheet class="grey lighten-3" height="60"></v-sheet>
                </template>
              </v-img>
            </v-list-item-icon>
            <v-list-item-title>{{ item.name }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-container>
  </div>
</template>
<script>
import { nanoid } from "nanoid"
import unit_component from "~/mixins/unit_component.js"
export default {
  name: "SheetEditor",
  mixins: [unit_component],
  props: ["sheet"],
  data: () => ({
    new_gap_options: [],
    add_gap_dialog: false,

    add_pair_dialog: false,
    add_pair_first_item: "",
    add_pair_second_item: "",

    insert_video_dialog: false,
    insert_video_url: "",

    description_loading: false,

    image_uploading: false,
    audio_uploading: false,

    edit_drawer: {
      show: false,
    },
    current: {
      index: undefined,
      data: {},
    },
  }),
  computed: {
    available_types() {
      return [
        { value: "default", text: this.$t("sheet_editor.types.default") },
        {
          value: "open_answer",
          text: this.$t("sheet_editor.types.open_answer"),
        },
        {
          value: "multiple_choice",
          text: this.$t("sheet_editor.types.multiple_choice"),
        },
        { value: "pairing", text: this.$t("sheet_editor.types.pairing") },
      ]
    },
    snippets() {
      return [
        {
          name: this.$t("sheet_editor.snippets.blank_unit.name"),
          img: "blank.svg",
          unit: {
            type: "default",
            code: "",
          },
        },
        {
          name: this.$t("sheet_editor.snippets.gap_filling_dropdown.name"),
          img: "fill_gap_dropdown.svg",
          unit: {
            type: "default",
            code: this.$t("sheet_editor.snippets.gap_filling_dropdown.code"),
          },
        },
        {
          name: this.$t("sheet_editor.snippets.gap_filling_open_answer.name"),
          img: "fill_gap_open.svg",
          unit: {
            type: "open_answer",
            code: this.$t("sheet_editor.snippets.gap_filling_open_answer.code"),
          },
        },
        {
          name: this.$t("sheet_editor.snippets.multiple_choice.name"),
          img: "choice.svg",
          unit: {
            type: "multiple_choice",
            code: this.$t("sheet_editor.snippets.multiple_choice.code"),
          },
        },
        {
          name: this.$t("sheet_editor.snippets.pairing_text_with_text.name"),
          img: "match_text.svg",
          unit: {
            type: "pairing",
            code: this.$t("sheet_editor.snippets.pairing_text_with_text.code"),
          },
        },
        {
          name: this.$t(
            "sheet_editor.snippets.pairing_text_with_pictures.name",
          ),
          img: "match_pic.svg",
          unit: {
            type: "pairing",
            code: this.$t(
              "sheet_editor.snippets.pairing_text_with_pictures.code",
            ),
          },
        },
        {
          name: this.$t("sheet_editor.snippets.sorting_pictures.name"),
          img: "sort_pic.svg",
          unit: {
            type: "pairing",
            code: this.$t("sheet_editor.snippets.sorting_pictures.code"),
            shuffle: true,
          },
        },
        {
          name: this.$t(
            "sheet_editor.snippets.pairing_pictures_with_sounds.name",
          ),
          img: "match_pic_sound.svg",
          unit: {
            type: "pairing",
            code: this.$t(
              "sheet_editor.snippets.pairing_pictures_with_sounds.code",
            ),
          },
        },
        {
          name: this.$t(
            "sheet_editor.snippets.questions_about_a_picture_true_or_false.name",
          ),
          img: "true_false_pic.svg",
          unit: {
            type: "multiple_choice",
            description: this.$t(
              "sheet_editor.snippets.questions_about_a_picture_true_or_false.description",
            ),
            code: this.$t(
              "sheet_editor.snippets.questions_about_a_picture_true_or_false.code",
            ),
          },
        },
        {
          name: this.$t(
            "sheet_editor.snippets.questions_about_a_text_multiple_choice.name",
          ),
          img: "choice_paragraph.svg",
          unit: {
            type: "multiple_choice",
            description: this.$t(
              "sheet_editor.snippets.questions_about_a_text_multiple_choice.description",
            ),
            code: this.$t(
              "sheet_editor.snippets.questions_about_a_text_multiple_choice.code",
            ),
          },
        },
        {
          name: this.$t(
            "sheet_editor.snippets.questions_about_a_video_open_answer.name",
          ),
          img: "open_video.svg",
          unit: {
            type: "open_answer",
            description: this.$t(
              "sheet_editor.snippets.questions_about_a_video_open_answer.description",
            ),
            code: this.$t(
              "sheet_editor.snippets.questions_about_a_video_open_answer.code",
            ),
          },
        },
        {
          name: this.$t(
            "sheet_editor.snippets.questions_about_a_sound_dropdown.name",
          ),
          img: "dropdown_sound.svg",
          unit: {
            type: "multiple_choice",
            description: this.$t(
              "sheet_editor.snippets.questions_about_a_sound_dropdown.description",
            ),
            code: this.$t(
              "sheet_editor.snippets.questions_about_a_sound_dropdown.code",
            ),
          },
        },
      ]
    },
  },
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
      return window.requestAnimationFrame(() => window.requestAnimationFrame(f))
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
      const new_gap =
        "[" +
        this.new_gap_options
          .map((opt) => (opt.right ? "+" + opt.value : opt.value))
          .join("|") +
        "]"

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

      code += `${this.add_pair_first_item} == ${this.add_pair_second_item}`

      this.current.data.code = code

      requestAnimationFrame(() => {
        input.selectionStart = this.current.data.code.length
        input.focus()
      })

      this.add_pair_dialog = false
    },
    insert_video_insert_click() {
      if (!this.$refs.insert_video_form.validate()) return
      this.inject_snippet(`{video:${this.insert_video_url}}`)
      this.insert_video_dialog = false
    },
    inject_snippet(snippet) {
      // insert in the current code a snippet at the
      // current cursor position, move the cursor
      // after the snippet and focus the textarea
      const input = this.$refs.textarea.$refs.input
      const start = input.selectionStart
      const code = this.current.data.code
      this.current.data.code =
        code.slice(0, input.selectionStart) +
        snippet +
        code.slice(input.selectionEnd)
      requestAnimationFrame(() => {
        input.selectionStart = start + snippet.length
        input.selectionEnd = start + snippet.length
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
      this.edit(Math.min(this.current.index, this.sheet.length - 1))
    },
    edit(i) {
      this.current.index = i
      this.edit_drawer.show = true
      this.current.data = this.sheet[i]
      this.$nextTick(function () {
        // scroll to the currently edited section
        this.$vuetify.goTo(
          this.$refs[`section-${this.keyed(this.sheet, i)}`][0],
          { offset: 15 },
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
    add(unit) {
      const base_unit = {
        type: "default",
        title: "",
        code: "",
      }
      this.sheet.push({
        ...base_unit,
        ...unit,
      })
      this.edit(this.sheet.length - 1)
    },
  },
  watch: {
    add_gap_dialog: function (val) {
      if (val) {
        this.new_gap_options = []
      } else {
        requestAnimationFrame(() => {
          this.$refs.textarea.focus()
        })
      }
    },
    add_pair_dialog: function (val) {
      if (val) {
        this.add_pair_first_item = ""
        this.add_pair_second_item = ""
      } else {
        this.$refs.add_pair_form.resetValidation()
        requestAnimationFrame(() => {
          this.$refs.textarea.focus()
        })
      }
    },
    insert_video_dialog: function (val) {
      if (val) {
        this.insert_video_url = ""
      } else {
        this.$refs.insert_video_form.resetValidation()
        requestAnimationFrame(() => {
          this.$refs.textarea.focus()
        })
      }
    },
    "edit_drawer.show": function (val) {
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
  },
}
</script>
<style scoped>
.pre-line {
  white-space: pre-line;
}
.code {
  font-family: monospace;
}
</style>
