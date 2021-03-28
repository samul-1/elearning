<template>
  <div>
    <b-spinner
      style="position: fixed; top: 50%; left: 50%; color: black"
      v-if="loading"
      label="Loading..."
    ></b-spinner>
    <div style="margin-top: 3rem" v-if="!tests.length">
      <b-card bg-variant="light" text-variant="black">
        <b-card-text class="grid-card">
          <font-awesome-icon
            class="mr-1"
            icon="exclamation-circle"
            style="width: 80px; height: 80px"
          />

          <span>Non hai ancora effettuato alcun test.</span>
        </b-card-text>
      </b-card>
    </div>

    <div class="grid-test-history" v-infinite-scroll="loadMoreTests">
      <TakenTest
        v-for="(item, index) in tests"
        :key="index"
        :correctlyAnsweredQuestions="item.correctlyAnsweredQuestions"
        :incorrectlyAnsweredQuestions="item.incorrectlyAnsweredQuestions"
        :unansweredQuestions="item.unansweredQuestions"
        :score="item.score"
        :passing="item.passing"
        :timestamp="item.timestamp"
        :index="index"
        :ref="index"
        :maxScore="maxScore"
        @expanded="previewExpanded"
        :class="{ 'expanded-grid-column': index == expanded }"
        :sendReportApiUrl="sendReportApiUrl"
      />

    </div>
    <p class="text-center mt-4 link" @click="loadMoreTests()">Carica più compiti</p>
  </div>
</template>

<script>
import TakenTest from "./TakenTest.vue";
import axios from "axios";
import infiniteScroll from "vue-infinite-scroll";

// Fontawesome
import { library } from "@fortawesome/fontawesome-svg-core";
import { faExclamationCircle } from "@fortawesome/free-solid-svg-icons";

library.add(faExclamationCircle);

export default {
  name: "TestHistory",
  components: {
    TakenTest,
  },
  directives: {
    infiniteScroll,
  },
  props: {
    tests: Array,
    maxScore: Number,
    sendReportApiUrl: String,
    getTakenTestsApiUrl: String,
  },
  mounted() {
    this.testsData = this.tests;
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  },
  data: () => {
    return {
      expanded: -1,
      testsData: [],
      loading: false,
    };
  },
  methods: {
    previewExpanded(index, value) {
      console.log(index + " " + value);
      // collapse all the other expanded previews when one is expanded
      this.expanded = value ? index : null;
      for (const [i] of this.tests.entries()) {
        if (i != index) {
          this.$refs[i][0].collapse();
        }
      }
    },
    loadMoreTests() {
      this.loading = true;
      axios
        .get(this.getTakenTestsApiUrl + this.minTestId)
        .then((response) => {
          this.loading = false;
          console.log(response.data);
          this.testsData.push(...response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  computed: {
    // returns the lowest test id present: used to poll the server for subsequent tests
    minTestId() {
      if (!this.testsData.length) {
        return 0;
      }
      return Math.min(...this.testsData.map((t) => parseInt(t.id)));
    },
  },
};
</script>

<style scoped>
@import "../../../static/test-styles.css";
</style>
