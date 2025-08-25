<script setup lang="ts">
const [route, router, localePath] = [useRoute(), useRouter(), useLocalePath()]
const { t } = useI18n()
const auth = useAuthStore()

const password = ref<string>("")
const error_messages = ref<string[]>([])
const show = ref(false)
const invalid = ref(false)
const submitted = ref(false)

useHead({
  title: t("login.password_reset"),
})

const submit = async () => {
  const key = route.params.key as string

  // Expecting key like "uid:token"
  const [uid, token] = (key ?? "").split(":")

  // Basic guard if params are missing
  if (!uid || !token) {
    error_messages.value = [t("login.verify_token_used_or_invalid") as string]
    invalid.value = true
    return
  }

  try {
    await auth.reset_password(uid, token, password.value)

    submitted.value = true
    await router.push(localePath({ name: "login", query: { reset: "" } }))
  } catch (e: any) {
    const status = e?.statusCode ?? e?.status ?? e?.response?.status
    const data = e?.data ?? e?.response?.data ?? {}

    if (status === 400 && data && typeof data === "object") {
      const errors = Object.keys(data)

      if (errors.includes("token") || errors.includes("uid")) {
        error_messages.value = [
          t("login.verify_token_used_or_invalid") as string,
        ]
        invalid.value = true
      } else if (errors.includes("new_password2")) {
        // Expect array of strings from backend validation
        error_messages.value = Array.isArray(data.new_password2)
          ? data.new_password2
          : [String(data.new_password2)]
      } else {
        // Fallback: flatten other possible backend error messages
        error_messages.value = errors.flatMap(k => {
          const val = (data as Record<string, unknown>)[k]
          return Array.isArray(val) ? val.map(String) : [String(val)]
        })
      }
    } else {
      // Unknown error
      error_messages.value = [
        (t("common.unknown_error") as string) || "Unexpected error",
      ]
    }
  }
}
</script>

<template>
  <v-row class="mt-5">
    <v-spacer />
    <v-col cols="7">
      <h2 class="mb-8">{{ t("login.password_reset") }}</h2>

      <v-form @submit.prevent="submit">
        <v-text-field
          v-model="password"
          name="password"
          variant="outlined"
          :type="show ? 'text' : 'password'"
          :label="t('login.password')"
          prepend-inner-icon="mdi-lock"
          :append-inner-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append-inner="show = !show"
          :disabled="submitted"
          required
        />

        <v-btn
          type="submit"
          class="mt-2"
          color="primary"
          :disabled="!password || submitted"
          :text="t('login.password_reset')"
        />

        <v-btn
          class="mt-2 ms-2"
          color="secondary"
          :to="localePath({ name: 'reset-password' })"
          v-show="invalid"
          :disabled="submitted"
        >
          {{ t("login.resend_link") }}
        </v-btn>
      </v-form>

      <div v-show="error_messages.length > 0">
        <v-alert class="mt-6 alert-pre-line" type="error" variant="tonal">
          <ul style="list-style: none; padding: 0; margin: 0">
            <li v-for="(error, i) in error_messages" :key="i">
              {{ error }}
            </li>
          </ul>
        </v-alert>
      </div>
    </v-col>
    <v-spacer />
  </v-row>
</template>
