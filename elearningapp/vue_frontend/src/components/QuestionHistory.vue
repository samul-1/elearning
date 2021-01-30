<template>
  <div>
    <h2>Domande già viste</h2>

    <div class="grid two-to-one-col-fr">
      <div style="align-self: center">
        Le domande presenti in questa pagina non ricompariranno nei prossimi
        test che effettuerai.
      </div>
      <b-button
        @click="showConfirmationModal"
        :disabled="!questions.length"
        variant="outline-danger"
      >
        <font-awesome-icon class="mr-1" icon="trash-alt" />

        Cancella cronologia domande</b-button
      >
    </div>
    <div class="mt-3" v-if="!questions.length">
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
      <div class="grid list-grid">
        <SeenQuestion
          v-for="(item, index) in questions"
          :key="index"
          :text="item.question.text"
          :answers="item.question.answers"
          :solution="item.question.solution"
          :correctAnswerIndex="item.question.correctAnswerIndex"
          :givenAnswer="item.givenAnswer"
          :questionId="index"
        />
      </div>
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
        <b-button variant="danger" @click="confirm">Conferma</b-button>

        <b-button @click="cancel">Annulla</b-button>
      </template>
      <div class="d-block">Hello From My Modal!</div>
    </b-modal>
  </div>
</template>

<script>
import SeenQuestion from "./SeenQuestion.vue";
import axios from "axios";

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
  props: {
    questions: Array,
    userId: Number,
    courseId: Number,
  },
  mounted() {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  },
  methods: {
    showConfirmationModal() {
      this.$root.$emit("bv::show::modal", "confirmation-modal");
    },
    confirm() {
      this.questions = [];
      this.$root.$emit("bv::hide::modal", "confirmation-modal");
      axios
        .post(
          "http://127.0.0.1:8000/delete_question_history/" +
            this.userId +
            "/" +
            this.courseId +
            "/"
        )
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          alert(error);
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.grid-card {
  display: grid;
  grid-template-columns: 110px auto;
  align-items: center;
}
</style>
