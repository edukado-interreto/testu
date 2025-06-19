<script setup lang="ts">
type Content = { title: string; message: string }

const { t } = useI18n()

const title = defineModel<string>("title", { default: "" })
const message = defineModel<string>("message", { default: "" })
const dialog = ref(false)
const ret = { STAY: false, QUIT: true } as const

let resolve: (value: boolean) => void

const open = (content: Content) => {
  dialog.value = true
  title.value = content?.title || ""
  message.value = content?.message || ""
  return new Promise<boolean>(resolver => {
    resolve = resolver
  })
}

const close = () => {
  dialog.value = false
}

const stay = () => {
  resolve(ret.STAY)
  close()
}

const quit = () => {
  resolve(ret.QUIT)
  close()
}

defineExpose({ open })
</script>

<template>
  <v-dialog v-model="dialog" max-width="400">
    <v-sheet variant="elevated">
      <div class="pa-6 d-fle">
        <v-icon class="float-left mr-3" size="x-large" color="pink-darken-1">
          mdi-alert-box
        </v-icon>
        <p class="text-h6 text-color-red">
          {{ title }}
        </p>
        <p class="text-italic mt-3">
          {{ message }}
        </p>
      </div>
      <div class="pa-6 d-flex justify-end">
        <v-btn class="mx-2" variant="tonal" color="red-darken-1" @click="quit">
          {{ $t("editor.confirm_leave.continue") }}
          <v-icon end icon="mdi-trash-can-outline"></v-icon>
        </v-btn>
        <v-btn class="mx-2" variant="elevated" color="primary" @click="stay">
          {{ $t("editor.confirm_leave.close") }}
          <v-icon end icon="mdi-file-edit-outline"></v-icon>
        </v-btn>
      </div>
    </v-sheet>
  </v-dialog>
</template>
