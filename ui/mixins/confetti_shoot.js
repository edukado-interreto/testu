export default {
  methods: {
    confetti_shoot(element) {
      this.$confetti({
        angle: 90,
        spread: 110,
        particleCount: 60,
        //origin: { x: 0.5, y: 0.5 },
        origin: this.confetti_calculate_coords(element),
        decay: 0.8,
        disableForReducedMotion: true,
      })
    },
    confetti_calculate_coords: function (element) {
      /**
       * Calculate the coordinates x and y in order
       * to shoot some confetti from the given html element.
       * @param {HTMLElement} element
       * @returns {{ x: {Number}, y: {Number} }}
       */
      const rect = element.getBoundingClientRect()

      // coordinates in pixels
      const px_x = rect.left + rect.width / 2 // center
      const px_y = rect.top + rect.height + 15 // underneath
      // since we shoot the confetti straight upwards,
      // it is more pretty if the confetti come from
      // below the element, hence the offset added in px_y.

      // coordinates as values between 0 and 1,
      // as required by the confetti api
      return {
        x: px_x / window.innerWidth,
        y: px_y / window.innerHeight,
      }
    },
  },
}
