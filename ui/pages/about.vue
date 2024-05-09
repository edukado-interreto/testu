<template>
  <v-container>
    <v-row>
      <v-col class="v-col-12 v-col-md-9">
        <h1 v-text="$t('about.about')" />

        <p class="text-justify mt-3" v-text="$t('about.about_text')" />
      </v-col>

      <v-col class="v-col-md-3 mt-4">
        <v-row>
          <v-col class="v-col-6 v-col-md-12">
            <a
              href="https://www.facebook.com/profile.php?id=100086451753450"
              target="_blank"
              class="text-decoration-none"
            >
              <v-img contain src="/logos/facebook-2021.svg" max-height="50" />
              <p
                class="text-center mt-2 mb-0"
                v-text="$t('about.facebook_page')"
              />
            </a>
          </v-col>
          <v-col>
            <a
              href="https://t.me/+8Z1dtayqGzk2Yzk0"
              target="_blank"
              class="text-decoration-none"
            >
              <v-img contain src="/logos/telegram-2019.svg" max-height="50" />
              <p
                class="text-center mt-2 mb-0"
                v-text="$t('about.telegram_chat')"
              />
            </a>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <h2>{{ $t("about.partners_title") }}</h2>

    <div v-for="(partner, id) in partners" :key="id">
      <h3 class="mt-7 mb-4 text-center">{{ partner.name }}</h3>

      <div class="d-md-flex align-center partner">
        <aside>
          <a :href="partner.url" target="_blank">
            <img :src="`/partners/${id}.png`" :alt="partner.name" />
          </a>
        </aside>

        <div class="pl-10">
          <div class="mb-2">
            <v-icon class="mr-1">mdi-map-marker</v-icon>
            {{ $t(`about.partners.${id}_location`) }}
          </div>
          <div class="mb-2">
            <v-icon class="mr-1">mdi-web</v-icon>
            <a :href="partner.url" target="_blank">{{ partner.domain }}</a>
          </div>
          <p class="text-justify" v-html="partner.description" />
        </div>
      </div>
    </div>
  </v-container>
</template>

<script setup lang="ts">
const { t } = useI18n()
useHead({ title: t("about.about") })

const partners = {
  ikso: {
    name: "Edukácia@Internet",
    url: "https://ikso.net/",
    domain: "ikso.net",
    description: t("about.partners.ikso_description", {
      1: '<a href="https://lernu.net/" target="_blank">lernu.net</a>',
      2: '<a href="https://slovake.eu/" target="_blank">slovake.eu</a>',
    }),
  },
  bit: {
    name: "bit schulungscenter GmbH",
    url: "https://www.bitschulungscenter.at/en/innovation/",
    domain: "bitschulungscenter.at",
    description: t("about.partners.bit_description"),
  },
  vu: {
    name: t("about.partners.vu_name"),
    url: "https://www.flf.vu.lt/",
    domain: "flf.vu.lt",
    description: t("about.partners.vu_description"),
  },
  uam: {
    name: t("about.partners.uam_name"),
    url: "https://amu.edu.pl",
    domain: "amu.edu.pl",
    description: t("about.partners.uam_description"),
  },
  leipzig: {
    name: t("about.partners.leipzig_name"),
    url: "https://www.uni-leipzig.de/",
    domain: "uni-leipzig.de",
    description: t("about.partners.leipzig_description"),
  },
}
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
