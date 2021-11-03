<template>
  <v-combobox
    ref="combobox"
    multiple
    chips
    @keydown="keydown"
    @input="input_is_blank = true"
    v-model="optionsModel"
    :hint="hint"
    placeholder="Start typing an option..."
    :append-icon="null"
    :label="label"
    :autofocus="autofocus"
    :rules="rules"
    validate-on-blur
  >
    <template v-slot:append-outer>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <div v-on="on">
            <v-btn
              :disabled="input_is_blank"
              class="rounded-l-xl rounded-r-0"
              @click="insert_option"
            >
              <v-icon small>mdi-plus</v-icon>
              <v-icon small>mdi-text-short</v-icon>
            </v-btn>
          </div>
        </template>
        <span>Add option (Tab)</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <div v-on="on">
            <v-btn
              :disabled="!input_is_blank || optionsModel.includes('\0')"
              class="rounded-l-0 rounded-r-xl"
              @click="insert_blank"
            >
              <v-icon small>mdi-plus</v-icon>
              <v-icon small>mdi-selection</v-icon>
            </v-btn>
          </div>
        </template>
        <span>Add the "leave blank" option (Ctrl+Space)</span>
      </v-tooltip>
    </template>
    <template v-slot:selection="data">
      <v-chip
        :key="JSON.stringify(data.item)"
        v-bind="data.attrs"
        :input-value="data.selected"
        :disabled="data.disabled"
        @click:close="data.parent.selectItem(data.item)"
      >
        <v-switch
          v-model="checkedModel"
          :value="data.item"
          dense
        >
          <template v-slot:label></template>
        </v-switch>
        <v-icon small v-if="data.item === '\0'">mdi-selection</v-icon>
        <template v-else>{{ data.item }}</template>
      </v-chip>
    </template>
  </v-combobox>
</template>
<script>
export default {
  props: ['value', 'label', 'autofocus', 'rules', 'firstchecked'],
  data: () => ({
    checkedModel: [],
    optionsModel: [],
    input_is_blank: true,
  }),
  computed: {
    hint() {
      if (this.optionsModel.length == 0) return ""
      let rights = 0
      let wrongs = 0
      this.value.forEach(function(opt) {
        if (opt.right) rights++
        else wrongs++
      })
      let txt = ""
      if (rights) txt += `${rights} right ${(rights != 1) ? 'options' : 'option'}`
      if (rights && wrongs) txt += ", "
      if (wrongs) txt += `${wrongs} wrong ${(wrongs != 1) ? 'options' : 'option'}`
      txt += ". Toggle the switches to change the options' rightness."
      return txt
    }
  },
  mounted() {
    this.$refs.combobox.$refs.input.addEventListener(
      'input',
      (e) => {
        this.input_is_blank = e.target.value === ''
      }
    )
  },
  methods: {
    insert_option() {
      this.$refs.combobox.blur()
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          this.$refs.combobox.focus()
        })
      })
    },
    insert_blank() {
      this.$refs.combobox.blur()
      this.optionsModel = [...this.optionsModel, '\0']
      setTimeout(() => {
        // for some reasons even the double requestAnimationFrame
        // is not always doing its job here (Chrome)
        this.$refs.combobox.focus()
      }, 250)
    },
    keydown(e) {
      // append an empty string to the model on Ctrl+Enter

      if (!e.ctrlKey) return
      if (e.code != 'Space') return

      if (e.path[0].value !== "") return
      // input field is not empty, abort
      
      if ((this.optionsModel||[]).includes('\0')) return
      // empty string is already present, abort

      if (!this.optionsModel) this.optionsModel = []
      // create the array if its value is falsy

      this.optionsModel = [...this.optionsModel, '\0']
      // append the value, push() seems to be unreactive here
    },
    updateData(k, val) {
      // update a data attribute only if its value differs
      // from the one we want to set. This is useful to
      // avoid triggering a watcher, specifically when that
      // leads to infinite loops
      if (JSON.stringify(this[k]) == JSON.stringify(val)) return
      this[k] = val
    }
  },
  watch: {
    optionsModel(val) {

      if (this.firstchecked !== undefined) {
        // automatically set the first item as
        // checked (i.e. right) when entered
        if (
          (this.optionsModel.length == 1)
          && (this.checkedModel.length == 0)
        ) {
          this.checkedModel.push(
            this.optionsModel[0]
          )
        }
      }

      this.$emit(
        'input',
        val.map(e => ({
          value: e,
          right: this.checkedModel.includes(e)
        }))
      )

    },
    checkedModel(val) {
      this.$emit(
        'input',
        this.optionsModel.map(e => ({
          value: e,
          right: val.includes(e)
        }))
      )
    },
    value: {
      handler(val) {
        this.updateData('optionsModel', val.map(e => e.value))
        this.updateData('checkedModel', val.filter(e => e.right).map(e => e.value))
      },
      deep: true,
      immediate: true
    }
  }
}
</script>
