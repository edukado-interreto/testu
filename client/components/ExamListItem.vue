<template>
  <v-card
    :to="localePath(`/exam_editor?exam=${item.lid}`)"
    nuxt
    class="mb-5"
  >
    <v-card-title
      class="subheading font-weight-bold"
    >
      <span>
        {{ item.name }}
      </span>
      <v-spacer></v-spacer>
      <v-chip v-if="item.accept_submission" small color="primary">Accepts submissions</v-chip>
    </v-card-title>
    <v-card-subtitle v-if="item.description">
      {{ item.description }}
    </v-card-subtitle>
    <v-divider></v-divider>
    <v-card-text>
      <v-icon small>mdi-account</v-icon> {{ item.created_by || $t('exercise.anonymous') }}
      <span>·</span>
      <v-icon small>mdi-clock</v-icon> {{ date_formatted(item.created) }}
    </v-card-text>
  </v-card>

</template>
<script>
export default {
  name: 'ExamListItem',
  props: [ 'item' ],
  methods: {
    date_formatted(d) {
      return (
        new Date(d)
      ).toLocaleString("en-US") // TODO: i18n 
    },
  }
}
</script>
