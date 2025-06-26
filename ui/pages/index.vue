<script setup lang="ts">
const { t } = useI18n()

useHead(() => ({ title: `Testu.eu - ${t("main.catchphrase")}` }))
</script>

<template>
  <exercise-search />
</template>
