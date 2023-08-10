export default {
  methods: {
    unit_component(t) {
      return {
        default: "UnitDefault",
        open_answer: "UnitOpenAnswer",
        multiple_choice: "UnitMultipleChoice",
        pairing: "UnitPairing",
      }[t]
    },
  },
}
