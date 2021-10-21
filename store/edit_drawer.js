export const state = () => ({
  sheet: undefined,
  node_path: undefined,
})

export const mutations = {
  set_node_path(state, value) {
    state.path = value
  },
  set_sheet(state, value) {
    state.sheet = value
  },
}
