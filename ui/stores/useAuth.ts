import { StorageSerializers, useLocalStorage } from "@vueuse/core"

const ACCESS_TOKEN_LIFETIME = 3600 // seconds
const AS_OBJECT = { serializer: StorageSerializers.object }

export const useAuthStore = defineStore("auth", () => {
  const API_BASE_URL = useRuntimeConfig().public.apiBase
  const $auth = $fetch.create({ baseURL: `${API_BASE_URL}/api/auth`, method: "POST" })

  // STORE
  const user: Ref<User | null> = useLocalStorage("user", null, AS_OBJECT)

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
    user.value = (await $auth<LoginResponse>("login/", { body: credentials })).user
  }

  const logout = async () => {
    const { detail } = await $auth<LogoutResponse>("logout/")
    $reset()
    useToasts().success(detail)
  }

  return { $reset, check_token, logged_in, login, logout, user }
})
