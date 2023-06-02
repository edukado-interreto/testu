<template>
  <v-container>
    <h1>About</h1>

    <h2 class="mb-3">{{ $t('about.about') }}</h2>
    <p class="text-justify">{{ $t('about.about_text') }}</p>

    <h2>{{ $t('about.partners_title') }}</h2>

    <div v-for="(partner, id) in partners" :key="id">
      <h3 class="mt-7 mb-4 text-center">{{ partner.name }}</h3>

      <div class="d-md-flex align-center partner">
        <aside>
          <a :href="partner.url" target="_blank">
            <img :src="'/partners/' + id + '.png'" :alt="partner.name" />
          </a>
        </aside>

        <div class="pl-10">
          <div class="mb-2">
            <v-icon class="mr-1">mdi-map-marker</v-icon>
            {{ $t('about.partners.' + id + '_location') }}
          </div>
          <div class="mb-2">
            <v-icon class="mr-1">mdi-web</v-icon>
            <a :href="partner.url" target="_blank">{{ partner.domain }}</a>
          </div>
          <p class="text-justify" v-html="partner.description"></p>
        </div>
      </div>
    </div>
  </v-container>
</template>
<script>
export default {
  head: () => ({
    title: 'About',
  }),
  data() {
    return {
      partners: {
        ikso: {
          name: 'Edukácia@Internet',
          url: 'https://ikso.net/',
          domain: 'ikso.net',
          description: this.$t('about.partners.ikso_description', {
            1: '<a href="https://lernu.net/" target="_blank">lernu.net</a>',
            2: '<a href="https://slovake.eu/" target="_blank">slovake.eu</a>',
          }),
        },
        bit: {
          name: 'bit schulungscenter GmbH',
          url: 'https://www.bitschulungscenter.at/en/innovation/',
          domain: 'bitschulungscenter.at',
          description: this.$t('about.partners.bit_description'),
        },
        vu: {
          name: this.$t('about.partners.vu_name'),
          url: 'https://www.flf.vu.lt/',
          domain: 'flf.vu.lt',
          description: this.$t('about.partners.vu_description'),
        },
        uam: {
          name: this.$t('about.partners.uam_name'),
          url: 'https://amu.edu.pl',
          domain: 'amu.edu.pl',
          description: this.$t('about.partners.uam_description'),
        },
        leipzig: {
          name: this.$t('about.partners.leipzig_name'),
          url: 'https://www.uni-leipzig.de/',
          domain: 'uni-leipzig.de',
          description: this.$t('about.partners.leipzig_description'),
        },
      },
    };
  },
};
</script>

<style scoped>
.partner {
  max-width: 1100px;
  margin: auto;
}

img {
  max-width: 200px;
  margin: auto;
}
</style>
