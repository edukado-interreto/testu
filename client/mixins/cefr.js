export default {
  data: () => ({
    CEFR: [, "A1", "A2", "B1", "B2", "C1", "C2"],
  }),
  methods: {
    n2cefr(n) {
      return this.CEFR[n]
    },
    cefr2n(level) {
      return this.CEFR.findIndex((v) => v == level)
    },
    cefr_info(item) {
      /**
       * Return a human readable text describing a cefr level range.
       * @param {object} item - An object with fields lang_learn_cefr_level_min
       *   and lang_learn_cefr_level_max containing values in the range 1-6,
       *   representing resp. A1-C2.
       * @example
       *   cefr_info({…min: 1, …max: 2}) => 'A1 - A2'
       *   cefr_info({…min: 1, …max: 1}) => 'A1'
       *   cefr_info({…min: 1, …max: 6}) => '' (any level: empty string)
       */

      const item_min = item.lang_learn_cefr_level_min
      const item_max = item.lang_learn_cefr_level_max

      if (item_min == this.cefr_lbound && item_max == this.cefr_ubound) return ""

      if (item_min == item_max) return this.n2cefr(item_min)

      return `${this.n2cefr(item_min)} - ${this.n2cefr(item_max)}`
    },
  },
  computed: {
    cefr_levels() {
      // return each cefr level,
      // i.e. return all the values except undefined ones
      // i.e. ['A1', …, 'C2']
      return this.CEFR.filter((v) => v !== undefined)
    },
    cefr_indexes() {
      // return the numeric equivalent of each level,
      // i.e. return all the indexes for the defined values
      // i.e. [1, …, 6]
      return this.cefr_levels.map((level) => this.cefr2n(level))
    },
    cefr_lbound() {
      // return the numeric lower bound level
      // i.e. 1
      return this.cefr2n(this.cefr_levels[0])
    },
    cefr_ubound() {
      // return the numeric upper bound level
      // i.e. 6
      return this.cefr2n(this.cefr_levels[this.cefr_levels.length - 1])
    },
  },
}
