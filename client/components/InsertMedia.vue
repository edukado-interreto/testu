<template>
  <div>
    <MsgBox ref="msgbox"></MsgBox>
    <form ref="form">
      <input
        type="file"
        ref="uploader"
        @change="change"
        :accept="`${type}/*`"
        class="d-none"
      />
      <slot :click="click"></slot>
    </form>
  </div>
</template>
<script>
export default {
  props: [ 'type', 'input_el', 'model' ],
  computed: {
    snippet_prefix() {
      if (this.type === 'audio') return 'sound'
      if (this.type === 'image') return 'img'
      throw `InsertMedia: type must be 'audio' or 'image', was: '${this.type}'`
    }
  },
  methods: {
    click() {
      this.$refs.uploader.click()
    },
    async change(e) {

      const file = e.target.files[0]
      if (!file) return // canceled by user

      this.$emit("load_start")

      const formData = new FormData()
      formData.append("file", file)
      formData.append("type", this.type)

      let resp = undefined

      try {
        resp = await this.$auth.axios.post('/v1/upload/', formData)
      } catch(e) {
        console.error({...e})
        await this.$refs.msgbox.alert(e.response.data.error || "Unexpected server response")
      } finally {
        this.$emit("load_end")
      }

      if (!resp) return

      this.inject_snippet(
        `{${this.snippet_prefix}:${resp.data.name}}`
      )
      this.$refs.form.reset()
    },
    inject_snippet(snippet) {
      // insert in the current code a snippet at the
      // current cursor position, move the cursor
      // after the snippet and focus the textarea

      const input = this.input_el[0][this.input_el[1]]
      const code = this.model[0][this.model[1]] || ""

      console.log("content:", code)
      //console.log("input_el:", this.input_el[0][this.input_el[1]])

      const start = input.selectionStart

      //this.model[0][this.model[1]] = code.slice(
      this.$set(this.model[0], this.model[1], code.slice(
          0, input.selectionStart
        ) + snippet + code.slice(
          input.selectionEnd
        )
      )
      requestAnimationFrame(() => {
        input.selectionStart = start + snippet.length
        input.selectionEnd   = start + snippet.length
        input.focus()
      })
    }
  }
}
</script>
