import { StorageSerializers, useLocalStorage } from "@vueuse/core"

const ACCESS_TOKEN_LIFETIME = 3600 // seconds
const AS_OBJECT = { serializer: StorageSerializers.object }

export const useAuthStore = defineStore("auth", () => {
  const requestFetch = useRequestFetch()
  const AUTH_BASE_URL = `${useRuntimeConfig().public.apiBase}/api/auth`

  const create =
    (method: "get" | "post") =>
    async <T>(url: string, options?: Record<string, any>): Promise<T> => {
      return await requestFetch(`${AUTH_BASE_URL}/${url}`, { method, ...options })
    }

  // const post = async <T>(url: string, options?: Record<string, any>): Promise<T> => {
  //   return await requestFetch(`${AUTH_BASE_URL}/${url}`, { method: "post", ...options })
  // }
  const $auth = { get: create("get"), post: create("post") }

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
      const data = await $auth.get<User>("user/")
      user.value = data
      return true
    } catch {
      $reset()
      return false
    }
  }

  const login = async (credentials: LoginCredential) => {
    user.value = (await $auth.post<LoginResponse>("login/", { body: credentials })).user
  }

  const logout = async () => {
    const { detail } = await $auth.post<LogoutResponse>("logout/")
    $reset()
    useToasts().success(detail)
  }
  const reset_password_send = async (email: string) => {
    const body = { email }
    const { detail } = await $auth.post<LogoutResponse>("password/reset/", { body })
    return detail
  }
  const reset_password = async (uid: string, token: string, password: string) => {
    const { detail } = await $auth.post<LogoutResponse>("password/reset/confirm/", {
      body: { uid, token, new_password1: password, new_password2: password },
    })
    return detail
  }

  return {
    $reset,
    check_token,
    logged_in,
    login,
    logout,
    user,
    reset_password,
    reset_password_send,
  }
})
