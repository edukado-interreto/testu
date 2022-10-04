export default {
  methods: {
    shuffle_array: function(in_array) {
      /**
       * Shuffle an array using the Fisher-Yates algorithm,
       * O(n), un-biased.
       */

      const out_array = in_array.slice();
      // clone the input array

      let currentIndex = out_array.length, randomIndex;

      // While there remain elements to shuffle...
      while (currentIndex != 0) {
        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        // And swap it with the current element.
        [out_array[currentIndex], out_array[randomIndex]] = [
          out_array[randomIndex], out_array[currentIndex]];
      }

      return out_array;
    },
  }
}
