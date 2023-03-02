<template>
  <v-text-field
    ref="field"
    outlined
    dense
    prepend-inner-icon="mdi-link-variant"
    append-icon="mdi-content-copy"
    @click:append="copy_text"
    :value="value"
    :label="label"
    readonly
    hide-details
  >
  </v-text-field>
</template>
<script>
export default {
  props: [ 'value', 'label' ],
  methods: {
    copy_text() {
      const input = this.$refs.field.$el.querySelector('input')
      input.select()
      document.execCommand('copy')
    }
  }
}
</script>
