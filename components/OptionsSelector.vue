<template>
  <v-combobox
    multiple
    chips
    @keydown="keydown"
    v-model="optionsModel"
    :hint='((optionsModel.length > 0) ? "Toggle the switches to set the options as right or wrong." : "")'
    placeholder="Start typing an option..."
    :append-icon="null"
    :label="label"
    :autofocus="autofocus"
    :rules="rules"
    validate-on-blur
  >
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
  }),
  methods: {
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
