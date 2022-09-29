export default {
  methods: {
    unit_component(t) {
      return {
        'default': 'UnitDefault',
        'open_answer': 'UnitOpenAnswer',
      }[t]
    },
  }
}
