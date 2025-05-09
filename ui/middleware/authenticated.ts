import type RawLocation from "vue-router"

export default defineNuxtRouteMiddleware(async (to, from) => {
  const auth = useAuthStore()
  const localePath = useLocalePath()

  if (!(await auth.check_token())) {
    const route = localePath({ name: "login" })
    return navigateTo(route)
  }
})
