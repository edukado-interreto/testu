<template>
  <div v-if="submission">
    <v-sheet
      v-for="(unit, i) in submission.exercise?.data?.sheet"
      :key="`submitted_${unit._key}`"
    >
      <div class="headline my-4"> 
        {{ i+1 }}. {{ unit.title }}
        <span v-if="unit.title === ''" class="font-italic">
          Untitled unit
        </span>
      </div>
      <div
        v-if="unit.description"
        class="body-2 mb-4 pre-line"
      >
        <RichContent
          :text="unit.description"
        >
        </RichContent>
      </div>
      <UnitMultipleChoice
        v-if="unit.type == 'multiple_choice'"
        :key="i"
        :solved="unit.solved"
        :readonly="true"
      ></UnitMultipleChoice>
      <UnitPairing
        v-if="unit.type == 'pairing'"
        :key="i"
        :solved="unit.solved"
        :readonly="true"
      ></UnitPairing>
      <UnitDefault
        v-if="unit.type == 'default'"
        :key="i"
        :solved="unit.solved"
        :readonly="true"
      ></UnitDefault>
      <UnitOpenAnswer
        v-if="unit.type == 'open_answer'"
        :key="i"
        :solved="unit.solved"
        :readonly="true"
        :ignore_case="unit.ignore_case"
      ></UnitOpenAnswer>
    </v-sheet>
  </div>
</template>
<script>
// load a solved, submitted exercise and
// display it for review
export default {
  props: [ 'submission' ]
}
</script>
