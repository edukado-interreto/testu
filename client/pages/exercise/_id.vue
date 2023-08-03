<template>
  <v-container>
    <MsgBox ref="msgbox"></MsgBox>
    <v-row>
      <v-col>
        <h1>{{ exercise.name }}</h1>
      </v-col>
      <v-spacer class="d-print-none"></v-spacer>
      <v-col cols="auto" class="d-print-none">
        <v-btn @click="window_print" plain>
          <v-icon left color="primary">mdi-printer</v-icon>
          {{ $t('exercise.pdf') }}
        </v-btn>
        <LikeButton icon :item="exercise" @liked="liked" />
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              class="d-print-none"
              :disabled="!user_logged_in"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list v-if="user_logged_in">
            <v-list-item nuxt @click="create_exam">
              <v-list-item-icon>
                <v-icon>mdi-school</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                {{ $t('exercise.create_exam') }}
              </v-list-item-title>
            </v-list-item>
            <v-list-item
              nuxt
              :to="localePath(`/editor?new_from=${exercise.lid}`)"
            >
              <v-list-item-icon>
                <v-icon>mdi-content-copy</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                {{ $t('exercise.create_copy') }}
              </v-list-item-title>
            </v-list-item>
            <v-list-item
              v-if="user_is_creator"
              nuxt
              :to="localePath(`/editor?edit=${exercise.lid}`)"
            >
              <v-list-item-icon>
                <v-icon>mdi-pencil</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                {{ $t('exercise.edit') }}
              </v-list-item-title>
            </v-list-item>
            <v-list-item
              v-if="user_is_creator"
              class="error--text font-weight-bold"
              @click="remove"
            >
              <v-list-item-icon>
                <v-icon color="error">mdi-delete</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                {{ $t('exercise.delete') }}
              </v-list-item-title>
            </v-list-item>
            <v-list-item
              v-if="!user_is_creator"
              @click="() => (mistake_dialog = !mistake_dialog)"
            >
              <v-list-item-icon>
                <v-icon> mdi-format-strikethrough-variant </v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>
                  {{ $t('exercise.mistake') }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item
              v-if="!user_is_creator"
              @click="() => (misuse_dialog = !misuse_dialog)"
            >
              <v-list-item-icon>
                <v-icon>mdi-alert-box</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                {{ $t('exercise.flag') }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-col>
    </v-row>
    <ExerciseFooterAttributes
      :exercise="exercise"
      class="mb-6"
    ></ExerciseFooterAttributes>

    <v-sheet v-if="exercise.description" class="mb-7">
      {{ exercise.description }}
    </v-sheet>

    <v-sheet v-for="(unit, i) in exercise.data.sheet" :key="unit._key">
      <div class="headline my-4">
        {{ i + 1 }}. {{ unit.title }}
        <span v-if="unit.title === ''" class="font-italic">
          {{ $t('sheet_editor.untitled_unit') }}
        </span>
      </div>
      <div v-if="unit.description" class="body-2 mb-4 pre-line">
        <RichContent :text="unit.description"> </RichContent>
      </div>
      <component
        :is="unit_component(unit.type)"
        :code="unit.code"
        :shuffle="unit.shuffle"
        :ignore_case="unit.ignore_case"
        :silent="all_silent"
        :readonly="all_readonly"
        :ref="`unit-${unit._key}`"
      />
    </v-sheet>

    <v-btn
      @click="submit"
      class="mt-9 primary d-print-none"
      :disabled="submitted"
    >
      {{ $t('exercise.check') }}
    </v-btn>

    <ReportDialog
      nature="mistake"
      v-if="exercise"
      :exercise="exercise.lid"
      v-model="mistake_dialog"
    >
      <v-icon class="pe-3" color="warning">
        mdi-format-strikethrough-variant
      </v-icon>
      {{
        $t('exercise.report_mistake_to_creator', {
          username: exercise.created_by,
        })
      }}
    </ReportDialog>

    <ReportDialog
      nature="misuse"
      v-if="exercise"
      :exercise="exercise.lid"
      v-model="misuse_dialog"
    >
      <v-icon class="pe-3" color="error"> mdi-alert-box </v-icon>
      {{ $t('exercise.report_misuse_to_administrators') }}
    </ReportDialog>

    <!--
    <pre>{{ submission }}</pre>
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
    -->
  </v-container>
</template>
<script>
import cefr from '~/mixins/cefr.js';
import langs_available from '~/mixins/langs_available.js';
import unit_component from '~/mixins/unit_component.js';
export default {
  name: 'Exercise',
  mixins: [langs_available, cefr, unit_component],
  data: () => ({
    //submission: {},
    all_readonly: false,
    all_silent: true,
    mistake_dialog: false,
    misuse_dialog: false,
    submitted: false,
  }),
  async asyncData({ route, params, $auth }) {
    const id = process.server ? route.params.id : params.id;
    let exercise;
    if (id) {
      exercise = (await $auth.axios.get(`/v1/exercises/${id}/`)).data;
    }
    return {
      id,
      exercise,
    };
  },
  computed: {
    user_logged_in() {
      const authUser = this.$store.getters['authenticator/authUser'];
      if (!authUser) return false;
      return true;
    },
    user_is_creator() {
      const authUser = this.$store.getters['authenticator/authUser'];
      if (!authUser) return false;
      return this.exercise.created_by === authUser.username;
    },
  },
  methods: {
    async create_exam() {
      if (
        !this.user_is_creator &&
        !(await this.$refs.msgbox.confirm(
          this.$t('exercise.create_exam_confirm')
        ))
      )
        return;
      this.$router.push(
        this.localePath(`/exam_editor?new_from=${this.exercise.lid}`)
      );
    },
    async remove() {
      if (
        !(await this.$refs.msgbox.confirm(this.$t('exercise.delete_confirm')))
      )
        return;

      try {
        await this.$auth.axios.delete(`/v1/exercises/${this.id}`);
        this.$router.push('/');
      } catch (e) {
        console.error({ ...e });
        await this.$refs.msgbox.alert(`Error ${e.response.status}`);
      }
    },
    create_submission() {
      // create the submission object to be sent to the server

      const submission = {};

      const username = this.$store.getters['authenticator/authUser'].username;
      if (username) {
        //submission.created_by = username
        // this field will be written by the backend
      } else {
        submission.guest = 'x'; // TODO: display name
      }

      submission.created = new Date();
      submission.exercise_lid = this.id;
      submission.exam_lid = null;
      submission.exercise = { ...this.exercise };
      submission.exercise.data.sheet = this.exercise.data.sheet.map((unit) => ({
        ...unit,
        solved: this.$refs[`unit-${unit._key}`][0].get_solved(),
      }));

      return submission;
    },
    async liked() {
      await this.$nuxt.refresh();
    },
    async submit() {
      // show the results of the quiz

      this.submitted = true;
      window.scrollTo({ top: 0, behavior: 'smooth' });

      this.all_silent = false;
      this.all_readonly = true;

      if (!this.user_logged_in) return;

      const submission = this.create_submission();
      try {
        await this.$auth.axios.post('/v1/submissions/', submission);
      } catch (e) {
        console.error({ ...e });
        await this.$refs.msgbox.alert(this.$t('exercise.error'));
      }
    },
    window_print() {
      window.print();
    },
  },
  head() {
    return {
      title: this.exercise.name,
    };
  },
};
</script>
<style scoped>
.pre-line {
  white-space: pre-line;
}
</style>
