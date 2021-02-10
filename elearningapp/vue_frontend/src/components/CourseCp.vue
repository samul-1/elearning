<template>
  <div>
    <h1 id="course_title">Pannello di controllo di {{ courseName }}</h1>
    <br />
    <div class="grid two-col-grid dashboard-grid">
      <div>
        <a
          v-if="admin || myPermissions.can_add_questions"
          class="w-100 btn btn-dark dashboard-btn mb-3"
          :href="addQuestionsApiUrl"
        >
          <font-awesome-icon class="mr-1" icon="plus-circle" />
          Aggiungi domande
        </a>
        <a
          v-if="admin || myPermissions.can_edit_questions"
          class="w-100 btn btn-dark dashboard-btn"
          :href="editQuestionsApiUrl"
        >
          <font-awesome-icon class="mr-1" icon="list" />
          Visualizza / modifica domande
        </a>
        <b-button
          v-if="admin || myPermissions.can_manage_contributors"
          variant="dark"
          class="w-100 mb-0 btn btn-dark dashboard-btn"
          v-b-modal="'assistant-modal'"
        >
          <font-awesome-icon class="mr-1" icon="user-shield" />
          Gestisci assistenti
        </b-button>
      </div>
      <div class="grid">
        <div class="grid three-col rem-1-gap">
          <div class="course-stat">
            <p class="heading">Iscritti</p>
            <p class="data">{{ numberOfSubscribers }}</p>
          </div>
          <div class="course-stat">
            <p style="letter-spacing: -1px" class="heading">Test svolti</p>
            <p class="data">{{ numberOfTestsTaken }}</p>
          </div>
          <div class="course-stat">
            <p class="heading">Media</p>
            <p class="data">{{ averageScore }}</p>
          </div>
          <div class="stats" style="grid-column: 1 / span 3">
            <i class="fas fa-link mr-1"></i>
            Link al corso per gli studenti:
            <a :href="'/course/' + courseId">
              {{ "http://127.0.0.1/course/" + courseId }}</a
            >
          </div>
        </div>
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
      <div style="align-self: start" v-if="reports.length" class="stats">
        <p class="stat-title">Segnalazioni</p>
        <ul class="report-list">
          <li
            class="mb-1"
            :class="{ 'resolved-issue': report.resolved }"
            v-for="(report, index) in reports"
            :key="index"
          >
            <span class="text-muted timestamp">{{
              formattedTimestamp(new Date(report.timestamp))
            }}</span>
            {{ report.username }}
            <b-button
              class="py-0 px-2 btn-rounded"
              variant="outline-primary"
              @click="showReport(report)"
              >Mostra</b-button
            >
          </li>
        </ul>
      </div>
      <div style="align-self: start" class="stats">
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
    <b-modal
      :ok-only="true"
      size="xl"
      title="Gestisci assistenti"
      id="assistant-modal"
    >
      <CoursePermissionManager
        style="max-height: 65vh; overflow-y: auto"
        :apiUsersUrl="apiUsersUrl"
        :updatePermissionApiUrl="updatePermissionApiUrl"
        :userId="userId"
      ></CoursePermissionManager>
    </b-modal>
    <b-modal
      :ok-only="true"
      size="xl"
      id="report-modal"
      title="Dettagli segnalazione"
    >
      <p>
        <strong>Inviata da:</strong> {{ shownReport.username }} ({{
          shownReport.firstName
        }}
        {{ shownReport.lastName }}), <strong>in data</strong>
        {{ formattedTimestamp(new Date(shownReport.timestamp)) }}
      </p>
      <p>
        <strong>Stato:</strong>
        <span
          class="ml-1"
          :class="{
            failed: !shownReport.resolved,
            passed: shownReport.resolved,
          }"
          >{{ shownReport.resolved ? "risolta" : "non risolta" }}</span
        >
        <b-button
          v-if="!shownReport.resolved"
          @click="closeReport()"
          class="ml-1 py-0"
          variant="outline-success"
          >Contrassegna come risolta</b-button
        >
      </p>
      <p>
        <strong>Relativa alla domanda:</strong>

        <a :href="editQuestionsApiUrl + shownReport.question.questionId"
          ><b-button class="ml-3 py-0" variant="outline-secondary"
            ><i class="fas fa-edit"></i> Modifica questa domanda</b-button
          ></a
        >
      </p>
      <div class="grid two-to-one-col rem-1-gap">
        <QuestionPreview
          :text="shownReport.question.text"
          :answers="shownReport.question.answers"
          :solution="shownReport.question.solution"
          :correctAnswerIndex="shownReport.question.correctAnswerIndex"
        ></QuestionPreview>
        <div class="self-align-start">
          <p><strong>Testo della segnalazione</strong></p>
          <vue-mathjax
            :formula="shownReport.text"
            :safe="false"
            :options="mathjaxOptions"
          ></vue-mathjax>
        </div>
      </div>
    </b-modal>
    <transition name="overlay-text">
      <div class="overlay-card" v-if="success">
        <b-card bg-variant="light" text-variant="black">
          <b-card-text class="grid-card">
            <font-awesome-icon
              class="correct"
              icon="check-circle"
              style="width: 80px; height: 80px"
            />
            Segnalazione chiusa con successo
          </b-card-text>
        </b-card>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from "axios";

// Fontawesome
import { library } from "@fortawesome/fontawesome-svg-core";
import CollapsableQuestionList from "./CollapsableQuestionList.vue";
import CoursePermissionManager from "./CoursePermissionManager.vue";
import QuestionPreview from "./QuestionPreview.vue";
import { VueMathjax } from "vue-mathjax";

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
    CoursePermissionManager,
    QuestionPreview,
    "vue-mathjax": VueMathjax,
  },
  props: {
    // TODO get course url as a prop
    userId: {
      type: Number,
      default: null,
    },
    reports: {
      type: Array,
      default: () => [],
    },
    courseName: String,
    courseId: Number,
    averageScore: Number,
    numberOfSubscribers: Number,
    numberOfTestsTaken: Number,
    hardestQuestions: Array,
    lastActions: Array,
    apiUsersUrl: String,
    admin: Boolean,
    myPermissions: {
      type: Object,
      default: () => {},
    },
    updatePermissionApiUrl: String,
    addQuestionsApiUrl: String,
    editQuestionsApiUrl: String,
    updateReportApiUrl: String,
  },
  mounted() {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  },
  data: () => {
    return {
      success: false,
      shownReport: { question: {} },
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
    showReport(report) {
      console.log(report);
      this.shownReport = report;
      this.$bvModal.show("report-modal");
    },
    closeReport() {
      this.loading = true;
      const putData = {
        reportId: this.shownReport.reportId, // this is the user whose permissions were being edited
        resolved: true,
      };
      this.loading = true;

      console.log(putData);

      axios
        .put(this.updateReportApiUrl, putData)
        .then((response) => {
          console.log(response);
          this.showConfirmationAndClose();
          this.loading = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    showConfirmationAndClose() {
      this.$bvModal.hide("report-modal");
      this.shownReport.resolved = true;

      // show success message and hide it programmatically
      this.success = true;
      setTimeout(() => {
        this.success = false;
      }, 2000);
    },
  },
};
</script>

<style scoped>
@import "../../../static/dashboard-styles.css";
</style>
