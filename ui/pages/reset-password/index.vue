<script setup lang="ts">
const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const reset_form = useTemplateRef("form")
const email = ref("")
const error_messages = ref<string[]>([])
const valid = ref<boolean | undefined>(undefined)
const submitted = ref(false)

const validate = () => reset_form.value?.validate()

async function submit() {
  if (!(await validate())?.valid) return
  const url = "/auth/password/reset/"
  try {
    const detail = await auth.reset_password_send(email.value)
    console.info(" Detail: ", detail)
    error_messages.value = []
    submitted.value = true
  } catch (e: any) {
    if (e?.response?.status === 400 && e.response.data) {
      error_messages.value = Object.values(e.response.data).flat() as string[]
    }
  }
}

onMounted(() => {
  const query_email = route.query?.email as string | undefined
  if (query_email) {
    email.value = query_email
    router.replace(route.path)
  }
})
</script>

<template>
  <v-row class="mt-5">
    <v-spacer />
    <v-col cols="7">
      <h2 class="mb-8">{{ t("login.password_reset") }}</h2>
      <v-form
        ref="form"
        v-model="valid"
        :disabled="submitted"
        @submit.prevent="submit"
      >
        <v-text-field
          v-model="email"
          name="email"
          variant="outlined"
          type="email"
          :label="t('login.email')"
          prepend-inner-icon="mdi-account"
          :rules="[v => /.+@.+\..+/.test(v) || t('login.mail_invalid')]"
          validate-on="blur"
          required
        />
        <v-btn
          type="submit"
          color="primary"
          class="mt-2"
          :disabled="!email || submitted"
        >
          {{ t("login.password_reset") }}
        </v-btn>
        <div v-show="error_messages.length > 0">
          <v-alert class="mt-2 alert-pre-line" type="error">
            <ul style="list-style: none; padding: 0">
              <li v-for="(error, i) in error_messages" :key="i">
                {{ error }}
              </li>
            </ul>
          </v-alert>
        </div>
      </v-form>
      <v-alert class="mt-6" type="success" v-if="submitted">
        {{ t("login.password_reset_sent") }}
      </v-alert>
    </v-col>
    <v-spacer />
  </v-row>
</template>
