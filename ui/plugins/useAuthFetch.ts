import type { UseFetchOptions } from "#app";
import { defu } from "defu";

async function useAuthFetch<T>(
  url: string,
  options: UseFetchOptions<T> = {}
) {
  const accessToken = useCookie("jwt-access");

  const defaults: UseFetchOptions<T> = {
    baseURL: "/api",
    key: url,
    headers: accessToken.value
      ? { Authorization: `Bearer ${accessToken.value}` }
      : {},
    onResponse: async ({ response, options }) => {
      if (response.status === 401) {
        try {
          const newToken = await refreshToken();
          accessToken.value = newToken;

          options.headers = { Authorization: `Bearer ${newToken}` };
          useFetch(url, options as UseFetchOptions<T>);
        } catch (error) {
          console.error("Token refresh failed:", error);
        }
      }
    },
  };

  const params = defu(options, defaults);

  return useFetch(url, params);
}

async function refreshToken() {
  const refreshToken = useCookie("refreshToken");

  const { data, status } = await useFetch<{ access: string }>(
    "/api/auth/token/refresh/",
    {
      method: "POST",
      body: { refresh: refreshToken.value },
    }
  );

  if (status.value === "success") {
    return data.value?.access;
  } else {
    throw new Error("Token refresh failed");
  }
}

export default defineNuxtPlugin(() => {
return {  provide: {
    http: useAuthFetch
  }
}})
