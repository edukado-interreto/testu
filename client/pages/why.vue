<script>
export default {
  methods: {
    point(idx) {
      return `why.point${idx + 1}`
    },
    title(idx) {
      return [this.point(idx), "title"].join(".")
    },
    subtitle(idx) {
      return [this.point(idx), "subtitle"].join(".")
    },
  },
}
</script>

<template>
  <v-container id="page-why">
    <h1 class="ms-4">{{ $t("Why") }}</h1>

    <v-row>
      <v-col cols="12" class="col-lg-6">
        <h2 class="ms-4">{{ $t("why.because") }}</h2>
        <v-list lines="three" three-line class="transparent mt-4">
          <v-list-item v-for="idx in [...Array(10).keys()]" :key="idx">
            <v-list-item-avatar>
              <v-avatar :style="`background: hsl(${34 - 18 * idx}, 86%, 62%)`">
                <span class="white--text font-weight-bold">{{ idx + 1 }}</span>
              </v-avatar>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>
                {{ $t(title(idx)) }}
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ $t(subtitle(idx)) }}
                <span v-if="point(idx) == 'why.point4'">
                  <!-- multilingual -->
                  <a href="https://tradukejo.ikso.net/project/6/">
                    tradukejo.ikso.net/project/6
                  </a>
                </span>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>

        <p class="text-center text--disabled mt-4">
          {{ $t("why.more_projects") }}
          <a href="https://ikso.net/projects/">ikso.net/projects</a>
        </p>
      </v-col>

      <v-col id="infographic" cols="12" class="col-sm-10 col-lg-6 mx-sm-auto">
        <v-img src="/why/testu_10_reasons_why.jpeg" alt="" />
      </v-col>
    </v-row>
  </v-container>
</template>

<style lang="scss">
#page-why {
  background: #fcfef0;

  h1,
  h2 {
    color: #364958;
  }
  .v-list-item__content {
    align-items: start;
  }
  .v-list-item__subtitle {
    -webkit-line-clamp: initial;
  }
}
</style>
