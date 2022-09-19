export default {
  data: () => ({
    CEFR: {
      A1: 0,
      A2: 1,
      B1: 2,
      B2: 3,
      C1: 4,
      C2: 5,
    }
  }),
  methods: {
    n2cefr(n) {
      return Object.entries(this.CEFR).find(e => e[1] == n)[0];
    }
  },
}
