<template>
  <div>
    <h1 id="course_title">{{ courseName }}</h1>
    <!--<h1>Benvenuto, {{ global_user_data.name }}</h1>-->
    <br />
    <!-- <div class="row">
        <div class="col-md-3 col-12">
            <a href="/test/{{ courseId }}"><button class="btn btn-dark">Simula un test</button></a><br />
            <a href="/question_history/{{ userId }}/{{ courseId }}"><button class="btn btn-dark">Lista domande già
                viste</button></a><br />
            <a href="/test_history/{{ userId }}/{{ courseId }}"><button class="btn btn-dark">Cronologia test</button></a>
        </div>
        <div class="col-md-5 col-1"></div>
        <div class="col-md-3 col-10 stats">
            <h3>Le mie statistiche</h3>
            <p><strong>Media punteggi:</strong> {{ course_specific_user_data.average_score }}</p>
            <p><strong>Ultimo punteggio:</strong> {{ course_specific_user_data.last_score }}</p>
        </div>
    </div> -->

    <div class="grid two-col-grid dashboard-grid">
      <div style="margin-top: 0rem">
        <a :href="'/test/' + courseId"
          ><button class="btn btn-dark dashboard-btn">
            <b-icon icon="list-ol" class="inline-icon dashboard-icon"></b-icon>
            Simula un test
          </button></a
        ><br />
        <a :href="'/question_history/' + userId + '/' + courseId"
          ><button class="btn btn-dark dashboard-btn">
            <b-icon
              icon="bookmark-check"
              class="inline-icon dashboard-icon"
            ></b-icon>
            Lista domande già viste
          </button></a
        ><br />
        <a :href="'/test_history/' + userId + '/' + courseId"
          ><button class="btn btn-dark dashboard-btn">
            <b-icon icon="bookmark" class="inline-icon dashboard-icon"></b-icon>
            Cronologia test
          </button></a
        >
      </div>
      <div class="stats">
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
            yLabels: 10,
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
.y-labels {
  font-size: 0.65rem;
}
.stroke {
  stroke: #61dafb;
}
.fill {
  fill: url(#gradient);
}
.stats {
  border: 1px solid #dbdbdb;
  border-radius: 0.8rem;
  padding: 1rem;
  text-align: center;
}
.point {
  fill: #61dafb;
  stroke: #61dafb;
}
</style>
