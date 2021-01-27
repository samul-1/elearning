<template>
  <div class="question-box">
    <p><strong>Domanda</strong></p>
    <!-- <p class="question-text" v-html="text"></p>-->
    <vue-mathjax :formula="text" :safe="false"></vue-mathjax>

    <p
      v-for="(answer, index) in answers"
      :key="index"
      :class="{
        correct: index == correctAnswerIndex && correctShown,
        incorrect: index != correctAnswerIndex && correctShown,
      }"
    >
      <strong>{{ index + 1 }}.</strong>&nbsp;
      <!--<span v-html="answer"></span>-->
      <vue-mathjax :formula="answer" :safe="false"></vue-mathjax>

      <span class="comment" v-if="index == correctAnswerIndex"
        ><em class="text-muted">(Risposta corretta)</em></span
      >
    </p>
    <p><strong>Soluzione</strong></p>
    <vue-mathjax :formula="solution" :safe="false"></vue-mathjax>
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
  },
  mounted() {},
  data: () => {
    return {
      correctShown: false,
      solShown: false,
    };
  },
  methods: {},
  computed: {},
};
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.question-box {
  border: none;
  border-radius: 0.8rem;
  padding: 1rem 2.5rem;
  box-shadow: 0px 0px 3px 0px rgba(19, 19, 19, 0.8);
}

.correct {
  color: green !important;
  text-shadow: 0 0 1.5px #228b22;
}

.incorrect {
  color: red !important;
  text-shadow: 0 0 1.5px #ff4500;
  opacity: 0.5;
}

.comment {
  margin-left: 50px;
}
</style>
