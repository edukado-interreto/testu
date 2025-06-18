import type { UseFetchOptions } from "nuxt/app"
import type { Composer } from "vue-i18n"

async function refreshToken() {
  const config = useRuntimeConfig()
  const token = useCookie("refreshToken").value

  try {
    const response = (await $fetch(`${config.public.apiBase}/api/auth/token/refresh/`, {
      method: "POST",
      data: { refresh: token },
    })) as Response
    return response.json()?.access
  } catch (error) {
    throw new Error("Token refresh failed")
  }
}

export default defineNuxtPlugin((app) => {
  const config = useRuntimeConfig()

  const baseURL = `${config.public.apiBase}/api/v1/`
  const i18n = app.$i18n as Composer
  const token = useCookie<string | null>("jwt-access")
  const headers = {
    ...useRequestHeaders(),
    "Accept-Language": i18n.locale.value,
  }

  const $apiFetch = $fetch.create({
    baseURL,
    headers,
    onRequest({ request, options }) {
      if (token.value) options.headers.set("Authorization", `Bearer ${token.value}`)
    },
    onResponse({ request, response, options }) {
      // Not Implemented
      // response._data = new myBusinessResponse(response._data)
    },
    async onResponseError({ request, response, options }) {
      if (response.status === 401) {
        try {
          token.value = await refreshToken()

          options.headers.set("Authorization", `Bearer ${token.value}`)
          $fetch(request.url, options as UseFetchOptions<T>)
        } catch (error) {
          console.error(error)
          throw error
        }
      }
    },
  })
  // Use with: const { $api, $apiFetch } = useNuxtApp()
  return {
    provide: { api: $apiFetch, apiFetch: $apiFetch.raw },
  }
})
