<script setup lang="ts">
import type { AwaitExpression } from "typescript"

const { $api, $apiFetch } = useNuxtApp()
const { t } = useI18n()
const router = useRouter()
const localePath = useLocalePath()

useHead({ title: t("login.verify_email") })

const form = ref<HTMLFormElement | null>(null)

const key = ref("")
const email = ref("")
const error_messages: Ref<string[]> = ref([])
const submitted = ref(false)

const verify_email = async () => {
  const url = "/auth/register/verify-email/"

  try {
    await $api(url, { method: "POST", body: { key: key.value } })
  } catch (e) {
    if (e.response.status === 404) {
      error_messages.value.push(t("login.verify_token_used_or_invalid"))
      return
    }
  }
  router.push({ path: localePath("/login"), query: { verified: null } })
}

const resend_link = async () => {
  if (!email.value) return
  if (!(await form.value?.validate()).valid) return

  const url = "/auth/register/resend-email/"

  try {
    const response: Response = await $apiFetch(url, {
      method: "POST",
      body: { email: email.value },
    })
    if (response.status === 200) submitted.value = true
  } catch (e) {
    // Always returns 200 even for non-existing email
    console.warn(e)
  }
}

onMounted(async () => {
  key.value = useRoute().params.key.toString()
  await verify_email()
})
</script>

<template>
  <v-row class="mt-5">
    <v-spacer />
    <v-col cols="7">
      <h2 class="mb-8">{{ $t("login.verify_email") }}</h2>

      <div v-if="error_messages.length > 0">
        <v-alert class="my-4" type="error">
          <ul style="list-style: none; padding: 0">
            <li v-for="(msg, i) in error_messages" :key="i" v-text="msg"/>
          </ul>
        </v-alert>

        <v-form @submit.prevent="resend_link" v-show="!submitted" ref="form" class="my-6 ">
          <v-text-field
            v-model="email"
            name="email"
            type="email"
            variant="underlined"
            :label="$t('login.email')"
            prepend-icon="mdi-account"
            :rules="[(v) => /.+@.+\..+/.test(v) || $t('login.mail_invalid')]"
            validate-on="submit lazy"
            required
          />
          <v-btn
            type="submit"
            class="mx-auto text-white"
            color="secondary"
            v-text="t('login.resend_link')"
          />
        </v-form>
      </div>
      <div v-else class="d-flex mt-16">
        <v-spacer/>
        <v-progress-circular indeterminate color="accent" size="70" width="3" />
        <v-spacer/>
      </div>
    </v-col>
    <v-spacer />
  </v-row>
</template>
