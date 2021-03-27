<template>
  <div class="seen-question-box col-md-10" :class="{'col-12': !questionOnly, 'col-10 mx-auto': questionOnly }">
    <p class="question-text">
      <span v-html="text"></span>
    </p>

    <div v-if="wrongAnswersPercentage != null && questionOnly">
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
          v-b-toggle="'collapse-' + operatingIndex"
          variant="outline-primary"
          class="small-button"
          >{{ showSolText }}</b-button
        >
        <br />
        <b-collapse :id="'collapse-' + operatingIndex" class="mt-2">
          <!-- <vue-mathjax
            :formula="solution"
            :safe="false"
            :options="mathjaxOptions"
          ></vue-mathjax> -->
          <span v-html="solution"></span>
        </b-collapse>
      </p>
      <div class="grid" style="justify-items: end">
        <b-button
          v-if="!reportSuccessful"
          v-b-modal="'report-modal-' + questionId"
          class="py-0"
          variant="outline-danger"
        >
          <i class="far fa-flag mr-1"></i> Segnala errore</b-button
        >
        <span class="correct" v-else
          ><i class="fas fa-check mr-1"></i> Segnalazione ricevuta con
          successo</span
        >
      </div>
    </div>
    <b-modal
      :cancel-title="'Annulla'"
      :ok-title="'Invia segnalazione'"
      :ok-disabled="!reportText.length"
      size="lg"
      title="Segnala errore"
      :id="'report-modal-' + questionId"
      @ok="sendReport"
    >
      <p>Dicci cosa non va con questa domanda.</p>
      <vue-editor
        :editorToolbar="customToolbar"
        :id="'report-editor-' + questionId"
        class="big-editor"
        v-model="reportText"
      ></vue-editor>
    </b-modal>
  </div>
</template>

<script>
import { VueEditor } from "vue2-editor";
import axios from "axios";

export default {
  name: "SeenQuestion",
  components: {
    VueEditor,
  },
  props: {
    sendReportApiUrl: String,
    text: String,
    solution: String,
    answers: Array,
    correctAnswerIndex: Number,
    givenAnswer: Number,
    questionIndex: {
      type: [String, Number],
      default: null,
    },
    questionId: Number,
    questionOnly: {
      type: Boolean,
      default: false,
    },
    wrongAnswersPercentage: {
      type: Number,
      default: null,
    },
  },
  mounted() {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  },
  data: () => {
    return {
      reportSuccessful: false,
      customToolbar: [
        ["bold", "italic", "underline"],
        [{ list: "ordered" }, { list: "bullet" }],
        [{ color: [] }],
      ],
      reportText: "",
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
    // in views where each question is displayed once, such as QuestionHistory, each questionId appears once per page at most,
    // hence it can be used as a target for the toggle element. In TestHistory, the same question id may appear multple times,
    // therefore we use the prop questionIndex which is unique (and passed by CollapsibleQuestionList)
    // we still need the questionId prop to handle report sending
    operatingIndex() {
      return this.questionIndex ?? this.questionId;
    },
  },
  methods: {
    sendReport() {
      axios
        .post(this.sendReportApiUrl, {
          questionId: this.questionId,
          text: this.reportText,
        })
        .then((response) => {
          console.log(response);
          this.reportSuccessful = true;
        })
        .catch((error) => {
          alert(error);
          console.log(error);
        });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import "../../../static/question-styles.css";
</style>
