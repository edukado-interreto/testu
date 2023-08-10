<template>
  <v-dialog
    v-model="display"
    :max-width="opts.max_width"
    :persistent="opts.modal"
  >
    <v-card>
      <v-card-title
        v-if="opts.title"
        :class="`${opts.color} white--text text-overline py-1`"
        v-text="opts.title"
      ></v-card-title>
      <v-card-text class="text-body-1 black--text d-flex pt-5">
        <v-icon x-large>{{ opts.icon }}</v-icon>
        <div
          class="ml-5"
          style="white-space: pre-line"
          v-text="opts.text"
        ></div>
      </v-card-text>
      <v-card-actions class="pb-5">
        <v-spacer></v-spacer>
        <v-btn
          v-for="btn in opts.buttons"
          :key="btn.value"
          v-text="btn.text"
          :color="btn.value ? 'primary' : undefined"
          @click="onclick($event, btn.value)"
          outlined
        ></v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
/*
 * This component provides alert, confirm and custom dialog
 * boxes with an interface similar to the native alert() and
 * confirm() JavaScript functions.

 * Example usage:
 *  
 *  <MsgBox ref="msgbox"></MsgBox>
 *
 *  if (!await this.$refs.msgbox.confirm(
 *    'Are you sure you want to proceed?'
 *  )) return;
 *
 */
export default {
  data: () => ({
    display: false,
    opts: {},
    promise_resolve: null,
    promise_reject: null,
    original_opts: {
      text: "",
      title: "TestU",
      max_width: 700,
      modal: true,
      icon: "mdi-alert-circle-outline",
      color: "secondary",
      buttons: [{ text: "Ok", value: true }],
    },
  }),
  created() {
    this.opts = { ...this.original_opts }
  },
  async mounted() {
    // // usage example
    // const reply = await this.confirm("Are you sure?", "Confirm")
    // this.alert(`You did choose: ${reply}`)
  },
  methods: {
    onclick(e, value) {
      this.hide()
      this.$nextTick(() => {
        this.promise_resolve(value)
      })
    },
    hide() {
      this.display = false
    },
    show(opts) {
      this.hide()
      this.opts = { ...this.original_opts, ...opts }
      this.display = true
      return new Promise((resolve, reject) => {
        this.promise_resolve = resolve
        this.promise_reject = reject
      })
    },
    alert(text, title) {
      return this.show({
        text,
        title: title || this.original_opts.title,
      })
    },
    confirm(text, title) {
      return this.show({
        text,
        title: title || this.original_opts.title,
        icon: "mdi-help-circle-outline",
        color: "primary",
        buttons: [
          { text: "Cancel", value: false },
          { text: "Ok", value: true },
        ],
      })
    },
  },
}
</script>
