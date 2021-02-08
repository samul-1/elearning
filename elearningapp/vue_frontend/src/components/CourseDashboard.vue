<template>
  <div>
    <h1 class="mb-5" id="course_title">{{ courseName }}</h1>

    <div class="grid two-col-grid dashboard-grid">
      <div style="margin-top: 0rem">
        <a :href="'/test/' + courseId"
          ><button class="btn btn-dark dashboard-btn">
            <font-awesome-icon class="mr-1" icon="stream" />
            Inizia un test
          </button></a
        ><br />
        <a :href="'/question_history/' + courseId"
          ><button class="btn btn-dark dashboard-btn">
            <font-awesome-icon class="mr-1" icon="bookmark" />
            Lista domande già viste
          </button></a
        ><br />
        <a :href="'/test_history/' + courseId"
          ><button class="btn btn-dark dashboard-btn">
            <font-awesome-icon class="mr-1" icon="history" />
            Cronologia test
          </button></a
        >
      </div>
      <div class="user-stats">
        <span class="h5">I tuoi ultimi punteggi</span>
        <span class="text-muted" style="margin-left: 0.5rem">
          Media: {{ userAverageScore }}</span
        >
        <TrendChart
          :datasets="[
            {
              data: lastScores,
              smooth: true,
              fill: true,
              showPoints: true,
            },
          ]"
          :grid="{
            verticalLines: false,
            horizontalLines: false,
          }"
          :labels="{
            // count unique values
            yLabels: parseInt(new Set(lastScores).size), //lastScores.length,
            yLabelsTextFormatter: (val) => Math.round(val),
          }"
          :interactive="false"
          :padding="'25 0 8 0'"
        >
        </TrendChart>
        <svg
          width="0"
          height="0"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id="gradient" x1="1" x2="1" y1="0" y2="1">
              <stop offset="0%" stop-color="rgba(97,218,251, 0.4)"></stop>
              <stop offset="100%" stop-color="rgba(97,218,251, 0.2)"></stop>
            </linearGradient>
          </defs>
        </svg>
      </div>
    </div>
  </div>
</template>

<script>
// Fontawesome
import { library } from "@fortawesome/fontawesome-svg-core";
import { faStream } from "@fortawesome/free-solid-svg-icons";
import { faHistory } from "@fortawesome/free-solid-svg-icons";
import { faBookmark } from "@fortawesome/free-solid-svg-icons";

library.add(faStream);
library.add(faHistory);
library.add(faBookmark);

export default {
  name: "CourseDashboard",
  components: {},
  props: {
    courseName: String,
    courseId: Number,
    userAverageScore: Number,
    userLastScore: Number,
    userId: Number,
    lastScores: Array,
  },
  mounted() {},
  data: () => {
    return {};
  },
  methods: {},
};
</script>

<style>
@import "../../../static/dashboard-styles.css";
</style>
