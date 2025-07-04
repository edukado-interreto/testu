<script setup lang="ts">
const is_editor = computed<boolean>(() => {
  return (useRoute().name as string)?.startsWith("editor")
})
</script>

<template>
  <v-app>
    <NuxtLayout :is_editor>
      <NuxtPage />
    </NuxtLayout>
  </v-app>
</template>
