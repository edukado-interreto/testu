<script setup lang="ts">
const instance = getCurrentInstance()
const { t } = useI18n()
const { confetti_shoot } = useConfettiShoot()
const shuffle_array = useShuffleArray()

type Props = {
  code: string
  shuffle?: boolean
  solved?: SolvedDrags
  readonly?: boolean
  silent?: boolean
  parsed?: [string, string][]
}
const {
  code,
  shuffle = false,
  solved,
  readonly = false,
  silent = false,
  parsed,
} = defineProps<Props>()

const uid = computed(() => instance?.uid || 0)
const score_awarded = ref(0)
const drags = ref<Drags | []>([])
const movable = ref<[boolean, boolean][] | []>([])
const hovered = ref<[boolean, boolean][] | []>([])

const update_dragging = () => {
  drags.value = parsed_local.value
    .map(p => p[0])
    .sort((a, b) => a.localeCompare(b))
    .map(e => [e, null])

  if (shuffle) {
    drags.value = shuffle_array(drags.value) as Drags
  }

  movable.value = parsed_local.value.map(p => [false, false])
  hovered.value = parsed_local.value.map(p => [false, false])
}

const load_drags_from_solved = () => {
  if (!solved || !solved.drags) return
  nextTick(() => {
    drags.value = [...solved.drags]
  })
}

const on_dragstart = (e, src_row, src_col) => {
  if (readonly) return
  e.dataTransfer.setData(
    "text/plain",
    JSON.stringify({ uid: uid.value, row: src_row, col: src_col }),
  )
}

const on_dragleave = (e, dst_row, dst_col) => {
  if (readonly) return
  hovered.value[dst_row][dst_col] = false
}

const on_dragover = (e, dst_row, dst_col) => {
  if (readonly) return
  if (drags.value[dst_row][dst_col] !== null) return
  e.preventDefault()
}

const on_dragenter = (e, dst_row, dst_col) => {
  if (readonly) return
  if (drags.value[dst_row][dst_col] !== null) return
  e.preventDefault()
  hovered.value[dst_row][dst_col] = true
}

const on_drop = (e, dst_row, dst_col) => {
  if (readonly) return
  let src
  try {
    src = JSON.parse(e.dataTransfer.getData("text"))
    if (src.uid !== uid.value) throw "Cross-component drop"
  } catch (e) {
    hovered.value[dst_row][dst_col] = false
    return
  }
  e.preventDefault()
  drags.value[dst_row][dst_col] = drags.value[src.row][src.col]
  drags.value[src.row][src.col] = null
  hovered.value[dst_row][dst_col] = false

  if (dst_col === 1 && success.value[dst_row]) {
    if (!silent) {
      confetti_shoot(guess_col.value[dst_row])
    }
  }
}

const get_solved = (): SolvedDrags => ({
  parsed: parsed_local.value,
  drags: drags.value,
})

const parsed_local = computed(() => {
  if (solved) return solved.parsed || []
  return code
    .split("\n\n")
    .map((s, i) => {
      let [src, dst] = s.split(/==(.*)/s).map(s => s.trim())
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
    return pair[1] === parsed_local.value[i][0]
  })
})

const score_available = computed(() => 0) // TODO

load_drags_from_solved()

watch(() => solved, load_drags_from_solved)
watch(() => shuffle, update_dragging)
watch(parsed_local, update_dragging)

onMounted(update_dragging)

defineExpose({ get_solved })
</script>

<template>
  <div class="mb-5">
    <v-row dense v-for="(pair, i) in drags" :key="parsed_local[i][1]">
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
              class="d-flex align-center fill-height"
            >
              <RichContent class="v-col" :text="pair[0]" />
              <v-col class="flex-grow-0">
                <v-icon
                  class="cursor-move"
                  :disabled="readonly === true"
                  @mouseenter="movable[i][0] = true"
                  @touchstart="movable[i][0] = true"
                  @mouseleave="movable[i][0] = false"
                  @touchend="movable[i][0] = false"
                >
                  mdi-drag
                </v-icon>
              </v-col>
            </v-sheet>
          </div>
          <v-sheet
            v-else
            rounded
            :color="hovered[i][0] ? 'grey-lighten-2' : 'grey-lighten-5'"
            class="drop-zone pa-2 text-grey border-t border-s text-center fill-height"
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
            class="d-flex align-center fill-height"
          >
            <RichContent class="v-col" :text="pair[1]" />
            <v-col class="flex-grow-0">
              <v-icon
                class="cursor-move"
                :disabled="readonly === true"
                @mouseenter="movable[i][1] = true"
                @touchstart="movable[i][1] = true"
                @mouseleave="movable[i][1] = false"
                @touchend="movable[i][1] = false"
              >
                mdi-drag
              </v-icon>
            </v-col>
          </v-sheet>
        </div>
        <v-sheet
          v-else
          rounded
          class="drop-zone border-t border-s pa-2 text-grey d-flex justify-center align-center fill-height"
          :color="hovered[i][1] ? 'grey-lighten-2' : 'grey-lighten-4'"
          @drop="on_drop($event, i, 1)"
          @dragenter="on_dragenter($event, i, 1)"
          @dragleave="on_dragleave($event, i, 1)"
          @dragover="on_dragover($event, i, 1)"
        >
          <div class="drop-zone-text">
            {{ t("exercise.drop_here") }}
          </div>
        </v-sheet>
      </v-col>
      <v-col cols="4" class="d-flex flex-wrap">
        <TransitionGroup name="result">
          <v-sheet
            rounded
            cols="11"
            :elevation="2"
            class="v-col align-center fill-height"
            key="answer"
          >
            <RichContent :text="parsed_local[i][1]" />
          </v-sheet>
          <v-col
            cols="1"
            v-if="!silent && success !== undefined"
            key="feedback"
          >
            <v-icon v-if="success[i] === true" color="success">
              mdi-check-bold
            </v-icon>
            <v-icon v-if="success[i] === false" color="error">
              mdi-close-thick
            </v-icon>
          </v-col>
        </TransitionGroup>
      </v-col>
    </v-row>
  </div>
</template>

<style lang="scss" scoped>
li {
  margin-bottom: 1.25em;
  line-height: 2.25em;
}
.pre-line {
  white-space: pre-line;
}
.drop-zone {
  transition: background-color 300ms ease-out;

  .drop-zone-text {
    pointer-events: none;
    touch-action: none;
    text-shadow: 0 1px white;
  }
}
.result {
  &-move,
  &-enter-active,
  &-leave-active {
    transition: all 300ms ease;
  }

  &-enter-from,
  &-leave-to {
    opacity: 0;
    transform: translateX(3rem);
  }

  /* ensure leaving items are taken out of layout flow so that moving
   animations can be calculated correctly. */
  &-leave-active {
    position: absolute;
  }
}
</style>
