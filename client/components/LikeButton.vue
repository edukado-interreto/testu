<template>
  <v-btn v-bind="$attrs" @click="click" :disabled="!user" class="d-print-none">
    <v-hover v-slot="{ hover }">
      <v-icon
        class="icon"
        :color="`${liked || hover ? 'pink' : 'grey'} lighten-${
          hover ? '4' : '2'
        }`"
      >
        mdi-heart
      </v-icon>
    </v-hover>
  </v-btn>
</template>

<script>
export default {
  props: { item: { type: Object, required: true } },
  data() {
    return {
      liked: false,
    };
  },
  computed: {
    user() {
      const authUser = this.$store.getters['authenticator/authUser'];
      if (!authUser) return null;
      return authUser;
    },
  },
  methods: {
    async click() {
      if (!this.user) return;

      console.info(this.$nuxt);
      const model = this.item.url.includes('exercise') ? 'exercises' : 'exams';
      const url = `/v1/${model}/${this.item.lid}/like/`;
      const resp = await this.$auth.axios.post(url);
      const liked = resp.data.liked;
      this.liked = !!liked; // Cast null or 1 as Boolean
      this.$emit('liked', liked);
    },
  },
  mounted() {
    this.liked = !!this.item.liked;
  },
};
</script>
