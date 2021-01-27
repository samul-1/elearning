<template>
  <div class="question-box col-10">
    <p class="question-text">
      <!--{{ text }}-->
      <vue-mathjax :formula="text" :safe="false"></vue-mathjax>
    </p>
    <p
      v-for="(answer, index) in answers"
      :key="index"
      :class="{
        correct: index == correctAnswerIndex && correctShown,
        incorrect: index != correctAnswerIndex && correctShown,
      }"
    >
      <strong>{{ index }}.</strong>&nbsp;
      <!--{{ answer }}-->
      <vue-mathjax :formula="answer" :safe="false"></vue-mathjax>

      <span class="comment" v-if="index == givenAnswer"
        ><em :class="{ 'text-muted': !correctShown }"
          >(La tua risposta)</em
        ></span
      >
    </p>
    <p class="text-muted" v-if="givenAnswer == -1">
      <em>(Non hai risposto a questa domanda)</em>
    </p>
    <p>
      <strong>Risposta corretta: </strong>
      <b-button
        @click="correctShown = !correctShown"
        variant="outline-success"
        class="small-button"
        >{{ showCorrAnsText }}</b-button
      >
    </p>
    <p>
      <strong>Soluzione: </strong>
      <b-button
        @click="solShown = !solShown"
        v-b-toggle="'collapse-' + questionId"
        variant="outline-primary"
        class="small-button"
        >{{ showSolText }}</b-button
      >
      <br />
      <b-collapse :id="'collapse-' + questionId" class="mt-2">
        {{ solution }}
      </b-collapse>
    </p>
  </div>
</template>

<script>
import { VueMathjax } from "vue-mathjax";

export default {
  name: "SeenQuestion",
  components: {
    "vue-mathjax": VueMathjax,
  },
  props: {
    text: String,
    solution: String,
    answers: Object,
    correctAnswerIndex: Number,
    givenAnswer: Number,
    questionId: [String, Number],
  },
  data: () => {
    return {
      correctShown: false,
      solShown: false,
    };
  },
  computed: {
    showCorrAnsText() {
      return this.correctShown ? "Nascondi" : "Mostra";
    },

    showSolText() {
      return this.solShown ? "Nascondi" : "Mostra";
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
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
  /* -webkit-box-shadow: 1px 1px 3px 0px rgba(0,0,0,0.75);
  -moz-box-shadow: 1px 1px 3px 0px rgba(0,0,0,0.75);
  box-shadow: 1px 1px 3px 0px rgba(0,0,0,0.75);
  border: 1px solid grey;
  border-radius: 3px;
  overflow-x: auto;
  background-color: #f2f2f2; */
  border: none;
  margin: 2rem;
  border-radius: 0.8rem;
  padding: 1rem 2.5rem;
  box-shadow: 0px 0px 3px 0px rgba(19, 19, 19, 0.8);
}

.comment {
  margin-left: 50px;
}
</style>
