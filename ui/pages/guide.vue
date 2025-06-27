<script setup lang="ts">
const route = useRoute()
const router = useRouter()

const tab = computed({
  get() {
    return parseInt(route.hash[1]) - 1
  },
  set(val) {
    let list_of_contents = [
      "#1_exercice",
      "#2_gap_filling",
      "#3_multiple_choice",
      "#4_sort_and_match",
      "#5_create_an_exam",
    ]

    router.replace({ hash: list_of_contents[val] })
  },
})
</script>

<template>
  <v-container>
    <h2 class="mb-3">{{ $t("guide.about") }}</h2>
    <p class="text-justify">{{ $t("guide.about_text") }}</p>

    <v-tabs
      v-model="tab"
      align-tabs="center"
      center-active
      class="mt-4"
      bg-color="grey-lighten-4"
      color="primary"
      grow
      mandatory
      show-arrows
    >
      <v-tab class="text-none">{{ $t("guide.exercice.name") }}</v-tab>
      <v-tab class="text-none">{{ $t("guide.gap_filling") }}</v-tab>
      <v-tab class="text-none">{{ $t("guide.multiple_choice.name") }}</v-tab>
      <v-tab class="text-none">{{ $t("guide.sort_and_match.name") }}</v-tab>
      <v-tab class="text-none">{{ $t("guide.exam.name") }}</v-tab>
    </v-tabs>

    <v-tabs-window v-model="tab" class="pa-1 mt-5">
      <v-container>
        <!-- 1_exercice -->
        <v-tabs-window-item>
          <v-img :src="`/guide/1_exercise.png`" height="300px" contain />
          {{ $t("guide.exercice.explanation1") }}
          <br>
          <br>

          <v-img :src="`/guide/1_exercice_unit.png`" height="300px" contain />
          <br>
          {{ $t("guide.exercice.explanation2") }}
          <br>
          <br>
          <v-row align-self="left">
            <v-col>
              <v-img :src="`/guide/1_type_units.png`" contain height="500px" />
            </v-col>
            <v-col>
              <br>
              <p>{{ $t("guide.exercice.explanation3") }}</p>

              <p>{{ $t("guide.exercice.explanation4") }}</p>

              <p>{{ $t("guide.exercice.explanation5") }}</p>

              <p>{{ $t("guide.exercice.explanation6") }}</p>

              <p>{{ $t("guide.exercice.explanation7") }}</p>
            </v-col>
          </v-row>
        </v-tabs-window-item>

        <!-- 2_gap_filling -->
        <v-tabs-window-item>
          <v-img :src="`/guide/2_gap_filling_1.png`" height="300px" contain />
          {{ $t("guide.exercice.gap_filling_1") }}
          <br>
          {{ $t("guide.exercice.gap_filling_2") }}
          <br>
          {{ $t("guide.exercice.gap_filling_3") }}
          <br>
          {{ $t("guide.exercice.gap_filling_4") }}
          <br>
          <br>
          <v-img
            :src="`/guide/2_gap_filling_tool.png`"
            height="100px"
            contain
          />
          {{ $t("guide.exercice.gap_filling_5") }}
          <br>

          <br>
          {{ $t("guide.exercice.gap_filling_open_answer_1") }}
          <br>

          <v-img
            :src="`/guide/2_gap_filling_open_answer.png`"
            height="300px"
            contain
          />
          <br>
          <br>
          {{ $t("guide.exercice.gap_filling_open_answer_2") }}
          <br>
          <br>
        </v-tabs-window-item>

        <!-- 3_multiple_choice -->
        <v-tabs-window-item>
          {{ $t("guide.multiple_choice.explanation1") }}
          <br>

          {{ $t("guide.multiple_choice.explanation2") }}
          <br>

          <br>

          <v-img
            :src="`/guide/3_multiple_choices.png`"
            height="300px"
            contain
          />

          {{ $t("guide.multiple_choice.explanation3") }}
          <br>

          <br>
          {{ $t("guide.multiple_choice.explanation4") }}

          <br>

          <br>
          <v-img
            :src="`/guide/3_multiple_choices_img.png`"
            height="300px"
            contain
          />

          <br>

          {{ $t("guide.multiple_choice.explanation5") }}
          <br>

          <br>
          <v-img
            :src="`/guide/3_multiple_choice_sound.png`"
            height="300px"
            contain
          />
        </v-tabs-window-item>

        <!-- 4_sort_and_match -->
        <v-tabs-window-item>
          {{ $t("guide.sort_and_match.explanation1") }}

          <br>

          <br>
          {{ $t("guide.sort_and_match.explanation1_1") }}

          <br>

          <br>
          {{ $t("guide.sort_and_match.explanation2") }}
          <br>

          <br>

          <v-img :src="`/guide/4_sort_and_match.png`" height="300px" contain />

          {{ $t("guide.sort_and_match.explanation3") }}

          <br>

          <br>
          <v-img
            :src="`/guide/4_sort_and_match_img.png`"
            height="300px"
            contain
          />

          <br>

          {{ $t("guide.sort_and_match.explanation4") }}
          <br>

          <br>
          <v-img
            :src="`/guide/4_sort_and_match_sounds.png`"
            height="300px"
            contain
          />

          <br>

          {{ $t("guide.sort_and_match.explanation5") }}
          <br>

          <br>
          <v-img
            :src="`/guide/4_sort_and_match_order.png`"
            height="300px"
            contain
          />

          <br>

          {{ $t("guide.sort_and_match.video") }}
          <br>

          <br>
          <v-img :src="`/guide/5_video.png`" height="300px" contain />
        </v-tabs-window-item>

        <!-- 5_create_an_exam -->
        <v-tabs-window-item>
          {{ $t("guide.exam.explanation1") }}
          <br>

          {{ $t("guide.exam.explanation2") }}
          <br>

          <br>

          <v-img :src="`/guide/6_exam_1.png`" height="400px" contain />

          <v-img :src="`/guide/6_exam_2.png`" height="200px" contain />
          {{ $t("guide.exam.explanation3") }}
          <br>

          <br>
          {{ $t("guide.exam.explanation4") }}

          <br>

          <br>

          <v-img :src="`/guide/6_exam_3.png`" height="300px" contain />

          <br>

          {{ $t("guide.exam.explanation5") }}
          <br>

          <br>
          <v-img :src="`/guide/6_exam_4.png`" height="300px" contain />

          <br>

          {{ $t("guide.exam.explanation6") }}
          <br>
          <br>

          {{ $t("guide.exam.explanation7") }}
          <br>
          <br>
          <v-img :src="`/guide/6_exam_5.png`" height="300px" contain />
        </v-tabs-window-item>
      </v-container>
    </v-tabs-window>
  </v-container>
</template>

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
