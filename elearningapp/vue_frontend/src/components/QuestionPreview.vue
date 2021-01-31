<template>
  <div :class="{ 'question-preview-box': styled }">
    <p><strong>Domanda</strong></p>
    <vue-mathjax
      :formula="text"
      :safe="false"
      :options="mathjaxOptions"
    ></vue-mathjax>

    <p
      class="answer-paragraph answer-paragraph-full"
      v-for="(answer, index) in answers"
      :key="index"
    >
      <strong>{{ parseInt(index + 1) }}.</strong>&nbsp;
      <vue-mathjax
        :formula="answer"
        :safe="false"
        :options="mathjaxOptions"
      ></vue-mathjax>

      <span class="comment" v-if="index + 1 == correctAnswerIndex"
        ><em class="text-muted">(Risposta corretta)</em></span
      >
    </p>
    <p><strong>Soluzione</strong></p>
    <vue-mathjax
      :formula="solution"
      :safe="false"
      :options="mathjaxOptions"
    ></vue-mathjax>
  </div>
</template>

<script>
import { VueMathjax } from "vue-mathjax";

export default {
  name: "QuestionPreview",
  components: {
    "vue-mathjax": VueMathjax,
  },
  props: {
    text: String,
    solution: String,
    answers: Array,
    correctAnswerIndex: Number,
    questionId: [String, Number],
    styled: {
      type: Boolean,
      default: true,
    },
  },
  mounted() {},
  data: () => {
    return {
      mathjaxOptions: {
        tex2jax: {
          inlineMath: [
            ["$", "$"],
            ["\\(", "\\)"],
          ],
          displayMath: [
            ["$$", "$$"],
            ["[", "]"],
          ],
          processEscapes: true,
          processEnvironments: true,
        },
      },
    };
  },
  methods: {},
  computed: {},
};
</script>

<style scoped>
@import "../../../static/question-styles.css";

/* .question-preview-box {
  border: none;
  border-radius: 0.8rem;
  padding: 1rem 2.5rem;
  box-shadow: 0px 0px 3px 0px rgba(19, 19, 19, 0.8);
}

.comment {
  margin-left: 50px;
}

.answer-paragraph:nth-of-type(2) {
  padding-top: 1.2rem;
  position: relative;
}

.answer-paragraph:nth-of-type(2):before {
  content: "";
  border-top: 1px solid rgb(211, 211, 211);
  box-shadow: 0 0 3px rgba(114, 114, 114, 0.2);
  position: absolute;
  top: 0;
  width: 100%;
} */
</style>
