<template>
  <div>
    <b-spinner
      style="position: fixed; top: 50%; left: 50%; color: black"
      v-if="loading"
      label="Loading..."
    ></b-spinner>
    <h2>Domande già viste</h2>

    <div class="grid two-to-one-col-fr one-col-mobile">
      <div style="align-self: center">
        <p>
          Le domande presenti in questa pagina non ricompariranno nei prossimi
          test che effettuerai.
        </p>
      </div>
      <b-button
        @click="showConfirmationModal"
        :disabled="!questionsData.length"
        variant="outline-danger"
      >
        <font-awesome-icon class="mr-1" icon="trash-alt" />

        Cancella cronologia domande</b-button
      >
    </div>
    <div class="mt-3" v-if="!questionsData.length">
      <b-card bg-variant="light" text-variant="black">
        <b-card-text class="grid-card">
          <font-awesome-icon
            class="mr-1"
            icon="exclamation-circle"
            style="width: 80px; height: 80px"
          />

          <span>Non hai ancora visto alcuna domanda.</span>
        </b-card-text>
      </b-card>
    </div>

    <div class="">
      <div class="grid list-grid" v-infinite-scroll="loadMoreQuestions">
        <SeenQuestion
          v-for="(item, index) in questionsData"
          :key="index"
          :text="item.question.text"
          :answers="item.question.answers"
          :solution="item.question.solution"
          :correctAnswerIndex="item.question.correctAnswerIndex"
          :givenAnswer="item.givenAnswer"
          :questionId="item.question.questionId"
          :sendReportApiUrl="sendReportApiUrl"
        />
      </div>
      <p class="text-center mt-2 link" @click="loadMoreQuestions()">Carica più domande</p>
    </div>
    <b-modal size="lg" id="confirmation-modal">
      <template #modal-header="{}">
        <h3>Conferma operazione</h3>
      </template>
      <template #default="{}">
        <p>
          Confermi l'operazione? Le domande che hai già visto potrebbero
          ricomparire nei prossimi test.
        </p></template
      >

      <template #modal-footer="{ cancel }">
        <!-- Button with custom close trigger value -->
        <b-button variant="danger" @click="confirmHistoryDeletion()"
          >Conferma</b-button
        >

        <b-button @click="cancel">Annulla</b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import SeenQuestion from "./SeenQuestion.vue";
import axios from "axios";
import infiniteScroll from "vue-infinite-scroll";

// Fontawesome
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faTrashAlt,
  faExclamationCircle,
} from "@fortawesome/free-solid-svg-icons";

library.add(faTrashAlt);
library.add(faExclamationCircle);

export default {
  name: "QuestionHistory",
  components: {
    SeenQuestion,
  },
  directives: {
    infiniteScroll,
  },
  props: {
    getSeenQuestionsApiUrl: String,
    deleteQuestionHistoryApiUrl: String,
    sendReportApiUrl: String,
    questions: Array,
    userId: Number,
    courseId: Number,
  },
  data: () => {
    return {
      questionsData: [],
      loading: false,
      filterByCategory: "",
    };
  },
  mounted() {
    this.questionsData = this.questions;
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  },
  methods: {
    showConfirmationModal() {
      this.$root.$emit("bv::show::modal", "confirmation-modal");
    },
    confirmHistoryDeletion() {
      this.questionsData = [];
      this.$root.$emit("bv::hide::modal", "confirmation-modal");
      axios
        .delete(
          this.deleteQuestionHistoryApiUrl
        )
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          alert(error);
          console.log(error);
        });
    },
    loadMoreQuestions(overwrite = false) {
      if (overwrite) {
        this.questionsData = [];
      }
      this.loading = true;
      axios
        .get(
          this.getSeenQuestionsApiUrl +
            this.maxQuestionId +
            "/" +
            (this.filterByCategory.length ? this.filterByCategory + "/" : "")
        )
        .then((response) => {
          this.loading = false;
          console.log(response.data);
          this.questionsData.push(...response.data);
        })
        .catch((error) => {
          // alert(error);
          console.log(error);
        });
    },
  },
  computed: {
    // returns the highest question id present: used to poll the server for subsequent questions
    // (which are retrieved sorted by id)
    maxQuestionId() {
      if (!this.questionsData.length) {
        return 0;
      }
      return Math.max(...this.questionsData.map((q) => parseInt(q.questionId)));
    },
  },
};
</script>

<style scoped>
@import "../../../static/question-styles.css";
</style>
