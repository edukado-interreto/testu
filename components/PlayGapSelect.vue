<template>
  <v-select
    dense
    style="display:inline-block"
    :items="shuffle(token.rights.concat(token.wrongs))"
    v-model="value"
    :success="success === true"
    :error="success === false"
    :prepend-inner-icon="success === undefined ? undefined : (success ? 'mdi-check-bold' : 'mdi-close-thick')"
  ></v-select>
</template>
<script>
export default {
  name: 'PlayGapSelect',
  props: [ "token" ],
  data: () => ({
    value: undefined
  }),
  computed: {
    success: function() {
      if (this.token.rights.includes(this.value)) {
        return true
      }
      if (this.token.wrongs.includes(this.value)) {
        return false
      }
      return undefined
    }
  },
  methods: {
    shuffle: function(array) {
      // shuffle an array using the Fisher-Yates algorithm
      let currentIndex = array.length,  randomIndex;
      // While there remain elements to shuffle...
      while (currentIndex != 0) {
        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        // And swap it with the current element.
        [array[currentIndex], array[randomIndex]] = [
          array[randomIndex], array[currentIndex]];
      }
      return array;
    }
  },
  watch: {
    success: function(val, oldVal) {
      if (process.server) return
      if (val === true) {
        this.$confetti({
          angle: 90,
          spread: 110,
          particleCount: 60,
          origin: { x:0.5, y: 0.5 },
          decay: 0.8
        });
      }
    }
  }
}
</script>
