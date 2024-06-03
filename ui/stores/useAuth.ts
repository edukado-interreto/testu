import { NitroFetchOptions } from "~/node_modules/nitropack/types"

const { $api } = useNuxtApp()
const $auth = $fetch.create({
  baseURL: "/api/auth",
  method: "POST",
})

export const useAuth = defineStore("auth", () => {
  const user = ref<User | null>(null)

  const login = async (credentials: LoginCredential): Promise<User> => {
    const data = await $auth<LoginResponse>("login/", { body: credentials })
    user.value = data.user
    return user
  }
  return { user, login }
})
