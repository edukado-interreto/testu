<template>
  <div>
    <v-img
      v-if="!broken"
      :src="src"
      contain
      max-height="150"
      @error="broken = true"
    ></v-img>
    <div v-else class="grey--text">
      <v-icon small>mdi-alert-outline</v-icon>
      <i>Invalid image: {{ content }}</i>
    </div>
  </div>
</template>
<script>
  export default {
    props: [ 'src', 'content' ],
    data: () => ({
      broken: false
    }),
    watch: {
      src() {
        this.broken = false
      }
    }
  }
</script>
