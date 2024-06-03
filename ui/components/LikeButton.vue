<script setup lang="ts">
const { $api } = useNuxtApp()

const props = defineProps<{ item: object }>()
const liked = ref(false)
const $store = { getters: { "authenticator/authUser": { username: "USERNAME" } } }
const emit = defineEmits(["liked"])

const user = computed(() => {
  const authUser = $store.getters["authenticator/authUser"]
  if (!authUser) return null
  return authUser
})

const click = async () => {
  if (!user) return

  const model = props.item.url.includes("exercise") ? "exercises" : "exams"
  const url = `/v1/${model}/${props.item.lid}/like/`
  const resp = await $api(url, { method: "POST" })
  const liked = resp.data.liked
  liked.value = !!liked.value // Cast null or 1 as Boolean
  emit("liked", liked.value)
}

onMounted(() => {
  liked.value = !!props.item.liked
})
</script>

<template>
  <v-btn v-bind="$attrs" @click="click" :disabled="!user" class="d-print-none" variant="text">
    <v-hover v-slot:default="{ isHovering, props }">
      <v-icon
        v-bind="props"
        class="icon"
        :color="`${liked || isHovering ? 'pink' : 'grey'} lighten-${
          isHovering ? '4' : '2'
        }`"
      >
        mdi-heart
      </v-icon>
    </v-hover>
  </v-btn>
</template>
