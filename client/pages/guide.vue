<template>
  <v-container>


        <h2 class="mb-3">{{ $t('guide.about') }}</h2>
        <p class="text-justify">{{ $t('guide.about_text') }}</p>


    <v-tabs v-model="tab">
      <v-tab >{{ $t('guide.exercice.name') }}</v-tab>
      <v-tab >{{ $t('guide.gap_filling') }}</v-tab>
      <v-tab >{{ $t('guide.multiple_choice') }}</v-tab>
      <v-tab >{{ $t('guide.sort_and_match') }}</v-tab>
      <v-tab >{{ $t('guide.video') }}</v-tab>

    </v-tabs>

    <v-tabs-items v-model="tab" class="pa-1 mt-5">
      <!-- 1_exercice -->

      <v-tab-item>
        <v-img
          :src="`/guide/1_exercise.png`"
          height="300px"
          contain
       ></v-img>
        {{ $t('guide.exercice.explanation1') }}
<br>
        <br>

      <v-img
          :src="`/guide/1_exercice_unit.png`"
          height="300px"
          contain
        ></v-img>
        <br>
        {{ $t('guide.exercice.explanation2') }}
        <br>
        <br>
        <v-row align-self="left" >
          <v-col >
            <v-img
              :src="`/guide/1_type_units.png`"
              contain
              height="500px"
            ></v-img>
          </v-col>
          <v-col >
            <br>
            <p>{{ $t('guide.exercice.explanation3') }}</p>

            <p>{{ $t('guide.exercice.explanation4') }}</p>

            <p>{{ $t('guide.exercice.explanation5') }}</p>

            <p>{{ $t('guide.exercice.explanation6') }}</p>

            <p>{{ $t('guide.exercice.explanation7') }}</p>
          </v-col>
        </v-row>


      </v-tab-item>

      <!-- 2_gap_filling -->
      <v-tab-item>

          <v-img
            :src="`/guide/2_gap_filling_1.png`"
            height="300px"
            contain
          ></v-img>
          {{ $t('guide.exercice.gap_filling_1') }}
          <br>
        {{ $t('guide.exercice.gap_filling_2') }}
          <br>
        {{ $t('guide.exercice.gap_filling_3') }}
        <br>
        {{ $t('guide.exercice.gap_filling_4') }}
        <br>
        <br>
        <v-img
          :src="`/guide/2_gap_filling_tool.png`"
          height="100px"
          contain
        ></v-img>
        {{ $t('guide.exercice.gap_filling_5') }}
        <br>


        <br>
        {{ $t('guide.exercice.gap_filling_open_answer_1') }}
        <br>

          <v-img
            :src="`/guide/2_gap_filling_open_answer.png`"
            height="300px"
            contain
          ></v-img>
        <br>
          <br>
          {{ $t('guide.exercice.gap_filling_open_answer_2') }}
          <br>
          <br>

</v-tab-item>


      <!-- 3_multiple_choice -->
      <v-tab-item>
        {{$t('guide.construction')}}
      </v-tab-item>

      <!-- 4_sort_and_match -->
      <v-tab-item>

        {{$t('guide.construction')}}

      </v-tab-item>

      <!-- 5_video -->
      <v-tab-item>

        {{$t('guide.construction')}}

      </v-tab-item>


    </v-tabs-items>

  </v-container>
</template>

<script>


  export default {
  name: 'guide',
  head() {
  },

  computed: {
    tab: {

  get() {
    return parseInt(this.$route.hash[1]) - 1

},
  set(val) {
    let list_of_contents = ["#1_exercice", "#2_gap_filling",
      "#3_multiple_choice", "#4_sort_and_match", "#5_video"];

      this.$router.replace(list_of_contents[val])

}
},
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
