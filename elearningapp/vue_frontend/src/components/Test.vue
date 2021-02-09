<template>
  <div>
    <b-spinner
      style="position: fixed; top: 50%; left: 50%"
      v-if="loading"
      label="Loading..."
    ></b-spinner>
    <div class="container-fluid h-100">
      <div style="float: right; position: sticky; top: 70px">
        <button class="btn btn-dark" ref="sendAnswers" @click="sendAnswers()">
          <font-awesome-icon class="mr-1" icon="check" />
          Invia risposte
        </button>
      </div>
      <div class="row">
        <Question
          v-for="(question, index) in questions"
          :key="index"
          :text="question.text"
          :answers="question.answers"
          :questionIndex="index"
          @answer="registerAnswer($event, index)"
        />
      </div>

      <b-modal
        :ok-only="true"
        :ok-title="'Torna al corso'"
        @hide="toCoursePage"
        size="xl"
        id="outcome-modal"
      >
        <template #modal-header="{}">
          <h1>Risultati</h1>
        </template>
        <template #default="{}">
          <div class="container">
            <div class="row">
              <div class="col-md-3 col-10">
                <p>
                  <strong>Punteggio: </strong>
                  <span class="score">{{ outcomeObj.score }}</span>
                </p>
              </div>
              <div class="col-3">
                <strong>Risposte corrette:</strong>
                {{ outcomeObj.correctlyAnsweredQuestions.length }}
              </div>
              <div class="col-3">
                <strong>Risposte errate:</strong>
                {{ outcomeObj.incorrectlyAnsweredQuestions.length }}
              </div>
              <div class="col-md-3 col-4">
                <strong>Risposte non date:</strong>
                {{ outcomeObj.unansweredQuestions.length }}
              </div>
              <div class="col-10">
                <p>
                  <strong>Esito: </strong>
                  <span class="passed" v-if="outcomeObj.passing"
                    ><strong>superato</strong></span
                  >
                  <span class="failed" v-else
                    ><strong>non superato</strong></span
                  >
                </p>
              </div>
            </div>
          </div>

          <div v-if="outcomeObj.correctlyAnsweredQuestions.length">
            <p>
              Domande a cui hai risposto correttamente:
              <b-button
                @click="corrShown = !corrShown"
                class="small-button"
                v-b-toggle.collapse-1
                variant="primary"
                >{{ corrShownText }}</b-button
              >
            </p>
            <b-collapse id="collapse-1" class="mt-2">
              <b-card>
                <div class="card-text">
                  <SeenQuestion
                    v-for="(
                      item, index
                    ) in outcomeObj.correctlyAnsweredQuestions"
                    :key="index"
                    :text="item.text"
                    :answers="item.answers"
                    :solution="item.solution"
                    :correctAnswerIndex="item.correctAnswerIndex"
                    :givenAnswer="item.yourAnswer"
                    :questionIddex="'1_' + index"
                    :questionId="item.questionId"
                    :sendReportApiUrl="sendReportApiUrl"
                  />
                </div>
              </b-card>
            </b-collapse>
          </div>
          <div v-if="outcomeObj.incorrectlyAnsweredQuestions.length">
            <p>
              Domande a cui hai risposto in maniera errata:
              <b-button
                class="small-button"
                @click="incorrShown = !incorrShown"
                v-b-toggle.collapse-2
                variant="primary"
                >{{ incorrShownText }}</b-button
              >
            </p>
            <b-collapse id="collapse-2" class="mt-2">
              <b-card>
                <div class="card-text">
                  <SeenQuestion
                    v-for="(
                      item, index
                    ) in outcomeObj.incorrectlyAnsweredQuestions"
                    :key="index"
                    :text="item.text"
                    :answers="item.answers"
                    :solution="item.solution"
                    :correctAnswerIndex="item.correctAnswerIndex"
                    :givenAnswer="item.yourAnswer"
                    :questionIndex="'2_' + index"
                    :questionId="item.questionId"
                    :sendReportApiUrl="sendReportApiUrl"
                  />
                </div>
              </b-card>
            </b-collapse>
          </div>
          <div v-if="outcomeObj.unansweredQuestions.length">
            <p>
              Domande a cui non hai risposto:
              <b-button
                class="small-button"
                @click="unansShown = !unansShown"
                v-b-toggle.collapse-3
                variant="primary"
                >{{ unansShownText }}</b-button
              >
            </p>
            <b-collapse id="collapse-3" class="mt-2">
              <b-card>
                <div class="card-text text-justify-center">
                  <SeenQuestion
                    v-for="(item, index) in outcomeObj.unansweredQuestions"
                    :key="index"
                    :text="item.text"
                    :answers="item.answers"
                    :solution="item.solution"
                    :correctAnswerIndex="item.correctAnswerIndex"
                    :givenAnswer="item.yourAnswer"
                    :questionIndex="'3_' + index"
                    :questionId="item.questionId"
                    :sendReportApiUrl="sendReportApiUrl"
                  />
                </div>
              </b-card>
            </b-collapse>
          </div>
        </template>
      </b-modal>
    </div>
  </div>
</template>

<script>
import Question from "./Question.vue";

import SeenQuestion from "./SeenQuestion.vue";

// Fontawesome
import { library } from "@fortawesome/fontawesome-svg-core";
import { faCheck } from "@fortawesome/free-solid-svg-icons";

library.add(faCheck);

import axios from "axios";

export default {
  name: "Test",
  components: {
    Question,
    SeenQuestion,
  },
  props: {
    sendReportApiUrl: String,
    questions: Array,
    courseDashboardUrl: String,
    sendAnswersApiUrl: String,
  },
  data: () => {
    return {
      answers: {},
      outcomeObj: {},
      corrShown: false,
      incorrShown: false,
      unansShown: false,
      loading: false,
    };
  },
  mounted() {
    for (let i = 0; i < this.questions.length; i++) {
      this.answers[i] = -1;
    }
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  },
  computed: {
    // TODO convert these to template syntax
    corrShownText() {
      return this.corrShown ? "Nascondi" : "Mostra";
    },

    incorrShownText() {
      return this.incorrShown ? "Nascondi" : "Mostra";
    },

    unansShownText() {
      return this.unansShown ? "Nascondi" : "Mostra";
    },
  },
  methods: {
    // called upon receiving answer event from a child Question component
    registerAnswer(answerIndex, questionIndex) {
      this.answers[questionIndex] = answerIndex;
    },

    // sends the answers to the server via POST and shows the outcome
    sendAnswers() {
      const postData = JSON.stringify(this.answers);
      console.log(postData);
      this.loading = true;
      axios
        .post(this.sendAnswersApiUrl, postData)
        .then((response) => {
          this.outcomeObj = response.data;
          this.$root.$emit("bv::show::modal", "outcome-modal", "#sendAnswers");

          console.log(response);
          this.loading = false;
        })
        .catch((error) => {
          alert(error);
          console.log(error);
        });
    },
    toCoursePage() {
      window.location.href = this.courseDashboardUrl;
    },
  },
};
</script>

<style>
@import "../../../static/test-styles.css";
</style>
