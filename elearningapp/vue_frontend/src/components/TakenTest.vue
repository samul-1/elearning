<template>
  <!-- :class="{ 'col-12': fullShown, 'col-3': !fullShown }" -->
  <div class="test-wrapper">
    <div
      class="preview"
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
    <div class="full taken-test" v-if="fullShown">
      <div class="row">
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
        :text="'Domande a cui hai risposto correttamente:'"
        :questions="correctlyAnsweredQuestions"
        :index="'test-' + index + '-1'"
      />
      <CollapsableQuestionList
        :text="'Domande a cui hai risposto in maniera errata:'"
        :questions="incorrectlyAnsweredQuestions"
        :index="'test-' + index + '-2'"
      />
      <CollapsableQuestionList
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
      let date = new Date(this.timestamp);
      return (
        (date.getDate() < 10 ? "0" + date.getDate() : date.getDate() + 1) +
        "/" +
        (date.getMonth() + 1 < 10
          ? "0" + (date.getMonth() + 1)
          : date.getMonth() + 1) +
        "/" +
        date.getFullYear() +
        ", alle " +
        (date.getHours() < 10 ? "0" + date.getHours() : date.getHours()) +
        ":" +
        (date.getMinutes() == 0 ? "0" + date.getMinutes() : date.getMinutes())
      );
    },
    formattedDate() {
      let date = new Date(this.timestamp);
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@600&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@800&display=swap");

* {
  font-family: "Source Sans Pro", sans-serif;
}
.taken-test {
  box-shadow: 0px 0px 3px 0px rgba(19, 19, 19, 0.8);
  border: 0px solid grey;
  border-radius: 0.8rem;
  overflow-x: auto;
  margin: 10px;
  padding: 15px;
  /* background-color: #f2f2f2; */
}

.mb-2px {
  margin-bottom: 2px;
}

.preview {
  display: grid;
  grid-template-rows: repeat(4, 1fr);
  align-items: center;
  justify-items: center;
  border: none;
  border-radius: 0.8rem;
  padding: 10px;
  box-shadow: 0px 0px 3px 0px rgba(19, 19, 19, 0.8);
  background: linear-gradient(to bottom, rgb(228, 228, 228) 21%, white 10%);
}

/* .preview-passed {
  background-color: rgba(55, 194, 0, 0.2);
}

.preview-failed {
  background-color: rgba(255, 0, 0, 0.2);
} */

.test-score-preview {
  font-size: 2rem;
  font-weight: thin;
}

.your-score-preview {
  font-weight: bold;
}

.test-date-preview {
  color: rgb(107, 107, 107);
  text-shadow: 0px 0px 1px rgb(94, 94, 94);
  align-self: flex-start;
}
</style>
