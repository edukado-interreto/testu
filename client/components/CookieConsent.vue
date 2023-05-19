<script>
export default {
  name: 'CookieConsent',
  data: () => ({
    show: false,
  }),
  methods: {
    clicked(answer) {
      localStorage.setItem('cookies', answer);
      this.show = false;
    },
  },
  mounted() {
    // Just checking if it’s set at this stage
    this.show = !localStorage.getItem('cookies');
  },
};
</script>

<template>
  <v-bottom-sheet id="cookie-consent" v-model="show" persistent inset>
    <v-sheet class="px-12 py-6 text-center" min-height="5em">
      <v-icon> mdi-cookie-alert </v-icon>
      <p
        class="text-emphasis-secondary text-small !!"
        v-text="$t('main.cookie_consent')"
      />
      <v-btn
        color="primary"
        @click="() => clicked('accepted')"
        data-value="accepted"
      >
        {{ $t('main.accept') }}
      </v-btn>
    </v-sheet>
  </v-bottom-sheet>
</template>
