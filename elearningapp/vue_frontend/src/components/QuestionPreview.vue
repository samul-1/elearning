<template>
  <div :class="{ 'question-box': styled }">
    <p><strong>Domanda</strong></p>
    <vue-mathjax :formula="text" :safe="false"></vue-mathjax>

    <p v-for="(answer, index) in answers" :key="index">
      <strong>{{ parseInt(index + 1) }}.</strong>&nbsp;
      <vue-mathjax :formula="answer" :safe="false"></vue-mathjax>

      <span class="comment" v-if="index + 1 == correctAnswerIndex"
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
    styled: {
      type: Boolean,
      default: true,
    },
  },
  mounted() {},
  data: () => {
    return {};
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

.comment {
  margin-left: 50px;
}
</style>
