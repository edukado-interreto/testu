<script setup lang="ts">
import type { FetchError } from "ofetch"

const { $api, $apiFetch } = useNuxtApp()
const { t } = useI18n()
const localePath = useLocalePath()

const signup_form = ref<HTMLFormElement | null>(null)

const username = ref("")
const email = ref("")
const password = ref("")
const valid = ref(undefined)
const submitted = ref(false)
const error_messages: Ref<string[]> = ref([])

useHead({ title: t("login.signup") })

const register_new_user = async () => {
  if (!(await validate()).valid) return

  error_messages.value = []

  try {
    const response = await $apiFetch("/auth/register/", {
      method: "POST",
      body: {
        username: username.value,
        email: email.value,
        password1: password.value,
        password2: password.value,
      },
    })
    submitted.value = true
  } catch (e: FetchError | any) {
    if (e.status === 400) {
      error_messages.value = Object.values(e.data).flat()
      return
    }
    error_messages.value = [`Server error (${e.status}: ${e.statusText})`]
    console.error({ ...e.response })
  }
}
const validate = () => signup_form.value?.validate()
</script>

<template>
  <v-row class="mt-5">
    <v-spacer />
    <v-col v-if="submitted" cols="7">
      <p>
        {{ $t("login.signup_thanks") }}
      </p>
      <p>
        {{ $t("login.check_inbox") }}
      </p>
    </v-col>
    <v-col v-else cols="7">
      <v-form
        ref="signup_form"
        v-model="valid"
        :lazy-validation="true"
        @submit.prevent="register_new_user"
      >
        <h1 class="text-h5 mb-5">{{ $t("login.signup") }}</h1>
        <v-text-field
          variant="outlined"
          density="compact"
          v-model="username"
          :label="$t('login.username')"
          :rules="[(v) => v !== '' || $t('login.required_field')]"
          required
        />
        <v-text-field
          variant="outlined"
          density="compact"
          v-model="email"
          :label="$t('login.email')"
          :rules="[(v) => /.+@.+\..+/.test(v) || $t('login.mail_invalid')]"
          type="email"
          name="email"
          validate-on="blur"
          required
        />
        <v-text-field
          variant="outlined"
          density="compact"
          v-model="password"
          :label="$t('login.password')"
          type="password"
          :rules="[(v) => v !== '' || $t('login.required_field')]"
          required
        />
        <v-btn type="submit" color="primary" class="mt-2">
          {{ $t("main.signup") }}
        </v-btn>
        <v-alert
          class="mt-2 alert-pre-line"
          type="error"
          v-show="error_messages.length > 0"
        >
          <ul style="list-style: none; padding: 0">
            <li v-for="(error, i) in error_messages">
              {{ error }}
            </li>
          </ul>
        </v-alert>
      </v-form>

      <div class="text--secondary mt-8">
        {{ $t("login.already_registered") }}
        <v-btn
          :to="localePath('/login')"
          v-text="t('main.login')"
          class="mx-3 text-none"
          variant="outlined"
          density="compact"
          color="primary"
        />
      </div>
    </v-col>
    <v-spacer />
  </v-row>
</template>
