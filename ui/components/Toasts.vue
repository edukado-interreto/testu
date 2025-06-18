<script setup lang="ts">
const store = useToasts()
const TEN_SECONDS = 10000
</script>

<template>
  <aside>
    <v-snackbar-queue v-model="store.toasts" closable :timeout="TEN_SECONDS" />
  </aside>
</template>
