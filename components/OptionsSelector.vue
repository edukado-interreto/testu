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
    <template v-slot:append>
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn
            v-on="on"
            rounded
            text
            @click="insert_blank"
          >
            <v-icon small>mdi-plus</v-icon>
            <v-icon small>mdi-selection</v-icon>
          </v-btn>
        </template>
        <span>Add the "leave blank" option (Ctrl+Enter)</span>
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
          color="success"
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
      if (!this.input_is_blank) {
        return "Press Enter to finalize the option…"
      }
      if (this.optionsModel.length == 0) {
        return ""
      }
      return "Toggle the switches (on = right, off = wrong) or start typing a new option."
    }
  },
  mounted() {
    const combobox = this.$refs.combobox

    combobox.$refs.input.addEventListener(
      'input',
      (e) => {
        // NOTE: this may not be bulletproof

        if (combobox.$el.classList.contains(
          'v-autocomplete--is-selecting-index'
        )) {
          // when the v-combobox has the class
          // 'v-autocomplete--is-selecting-index',
          // VueJS sets the <input> (e.target) opacity
          // to 0 and read its key events so that the user
          // can traverse the chips using the arrow keys.
          // This means that the user may actually
          // type some text in it, which VueJS would
          // remove when setting back the opacity to 1.
          this.input_is_blank = true
          return
        }

        this.input_is_blank = e.target.value === ''

      }
    )
  },
  methods: {
    insert_blank() {
      // Append a '\0' to the array of options.
      // If the option is already in the array,
      // remove that one and append a new one
      this.optionsModel = [
        ...(this.optionsModel.filter(
          e => e != '\0'
        )),
        '\0'
      ]
    },
    keydown(e) {
      // append an empty string to the model on Ctrl+Enter

      if (!e.ctrlKey) return
      if (e.code != 'Enter') return
      if (!this.input_is_blank) return

      this.insert_blank()
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
        this.updateData(
          'optionsModel',
          val.map(e => e.value)
        )
        this.updateData(
          'checkedModel',
          val.filter(e => e.right).map(e => e.value)
        )
      },
      deep: true,
      immediate: true
    }
  }
}
</script>
<style>
  .v-input--switch__thumb.success--text::after {
    content: '\002714';
    font-weight: bold;
    color: white;
  }
</style>
