import * as vueuse from "@vueuse/core"

const AS_OBJECT = { serializer: vueuse.StorageSerializers.object }

const $auth = $fetch.create({ baseURL: "/api/auth", method: "POST" })

export const useAuthStore = defineStore("auth", () => {
  // STORE
  const user: Ref<User | null> = vueuse.useLocalStorage("user", null, AS_OBJECT)

  // GETTERS
  const logged_in = computed<boolean>(() => user.value !== null)

  // ACTIONS
  const $reset = () => {
    user.value = null
  }

  const check_token = async (): Promise<boolean> => {
    try {
      const data = await $auth<User>("user/", { method: "get" })
      user.value = data
      return true
    } catch {
      return false
    }
  }

  const login = async (credentials: LoginCredential) => {
    const body = { body: credentials }
    const data = await $auth<LoginResponse>("login/", body)
    user.value = data.user
  }

  const logout = async () => {
    await $auth("logout/")
    $reset()
  }

  return { $reset, check_token, logged_in, login, logout, user }
})
