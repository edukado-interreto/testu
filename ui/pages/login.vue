<script setup lang="ts">
const [route, router, localePath] = [useRoute(), useRouter(), useLocalePath()]
const { t: $t, t } = useI18n()
const auth = useAuthStore()

const form = ref<HTMLFormElement | null>(null)
const email = ref("")
const password = ref("")
const valid = ref(undefined)
const error_message = ref("")
const loading = ref(false)

const filled = computed(() => email.value && password.value)
const validate = async () => {
  return filled && (await form.value?.validate()).valid
}
const redirect = async () => {
  await navigateTo(route.redirectedFrom || "/")
}

useHead(() => ({ title: t("login.page_title") }))

const login_success = () => {
  redirect()
}
const login_error = (e: any | Error) => {
  const error = unref(e)
  error_message.value = error.data?.non_field_errors.join("\n")
}

const login = async () => {
  if (!(await validate())) return
  const credentials = { email: email.value, password: password.value }
  try {
    loading.value = true
    await auth.login(credentials)
    login_success()
  } catch (error) {
    login_error(error)
  } finally {
    loading.value = false
  }
}
const reset_validation = () => {
  error_message.value = ""
  loading.value = false
  form.value?.resetValidation()
}

onMounted(async () => {
  if (auth.user === null) await auth.check_token()
  if (auth.user?.username) redirect()
})
</script>

<template>
  <v-container>
    <v-row class="mt-5">
      <v-spacer />
      <v-col class="col-md-7">
        <v-alert type="success" v-if="'verified' in route.query">
          {{ $t("login.email_is_verified") }}
        </v-alert>
        <v-alert type="success" v-if="'reset' in route.query">
          {{ $t("login.password_reset_done") }}
        </v-alert>
        <v-form
          ref="form"
          v-model="valid"
          validation-on="submit lazy"
          @submit.prevent="login"
        >
          <v-text-field
            v-model="email"
            autofocus
            variant="underlined"
            name="email"
            type="email"
            :label="$t('login.email')"
            prepend-icon="mdi-account"
            validate-on="lazy submit"
            :rules="[v => /.+@.+\..+/.test(v) || $t('login.mail_invalid')]"
            @update:modelValue="reset_validation"
            required
          />
          <v-text-field
            v-model="password"
            variant="underlined"
            :label="$t('login.password')"
            name="password"
            type="password"
            prepend-icon="mdi-lock"
            validate-on="lazy submit"
            :rules="[v => v !== '' || $t('login.required_field')]"
            @update:modelValue="reset_validation"
            @update:focused="reset_validation"
            required
          />
          <v-btn
            type="submit"
            color="primary"
            class="mt-2 me-2"
            :disabled="!filled || loading"
          >
            {{ $t("login.login") }}
          </v-btn>
          <v-btn
            color="secondary"
            class="mt-2 text-white"
            :to="localePath({ name: 'reset-password', query: { email } })"
            v-show="!!error_message"
          >
            {{ $t("login.password_reset") }}
          </v-btn>
          <v-alert class="mt-6" type="error" v-show="!!error_message">
            {{ error_message }}
          </v-alert>
        </v-form>
      </v-col>
      <v-spacer />
    </v-row>
    <v-row>
      <v-col class="mx-auto v-col-8 v-col-lg-6">
        <v-sheet color="grey-lighten-4" class="mt-12 pa-6" rounded="xl">
          <p
            class="text-center text-grey"
            v-text="$t('login.no_account_yet')"
          />
          <p class="text-center mt-4">
            <v-btn
              color="amber"
              class="text-none px-8"
              variant="flat"
              nuxt
              :to="localePath('/signup')"
            >
              {{ $t("main.signup") }}
            </v-btn>
          </p>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>
