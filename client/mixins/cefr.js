export default {
  data: () => ({
    CEFR: [
      ,
      'A1',
      'A2',
      'B1',
      'B2',
      'C1',
      'C2'
    ]
  }),
  methods: {
    n2cefr(n) {
      return this.CEFR[n]
    },
    cefr2n(level) {
      return this.CEFR.findIndex(v => v == level)
    }
  },
  computed: {
    cefr_levels() {
      // return each cefr level,
      // i.e. return all the values except undefined ones
      // i.e. ['A1', …, 'C2']
      return this.CEFR.filter(v => v !== undefined)
    },
    cefr_indexes() {
      // return the numeric equivalent of each level,
      // i.e. return all the indexes for the defined values
      // i.e. [1, …, 6]
      return this.cefr_levels.map(
        level => this.cefr2n(level)
      )
    },
    cefr_lbound() {
      // return the numeric lower bound level
      // i.e. 1
      return this.cefr2n(this.cefr_levels[0])
    },
    cefr_ubound() {
      // return the numeric upper bound level
      // i.e. 6
      return this.cefr2n(
        this.cefr_levels[this.cefr_levels.length-1]
      )
    }
  }
}
