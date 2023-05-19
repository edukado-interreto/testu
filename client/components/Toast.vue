<script>
export default {
  data: () => ({
    timeout: 10000,
    toasts: [],
  }),
  methods: {
    success(text) {
      return this.spawn(text, { color: 'success' });
    },
    warning(text) {
      return this.spawn(text, { color: 'warning' });
    },
    error(text) {
      return this.spawn(text, { color: 'error' });
    },
    spawn(text, attrs) {
      const uid = this._getUid();
      setTimeout(() => this.remove(uid), this.timeout + 10);
      this.toasts.push({ text, open: true, uid, attrs });
    },
    remove(uid) {
      const idx = this.toasts.findIndex((t) => (t.uid = uid));
      this.toasts.splice(idx, 1);
    },
    _getUid() {
      return new Date().toISOString();
    },
  },
};
</script>

<template>
  <aside>
    <v-snackbar
      v-for="(toast, i) in toasts"
      v-model="toast.open"
      v-bind="toast.attrs"
      :key="toast.uid"
      :style="`bottom: ${i * 4}em`"
      :timeout="timeout"
      class="toast"
    >
      {{ toast.text }}
      <template v-slot:action="{ attrs }">
        <v-btn v-bind="attrs" plain icon @click="() => remove(toast.uid)">
          <v-icon color="white">mdi-close-circle</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </aside>
</template>

<style>
.toast {
  transition: bottom 0.4s;
}
</style>
