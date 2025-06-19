<script setup lang="ts">
/*
 * This component provides alert, confirm and custom dialog
 * boxes with an interface similar to the native alert() and
 * confirm() JavaScript functions.

 * Example usage:
 *  
 *  <MsgBox ref="msgbox" />
 *
 *  if (!await msgbox.confirm(
 *    'Are you sure you want to proceed?'
 *  )) return;
 *
 */

const opts = ref<MsgBoxOptions>({})
const original_opts = reactive<MsgBoxOptions>({
  text: "",
  title: "TestU",
  max_width: 700,
  modal: true,
  icon: "mdi-alert-circle-outline",
  color: "secondary",
  buttons: [{ text: "Ok", value: true }],
})
const display = ref(false)
const promise_resolve = ref<Function | null>(null)
const promise_reject = ref<Function | null>(null)

onBeforeMount(() => {
  opts.value = { ...original_opts }
})

onMounted(async () => {
  // // usage example
  // const reply = await confirm("Are you sure?", "Confirm")
  // alert(`You did choose: ${reply}`)
})

const onclick = (e: Event, value: boolean) => {
  hide()
  nextTick(() => {
    promise_resolve.value && promise_resolve.value(value)
  })
}

const hide = () => {
  display.value = false
}

const show = (options: MsgBoxOptions) => {
  hide()
  opts.value = { ...original_opts, ...options }
  display.value = true
  return new Promise((resolve, reject) => {
    promise_resolve.value = resolve
    promise_reject.value = reject
  })
}

const alert = (text: string, title: string) => {
  return show({
    text,
    title: title || original_opts.title,
  })
}

const confirm = (text: string, title: string) => {
  return show({
    text,
    title: title || original_opts.title,
    icon: "mdi-help-circle-outline",
    color: "primary",
    buttons: [
      { text: "Cancel", value: false },
      { text: "Ok", value: true },
    ],
  })
}

defineExpose({ hide, show, alert, confirm })
</script>

<template>
  <v-dialog
    v-model="display"
    :max-width="opts.max_width"
    :persistent="opts.modal"
  >
    <v-card>
      <v-card-title
        v-if="opts.title"
        :class="`bg-${opts.color} text-white text-overline py-2`"
        v-text="opts.title"
      />
      <v-card-text class="text-body-1 text-black d-flex align-center pt-5">
        <v-icon size="x-large" color="grey-darken-2">{{ opts.icon }}</v-icon>
        <div class="ml-5" style="white-space: pre-line" v-text="opts.text" />
      </v-card-text>
      <v-card-actions class="pa-5">
        <v-spacer />
        <v-btn
          v-for="btn in opts?.buttons || []"
          :key="btn.value.toString()"
          v-text="btn.text"
          :color="btn.value ? 'primary' : 'tertiaryy'"
          @click="onclick($event, btn.value)"
          variant="outlined"
        />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
