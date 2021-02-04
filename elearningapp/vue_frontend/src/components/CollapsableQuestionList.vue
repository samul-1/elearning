<template>
  <div class="list-wrapper">
    <p :class="{ 'text-muted': !questions.length }">
      {{ text }}
      <b-button
        class="small-button"
        @click="shown = !shown"
        v-b-toggle="'collapse-' + index"
        variant="primary"
        :disabled="!questions.length"
        >{{ shownText }}
      </b-button>
    </p>
    <b-collapse :id="'collapse-' + index" class="mt-2">
      <b-card class="transparent-card no-border">
        <div class="card-text">
          <SeenQuestion
            v-for="(item, idx) in questions"
            :key="idx"
            :text="item.text"
            :answers="item.answers"
            :solution="item.solution"
            :correctAnswerIndex="item.correctAnswerIndex"
            :givenAnswer="item.yourAnswer"
            :questionId="'list' + index + '-' + idx"
            :questionOnly="questionOnly"
            :wrongAnswersPercentage="item.wrongAnswersPercentage"
          />
        </div>
      </b-card>
    </b-collapse>
  </div>
</template>

<script>
import SeenQuestion from "./SeenQuestion.vue";

export default {
  name: "CollapsableQuestionList",
  components: {
    SeenQuestion,
  },
  props: {
    text: String,
    questions: Array,
    index: String,
    questionOnly: {
      type: Boolean,
      default: false,
    },
    wrongAnswerPercentage: {
      type: Number,
      default: null,
    },
  },
  mounted() {},
  data: () => {
    return {
      shown: false,
    };
  },
  methods: {},
  computed: {
    shownText() {
      return this.shown ? "Nascondi" : "Mostra";
    },
  },
};
</script>

<style>
@import "../../../static/question-styles.css";

/* .transparent-card {
  background-color: transparent !important;
}

.list-wrapper {
  padding-bottom: 10px;
} */
</style>
