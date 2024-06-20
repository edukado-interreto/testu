import { StorageSerializers, useLocalStorage } from "@vueuse/core"
import type { NitroFetchOptions } from "@nitropack/types"

const AS_OBJECT = { serializer: StorageSerializers.object }

type LoginBody = NitroFetchOptions<string, LoginCredential>

const $auth = $fetch.create({ baseURL: "/api/auth", method: "POST" })

export const useAuth = defineStore("auth", () => {
  // STORE
  const user: Ref<User | null> = useLocalStorage("user", null, AS_OBJECT)

  // GETTERS
  const logged_in: ComputedRef<boolean> = computed(() => user.value !== null)

  // ACTIONS
  const $reset = () => {
    user.value = null
  }

  const login = async (credentials: LoginCredential): Promise<User> => {
    const body = { body: credentials } as LoginBody
    let data = null
    try {
      data = await $auth<LoginResponse>("login/", body)
    } finally {
      user.value = data?.user
    }
    return user
  }

  const logout = async () => {
    await $auth("logout/")
    $reset()
  }

  return { user, login, logout, logged_in, $reset }
})
