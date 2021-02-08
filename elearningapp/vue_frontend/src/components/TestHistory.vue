<template>
  <div>
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

    <div class="grid-test-history">
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
  </div>
</template>

<script>
import TakenTest from "./TakenTest.vue";

// Fontawesome
import { library } from "@fortawesome/fontawesome-svg-core";
import { faExclamationCircle } from "@fortawesome/free-solid-svg-icons";

library.add(faExclamationCircle);

export default {
  name: "TestHistory",
  components: {
    TakenTest,
  },
  props: {
    tests: Array,
    maxScore: Number,
    sendReportApiUrl: String,
  },
  mounted() {},
  data: () => {
    return {
      expanded: -1,
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
  },
};
</script>

<style scoped>
@import "../../../static/test-styles.css";
</style>
