<script setup lang="ts">
// ChatGPT made!!
const { confetti_shoot } = useConfettiShoot()
const shuffle_array = useShuffleArray()

const props = defineProps<{
  code: string
  shuffle: boolean
  solved: object
  readonly: boolean
  silent: boolean
}>()

const score_awarded = ref(0)
const drags = ref([])
const movable = ref([])
const overed = ref([])

const update_dragging = () => {
  const parsed = computedParsed.value

  drags.value = parsed
    .map((p) => p[0])
    .sort((a, b) => a.localeCompare(b))
    .map((e) => [e, null])

  if (props.shuffle) {
    drags.value = shuffle_array(drags.value)
  }

  movable.value = parsed.map((p) => [false, false])
  overed.value = parsed.map((p) => [false, false])
}

const load_drags_from_solved = () => {
  if (!props.solved || !props.solved.drags) return
  nextTick(() => {
    drags.value = [...props.solved.drags]
  })
}

const on_dragstart = (e, src_row, src_col) => {
  if (props.readonly) return
  e.dataTransfer.setData(
    "text/plain",
    JSON.stringify({
      component: componentUid,
      row: src_row,
      col: src_col,
    }),
  )
}

const on_dragleave = (e, dst_row, dst_col) => {
  if (props.readonly) return
  overed.value[dst_row][dst_col] = false
}

const on_dragover = (e, dst_row, dst_col) => {
  if (props.readonly) return
  if (drags.value[dst_row][dst_col] !== null) return
  e.preventDefault()
}

const on_dragenter = (e, dst_row, dst_col) => {
  if (props.readonly) return
  if (drags.value[dst_row][dst_col] !== null) return
  e.preventDefault()
  overed.value[dst_row][dst_col] = true
}

const on_drop = (e, dst_row, dst_col) => {
  if (props.readonly) return
  let src
  try {
    src = JSON.parse(e.dataTransfer.getData("text"))
    if (src.component !== componentUid) throw "Cross-component drop"
  } catch (e) {
    overed.value[dst_row][dst_col] = false
    return
  }
  e.preventDefault()
  drags.value[dst_row][dst_col] = drags.value[src.row][src.col]
  drags.value[src.row][src.col] = null
  overed.value[dst_row][dst_col] = false

  if (dst_col === 1 && success.value[dst_row]) {
    if (!props.silent) {
      confetti_shoot(guess_col.value[dst_row])
    }
  }
}

const get_solved = () => ({
  parsed: computedParsed.value,
  drags: drags.value,
})

const computedParsed = computed(() => {
  if (props.solved) return props.solved.parsed || []
  return props.code
    .split("\n\n")
    .map((s, i) => {
      let [src, dst] = s.split(/==(.*)/s).map((s) => s.trim())
      if (!dst) {
        dst = `${i + 1}`
      }
      return [src, dst]
    })
    .filter(([src, dst]) => !!src)
})

const success = computed(() => {
  return drags.value.map((pair, i) => {
    if (pair[1] === null) return undefined
    return pair[1] === computedParsed.value[i][0]
  })
})

const score_available = computed(() => 0) // TODO

watch(() => props.solved, load_drags_from_solved)
watch(() => props.shuffle, update_dragging)
watch(computedParsed, update_dragging)

onMounted(() => {
  update_dragging()
})

created(() => {
  load_drags_from_solved()
})
</script>

<template>
  <div class="mb-5">
    <v-row dense v-for="(pair, i) in drags" :key="parsed[i][1]">
      <v-col cols="4">
        <div class="mr-4 fill-height">
          <!--
            we use redundant divs because binding some events
            to v-sheet elements results in a buggy behaviour
          -->
          <div
            v-if="pair[0] !== null"
            :draggable="!readonly && movable[i][0]"
            @dragstart="on_dragstart($event, i, 0)"
            class="fill-height"
          >
            <v-sheet
              rounded
              :elevation="2"
              class="pa-1 fill-height"
              style="position: relative"
            >
              <div class="pa-1 mr-7">
                <RichContent :text="pair[0]" />
              </div>
              <v-icon
                class="pa-2"
                style="position: absolute; right: 0; top: 0; cursor: move"
                :disabled="readonly === true"
                @mouseenter="$set(movable[i], 0, true)"
                @touchstart="$set(movable[i], 0, true)"
                @mouseleave="$set(movable[i], 0, false)"
                @touchend="$set(movable[i], 0, false)"
              >
                mdi-drag
              </v-icon>
            </v-sheet>
          </div>
          <v-sheet
            v-else
            rounded
            :class="
              'pa-2 grey grey--text text-center fill-height ' +
              (overed[i][0] ? 'lighten-2' : 'lighten-5')
            "
            @drop="on_drop($event, i, 0)"
            @dragenter="on_dragenter($event, i, 0)"
            @dragleave="on_dragleave($event, i, 0)"
            @dragover="on_dragover($event, i, 0)"
          >
            &nbsp;
          </v-sheet>
        </div>
      </v-col>
      <v-col cols="4" ref="guess_col">
        <div
          v-if="pair[1] !== null"
          :draggable="!readonly && movable[i][1]"
          @dragstart="on_dragstart($event, i, 1)"
          class="fill-height"
        >
          <v-sheet
            rounded
            :elevation="2"
            class="pa-1 fill-height"
            style="position: relative"
          >
            <div class="pa-1 mr-7">
              <RichContent :text="pair[1]" />
            </div>
            <v-icon
              class="pa-2"
              style="position: absolute; right: 0; top: 0; cursor: move"
              :disabled="readonly === true"
              @mouseenter="$set(movable[i], 1, true)"
              @touchstart="$set(movable[i], 1, true)"
              @mouseleave="$set(movable[i], 1, false)"
              @touchend="$set(movable[i], 1, false)"
            >
              mdi-drag
            </v-icon>
          </v-sheet>
        </div>
        <v-sheet
          v-else
          rounded
          :class="
            'pa-2 grey grey--text ' +
            'd-flex justify-center align-center fill-height ' +
            (overed[i][1] ? 'lighten-2' : 'lighten-4')
          "
          @drop="on_drop($event, i, 1)"
          @dragenter="on_dragenter($event, i, 1)"
          @dragleave="on_dragleave($event, i, 1)"
          @dragover="on_dragover($event, i, 1)"
        >
          <div style="pointer-events: none; touch-action: none">drop here</div>
        </v-sheet>
      </v-col>
      <v-col cols="4" style="position: relative">
        <v-sheet rounded :elevation="2" class="pa-1 mr-7 fill-height">
          <div class="pa-1">
            <RichContent :text="parsed[i][1]" />
          </div>
        </v-sheet>
        <div
          v-if="!silent && success !== undefined"
          style="position: absolute; right: 4px; top: 10px"
        >
          <v-icon v-if="success[i] === true" color="success">
            mdi-check-bold
          </v-icon>
          <v-icon v-if="success[i] === false" color="error">
            mdi-close-thick
          </v-icon>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<style scoped>
li {
  margin-bottom: 1.25em;
  line-height: 2.25em;
}
.pre-line {
  white-space: pre-line;
}
</style>
