<template>
  <div class="seen-question-box col-10">
    <p class="question-text">
      <span v-html="text"></span>
    </p>

    <div v-if="wrongAnswersPercentage != null">
      <div class="w-100 progress-border">
        <div
          class="progress-amount bg-danger"
          :style="'width:' + wrongAnswersPercentage + '%'"
        ></div>
        <span class="average-text">
          {{ wrongAnswersPercentage.toFixed(1) }}% di errori
        </span>
      </div>
      <!-- <span>
        Sbagliata nel{{ String(wrongAnswersPercentage)[0] == "8" ? "l'" : " "
        }}{{ wrongAnswersPercentage.toFixed(1) }}% dei test</span
      > -->
    </div>
    <div v-if="!questionOnly">
      <p
        v-for="(answer, index) in answers"
        :key="index"
        class="answer-p"
        :class="{
          correct: index + 1 == correctAnswerIndex && correctShown,
          incorrect: index + 1 != correctAnswerIndex && correctShown,
        }"
      >
        <strong>{{ index + 1 }}.</strong>&nbsp;
        <!--{{ answer }}-->
        <span v-html="answer"></span>

        <!-- <vue-mathjax
          :formula="answer"
          :safe="false"
          :options="mathjaxOptions"
        ></vue-mathjax> -->

        <span class="comment" v-if="index + 1 == givenAnswer"
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
          <!-- <vue-mathjax
            :formula="solution"
            :safe="false"
            :options="mathjaxOptions"
          ></vue-mathjax> -->
          <span v-html="solution"></span>
        </b-collapse>
      </p>
    </div>
  </div>
</template>

<script>
// import { VueMathjax } from "vue-mathjax";

export default {
  name: "SeenQuestion",
  components: {
    // "vue-mathjax": VueMathjax,
  },
  props: {
    text: String,
    solution: String,
    answers: Array,
    correctAnswerIndex: Number,
    givenAnswer: Number,
    questionId: [String, Number],
    questionOnly: {
      type: Boolean,
      default: false,
    },
    wrongAnswersPercentage: {
      type: Number,
      default: null,
    },
  },
  data: () => {
    return {
      correctShown: false,
      solShown: false,
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
@import "../../../static/question-styles.css";

/* .seen-question-box {
  border: none;
  margin: 2rem;
  border-radius: 0.8rem;
  padding: 1rem 2.5rem;
  box-shadow: 0px 0px 3px 0px rgba(19, 19, 19, 0.8);
}

.comment {
  margin-left: 50px;
} */
</style>
