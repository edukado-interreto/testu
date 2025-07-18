<script setup lang="ts">
const { $api } = useNuxtApp()

const props = defineProps<{ item: Exercise | Exam }>()
const liked = ref(false)
const auth = useAuthStore()
const emit = defineEmits(["liked"])

const click = async () => {
  if (!auth.user) return

  const model = props.item.url.includes("exercise") ? "exercises" : "exams"
  const url = `${model}/${props.item.lid}/like/`
  const resp = await $api<LikedResponse>(url, { method: "post" })
  liked.value = !!resp.liked // Cast null or 1 as Boolean
  emit("liked", liked.value)
}

const color = (active: boolean, hover: boolean) => {
  const hue = active || hover ? "pink" : "grey"
  const transparency = 4 - Number(active) * 2 - Number(hover)
  return `${hue}-lighten-${transparency}`
}

onMounted(() => {
  liked.value = !!props.item.liked
})
</script>

<template>
  <v-hover #="{ isHovering, props }">
    <v-btn
      v-bind="props"
      @click="click"
      icon
      :disabled="!auth.user"
      class="d-print-none"
      variant="text"
    >
      <v-icon class="icon" size="large" :color="color(liked, !!isHovering)">
        mdi-heart
      </v-icon>
    </v-btn>
  </v-hover>
</template>
