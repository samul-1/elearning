<template>
  <div>
    <h1 id="course_title">Pannello di controllo di {{ courseName }}</h1>
    <br />
    <div class="grid two-col-grid dashboard-grid">
      <div>
        <a :href="'/add_question/' + courseId"
          ><button class="btn btn-dark dashboard-btn mb-3">
            <font-awesome-icon class="mr-1" icon="plus-circle" />
            Aggiungi domande
          </button></a
        >
        <a :href="'/edit_question/' + courseId"
          ><button
            style="margin-bottom: 0 !important"
            class="btn btn-dark dashboard-btn"
          >
            <font-awesome-icon class="mr-1" icon="list" />
            Visualizza / modifica domande
          </button></a
        >
        <button class="btn btn-dark dashboard-btn mt-3">
          <font-awesome-icon class="mr-1" icon="user-shield" />
          Gestisci assistenti
        </button>
      </div>
      <div class="stats">
        <p class="stat-title">Statistiche del corso</p>
        <p>
          Iscritti al corso: <span class="data">{{ numberOfSubscribers }}</span>
        </p>
        <p>
          Test effettuati: <span class="data">{{ numberOfTestsTaken }}</span>
        </p>
        <p>
          Punteggio medio: <span class="data">{{ averageScore }}</span>
        </p>
      </div>
      <div style="align-self: start" class="stats">
        <p class="stat-title">Ultime azioni</p>
        <ul class="log-list">
          <li v-for="(action, index) in lastActions" :key="index">
            <span class="text-muted timestamp">{{
              formattedTimestamp(new Date(action.timestamp))
            }}</span>
            {{ action.user }} ha
            {{ action.action == "E" ? "modificato" : "creato" }}
            <a :href="'/edit_question/' + courseId + '/' + action.questionId"
              >una domanda</a
            >
          </li>
        </ul>
      </div>
      <div class="stats">
        <p class="stat-title">
          {{ "Le " + hardestQuestions.length + " domande più sbagliate" }}
        </p>
        <CollapsableQuestionList
          :index="1"
          :questions="hardestQuestions"
          :questionOnly="true"
        ></CollapsableQuestionList>
      </div>
    </div>
  </div>
</template>

<script>
// Fontawesome
import { library } from "@fortawesome/fontawesome-svg-core";
import CollapsableQuestionList from "./CollapsableQuestionList.vue";
import {
  faList,
  faPlusCircle,
  faUserShield,
} from "@fortawesome/free-solid-svg-icons";

library.add(faPlusCircle);
library.add(faList);
library.add(faUserShield);

export default {
  name: "CourseCp",
  components: {
    CollapsableQuestionList,
  },
  props: {
    courseName: String,
    courseId: Number,
    averageScore: Number,
    numberOfSubscribers: Number,
    numberOfTestsTaken: Number,
    hardestQuestions: Array,
    lastActions: Array,
  },
  mounted() {},
  data: () => {
    return {};
  },
  methods: {
    formattedTimestamp(date) {
      return (
        (date.getDate() < 10 ? "0" + date.getDate() : date.getDate() + 1) +
        "/" +
        (date.getMonth() + 1 < 10
          ? "0" + (date.getMonth() + 1)
          : date.getMonth() + 1) +
        "/" +
        date.getFullYear() +
        ", " +
        (date.getHours() < 10 ? "0" + date.getHours() : date.getHours()) +
        ":" +
        (date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes())
      );
    },
  },
};
</script>

<style scoped>
@import "../../../static/dashboard-styles.css";

/* .stats {
  border: 1px solid #dbdbdb;
  border-radius: 0.8rem;
  padding: 1rem;
  text-align: center;
}

.stats .data {
  font-weight: bold;
}

.grid div {
  align-self: center;
} */
</style>
