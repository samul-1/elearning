<template>
  <!-- :class="{ 'col-12': fullShown, 'col-3': !fullShown }" -->
  <div class="test-wrapper">
    <div
      class="test-preview"
      :class="{
        'preview-passed': this.passing,
        'preview-failed': !this.passing,
        'full-shown': this.fullShown,
      }"
      v-if="!fullShown"
    >
      <div class="test-date-preview">{{ formattedDate }}</div>
      <span class="test-score-preview">
        <span class="your-score-preview">{{ score }}</span> / {{ maxScore }}
      </span>
      <span
        class="test-outcome-preview"
        :class="{ passed: this.passing, failed: !this.passing }"
      >
        <font-awesome-icon
          class="mr-1"
          :icon="this.passing ? 'check' : 'times'"
        />
        {{ outcome }}
      </span>
      <b-button
        @click="
          fullShown = !fullShown;
          $emit('expanded', index, fullShown);
        "
        v-b-toggle="'collapse-' + index"
        :variant="this.passing ? 'outline-success' : 'outline-danger'"
        >Mostra dettagli
      </b-button>
    </div>
    <!-- // ! take care of lag when expanding test -->
    <div class="full taken-test" v-if="fullShown">
      <div class="row w-100">
        <div class="col-12 order-1 col-lg-4 order-lg-2 align-self-end">
          <p class="test-date">
            Test sostenuto in data {{ formattedTimestamp }}
          </p>
        </div>
        <div class="col-12 order-2 col-lg-8 order-lg-1 align-self-start">
          <h3 class="test-score">Punteggio: {{ score }}</h3>
        </div>
      </div>
      <p
        class="test-outcome"
        :class="{ passed: this.passing, failed: !this.passing }"
      >
        {{ outcome }}
      </p>

      <CollapsableQuestionList
        :sendReportApiUrl="sendReportApiUrl"
        :text="'Domande a cui hai risposto correttamente:'"
        :questions="correctlyAnsweredQuestions"
        :index="'test-' + index + '-1'"
      />
      <CollapsableQuestionList
        :sendReportApiUrl="sendReportApiUrl"
        :text="'Domande a cui hai risposto in maniera errata:'"
        :questions="incorrectlyAnsweredQuestions"
        :index="'test-' + index + '-2'"
      />
      <CollapsableQuestionList
        :sendReportApiUrl="sendReportApiUrl"
        :text="'Domande a cui non hai risposto:'"
        :questions="unansweredQuestions"
        :index="'test-' + index + '-3'"
      />
      <b-button
        @click="
          fullShown = !fullShown;
          $emit('expanded', index, fullShown);
        "
        v-b-toggle="'collapse-' + index"
        :variant="this.passing ? 'outline-success' : 'outline-danger'"
        >{{ buttonText }}
      </b-button>
    </div>
  </div>
</template>

<script>
import { library } from "@fortawesome/fontawesome-svg-core";
import { faCheck, faTimes } from "@fortawesome/free-solid-svg-icons";

library.add(faCheck);
library.add(faTimes);

import CollapsableQuestionList from "./CollapsableQuestionList.vue";
export default {
  components: { CollapsableQuestionList },
  name: "TakenTest",
  props: {
    sendReportApiUrl: String,
    index: Number,
    score: Number,
    timestamp: String,
    correctlyAnsweredQuestions: Array,
    incorrectlyAnsweredQuestions: Array,
    unansweredQuestions: Array,
    passing: Number,
    maxScore: Number,
  },
  data: () => {
    return {
      fullShown: false,
      monthNames: [
        "gennaio",
        "febbraio",
        "marzo",
        "aprile",
        "maggio",
        "giugno",
        "luglio",
        "agosto",
        "settembre",
        "ottobre",
        "novembre",
        "dicembre",
      ],
    };
  },
  computed: {
    outcome() {
      return this.passing ? "Superato" : "Non superato";
    },
    buttonText() {
      return this.fullShown ? "Nascondi dettagli" : "Mostra dettagli";
    },
    formattedTimestamp() {
      // spaces in the timestamp are being replaced with T's to maintain compatibility with iOS
      // https://www.elliotjreed.com/post/javascript/2019-03-20_Invalid_date_format_in_Javascript_on_iOS_devices
      let date = new Date(this.timestamp.replace(" ", "T"));
      return (
        (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) +
        "/" +
        (date.getMonth() + 1 < 10
          ? "0" + (date.getMonth() + 1)
          : date.getMonth() + 1) +
        "/" +
        date.getFullYear() +
        ", alle " +
        (date.getHours() < 10 ? "0" + date.getHours() : date.getHours()) +
        ":" +
        (date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes())
      );
    },
    formattedDate() {
      let date = new Date(this.timestamp.replace(" ", "T"));
      return (
        date.getDate() +
        //(date.getDate() < 10 ? "0" + date.getDate() : date.getDate() + 1) +
        " " +
        this.monthNames[date.getMonth()].toUpperCase() +
        // (date.getMonth() + 1 < 10
        //   ? "0" + (date.getMonth() + 1)
        //   : date.getMonth() + 1) +
        " " +
        date.getFullYear()
      );
    },
  },
  methods: {
    collapse() {
      this.fullShown = false;
    },
  },
};
</script>

<style scoped>
@import "../../../static/test-styles.css";
</style>
