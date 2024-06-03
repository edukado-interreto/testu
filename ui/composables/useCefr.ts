const CEFR = { A1: 1, A2: 2, B1: 3, B2: 4, C1: 5, C2: 6 } as const

const cefr_levels = Object.keys(CEFR).sort()

const n2cefr = (n: number) => Object.keys(CEFR).find((key: Cefr) => CEFR[key] === n)

const cefr_info = (item: Exercise) => {
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

  if (item_min === CEFR.A1 && item_max === CEFR.C2) return ""

  if (item_min === item_max) return n2cefr(item_min)

  return `${n2cefr(item_min)} - ${n2cefr(item_max)}`
}

export default function () {
  return {
    CEFR,
    n2cefr,
    cefr_info,
    cefr_levels,
  }
}
