<template>
  <div>
    {{ id }}
    {{ exercise }}
  </div>
</template>
<script>
  export default {
    name: 'Exercise',
    data: () => ({
    }),
    async asyncData({ route, params }) {
      const id = (process.server) ? route.params.id : params.id;
      let exercise;

      if (id) {
        exercise = await (
          await fetch(`/api/v1/sheets/${id}/`)
        ).json()
      }

      return {
        id,
        exercise
      }
    }
  }
</script>
