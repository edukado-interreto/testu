export default defineNuxtRouteMiddleware(async () => {
  const auth = useAuthStore()
  const localePath = useLocalePath()

  if (!(await auth.check_token())) {
    const route = localePath({ name: "login" })
    return navigateTo(route)
  }
})
