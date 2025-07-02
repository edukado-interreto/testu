<script setup lang="ts">
import MsgBox from "@/components/MsgBox.vue"

const model = defineModel<Partial<Unit>>()
const props = defineProps<{
  type: "audio" | "image"
  input_el: HTMLTextAreaElement
  field: "description" | "code"
}>()
const emit = defineEmits<{
  load_start: []
  load_end: []
}>()

const { $apiFetch } = useNuxtApp()

// Template refs
const uploader = useTemplateRef<HTMLInputElement>("uploader")
const msgbox = useTemplateRef<typeof MsgBox>("msgbox")
const form = useTemplateRef<HTMLFormElement>("form")

const snippet_prefix = computed(() => {
  if (props.type === "audio") return "sound"
  if (props.type === "image") return "img"
  throw new Error(
    `InsertMedia: type must be 'audio' or 'image', was: '${props.type}'`,
  )
})

const open = () => {
  uploader.value?.click()
}

const change = async (e: Event) => {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return // canceled by user

  emit("load_start")

  const formData = new FormData()
  formData.append("file", file)
  formData.append("type", props.type)

  let resp: any = undefined

  try {
    // Note: You'll need to inject or import your auth/axios service
    // resp = await $auth.axios.post('/v1/upload/', formData)
    resp = await $apiFetch("upload/", {
      method: "POST",
      body: formData,
    })
    console.log(resp)
  } catch (e: any) {
    console.error({ ...e })
    msgbox.value?.alert(
      e.response?.data?.error || "Unexpected response",
      JSON.stringify(e),
    )
  } finally {
    emit("load_end")
  }

  if (!resp) return

  inject_snippet(`{${snippet_prefix.value}:${resp._data.name}}`)
  form.value?.reset()
}

const inject_snippet = (snippet: string) => {
  // Insert in the current code a snippet at the current cursor position,
  // move the cursor after the snippet and focus the textarea
  if (model.value === undefined) return

  const input = props.input_el
  const code = model.value[props.field] || ""

  const start = input.selectionStart as number

  model.value[props.field] =
    code.slice(0, input.selectionStart) +
    snippet +
    code.slice(input.selectionEnd as number)

  console.info("snippet", snippet)

  nextTick(() => {
    input.selectionStart = start + snippet.length
    input.selectionEnd = start + snippet.length
    input.focus()
  })
}
</script>

<template>
  <MsgBox ref="msgbox" />
  <form ref="form">
    <input
      type="file"
      ref="uploader"
      @change="change"
      :accept="`${type}/*`"
      class="d-none"
    />
    <slot :click="open"></slot>
  </form>
</template>
