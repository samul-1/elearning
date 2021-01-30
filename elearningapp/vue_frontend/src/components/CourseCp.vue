<template>
  <div>
    <h1 id="course_title">Pannello di controllo di {{ courseName }}</h1>
    <br />
    <div class="grid two-col-grid dashboard-grid">
      <div>
        <a :href="'/add_question/' + courseId"
          ><button class="btn btn-dark dashboard-btn">
            <font-awesome-icon class="mr-1" icon="plus-circle" />
            Aggiungi domande
          </button></a
        ><br />
        <a :href="'/edit_question/' + courseId"
          ><button
            style="margin-bottom: 0 !important"
            class="btn btn-dark dashboard-btn"
          >
            <font-awesome-icon class="mr-1" icon="list" />
            Visualizza / modifica domande
          </button></a
        ><br />
      </div>
      <div class="stats">
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
    </div>
  </div>
</template>

<script>
// Fontawesome
import { library } from "@fortawesome/fontawesome-svg-core";
import { faList, faPlusCircle } from "@fortawesome/free-solid-svg-icons";

library.add(faPlusCircle);
library.add(faList);

export default {
  name: "CourseCp",
  components: {},
  props: {
    courseName: String,
    courseId: Number,
    averageScore: Number,
    numberOfSubscribers: Number,
    numberOfTestsTaken: Number,
  },
  mounted() {},
  data: () => {
    return {};
  },
  methods: {},
};
</script>

<style scoped>
.stats {
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
}
</style>
