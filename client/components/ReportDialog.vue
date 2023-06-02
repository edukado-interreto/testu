<script>
export default {
  name: 'ReportDialog',
  props: {
    exercise: { required: true, type: String },
    nature: { required: true, type: String }, // "mistake" | "misuse"
  },
  data: () => ({
    description: '',
    disabled: false,
  }),
  methods: {
    close() {
      this.$emit('input', false);
    },
    async submit() {
      this.disabled = true;
      const response = await this.$auth.axios.post('/v1/reports/', {
        exercise: this.exercise,
        nature: this.nature,
        description: this.description,
      });
      if (response?.status !== 201) throw response;

      this.$refs.toasts.success(
        this.$t(`exercise.submit_${this.nature}_confirm`)
      );
      this.description = '';
      this.disabled = false;
      this.close();
    },
  },
};
</script>

<template>
  <div>
    <v-dialog v-bind="$attrs" v-on="$listeners" max-width="500px">
      <v-card>
        <v-form ref="flag_form" :disabled="disabled">
          <v-card-title> <slot /> </v-card-title>
          <v-card-text>
            <v-textarea
              @keypress.ctrl.enter="submit"
              v-model="description"
              rows="2"
              outlined
              :label="$t('exercise.explanation')"
            />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn @click="close">
              {{ $t('main.cancel') }}
            </v-btn>
            <v-btn
              type="submit"
              color="primary"
              @click.prevent="submit"
              :disabled="disabled"
            >
              {{ $t('main.submit') }}
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
    <Toast ref="toasts" />
  </div>
</template>
