<template>
  <v-combobox
    multiple
    chips
    @keydown="keydown"
    v-model="valueInnerModel"
    hint='Press Ctrl+Enter to insert the "leave blank" option.'
    :append-icon="null"
    :label="label"
    :autofocus="autofocus"
  >
    <template v-slot:selection="data">
      <v-chip
        :key="JSON.stringify(data.item)"
        v-bind="data.attrs"
        :input-value="data.selected"
        :disabled="data.disabled"
        @click:close="data.parent.selectItem(data.item)"
      >
        <v-icon small v-if="data.item === '\0'">mdi-selection</v-icon>
        <template v-else>{{ data.item }}</template>
      </v-chip>
    </template>
  </v-combobox>
</template>
<script>
export default {
  props: ['value', 'label', 'autofocus'],
  data: () => ({
  }),
  computed: {
    valueInnerModel: {
      // This computed property and the usage of "\0" as
      // replacement for the empty string is a workaround.
      // v-combobox have an issue handling falsy elements:
      // an empty string may be added to the items and is
      // correctly displayed using slots, or even as is,
      // but when deleting the empty string item by user
      // interaction, all items got removed.
      // So we use a computed internal model for the
      // v-combobox, where every occurrences of empty
      // string elements are replaced by a non-printable
      // char (we chose "\0", but also "\n" would work).
      get() {
        return this.valueModel.map(e => (e === "") ? "\0" : e)
      },
      set(val) {
        this.valueModel = val.map(e => (e === "\0") ? "" : e)
      }
    },
    valueModel: {
      // This enable two-way communication between the
      // component and its parent if the 'value' prop
      // is used this way:
      // <component :value.sync="my_value"/>
      get() {
        return this.value
      },
      set(val) {
        this.$emit(
          'update:value',
          val
        )
      }
    },
  },
  methods: {
    keydown(e) {
      // append an empty string to the model on Ctrl+Enter

      if (!e.ctrlKey) return
      if (e.code != 'Enter') return

      if (e.path[0].value !== "") return
      // input field is not empty, abort
      
      if ((this.valueInnerModel||[]).includes('\0')) return
      // empty string is already present, abort

      if (!this.valueInnerModel) this.valueInnerModel = []
      // create the array if its value is falsy

      this.valueInnerModel = [...this.valueInnerModel, '\0']
      // append the value, push() seems to be unreactive here
    },
  }
}
</script>
