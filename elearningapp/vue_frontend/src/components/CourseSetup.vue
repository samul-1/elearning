<template>
  <div id="setup">
    <b-spinner
      style="position: fixed; top: 50%; left: 50%"
      v-if="loading"
      label="Loading..."
    ></b-spinner>
    <div>
      <transition name="slide-fade">
        <div id="step1" v-if="currstep == 1">
          <div class="setupfield">
            <label for="input-large">
              <h3>Nome del corso</h3>
            </label>
            <b-form-input
              autocomplete="off"
              id="input-large"
              size="lg"
              v-model="coursename"
              placeholder="Inserisci il nome del corso"
            ></b-form-input>
          </div>
          <div class="setupfield">
            <h3>Che modalità di domande vuoi usare nei test?</h3>
            <b-form-group>
              <div class="radio-option">
                <b-form-radio v-model="questionmode" name="a" value="A"
                  >Domande singole</b-form-radio
                >
                <span class="desc text-muted">
                  Ogni domanda sarà scorrelata dalle altre. Le domande verranno
                  scelte casualmente nelle simulazioni dei compiti.
                  <br /><em>Svantaggio:</em> non potrai inserire più domande
                  collegate tra di loro, poiché le domande vengono scelte
                  indipendentemente le une dalle altre nei test.
                </span>
              </div>
              <div class="radio-option">
                <b-form-radio v-model="questionmode" name="b" value="B"
                  >Domande raggruppate</b-form-radio
                >
                <span class="desc text-muted">
                  Ogni esercizio è composto da un testo introduttivo, anche
                  un'immagine eventualmente, e una serie di domande a risposta
                  multipla relative all'argomento principale. Nelle simulazioni
                  dei test, quando viene scelta la <em>macro-domanda</em>,
                  compaiono automaticamente tutte le domande a essa associata.
                </span>
              </div>
              <div class="radio-option">
                <b-form-radio v-model="questionmode" name="c" value="C"
                  >Piattaforma di valutazione esercizi JavaScript</b-form-radio
                >
                <span class="desc text-muted">
                  Gli esercizi sono problemi da risolvere implementando un
                  programma in JavaScript. Le correzioni sottomesse dagli utenti
                  sono corrette automaticamente dalla piattaforma.
                </span>
              </div>
            </b-form-group>
          </div>
        </div>
      </transition>
      <transition name="slide-fade">
        <div id="step2" v-if="currstep == 2">
          <div class="setupfield">
            <label for="input-large">
              <h3>Qual è il punteggio minimo per la sufficienza nei test?</h3>
            </label>
            <b-form-input
              autocomplete="off"
              :type="'number'"
              v-model="minpoints"
              id="input-large"
              size="lg"
              value="0"
            ></b-form-input>
          </div>
          <div class="setupfield">
            <h3>Quanti punti assegnare per:</h3>
            <div class="row">
              <div class="col-4">
                <label for="input-large">
                  <h5>Risposta corretta</h5>
                </label>
                <b-form-input
                  autocomplete="off"
                  :type="'number'"
                  v-model="corrpoints"
                  id="input-large"
                  size="lg"
                ></b-form-input>
              </div>
              <div class="col-4">
                <label for="input-large">
                  <h5>Risposta sbagliata</h5>
                </label>
                <b-form-input
                  autocomplete="off"
                  :type="'number'"
                  v-model="incorrpoints"
                  id="input-large"
                  size="lg"
                ></b-form-input>
              </div>
              <div class="col-4">
                <label for="input-large">
                  <h5>Risposta non data</h5>
                </label>
                <b-form-input
                  autocomplete="off"
                  :type="'number'"
                  v-model="unanspoints"
                  id="input-large"
                  size="lg"
                ></b-form-input>
              </div>
              <div class="col-12" style="margin-top: 1rem">
                <p v-if="questionmode == 'B'">
                  <strong>Nota bene:</strong> dato che hai selezionato la
                  modalità <em>Domande raggruppate</em>, questo parametro si
                  riferisce al numero di punti che ogni singola "micro-domanda"
                  vale. Questo significa che se, per esempio, crei una domanda
                  raggruppata che ne contiene 3 al suo interno, ciascuna delle 3
                  domande a essa associata avrà i valori specificati.
                </p>
              </div>
            </div>
          </div>
        </div>
      </transition>
      <transition name="slide-fade">
        <div id="step3" v-if="currstep == 3">
          <div class="setupfield">
            <h3>Vuoi che le domande vengano raggruppate per categoria?</h3>
            <b-form-group>
              <div class="radio-option">
                <b-form-radio v-model="categorymode" name="a" value="A"
                  >Sì</b-form-radio
                >
                <span class="desc text-muted">
                  Potrai creare una lista di argomenti trattati nel corso, e
                  ogni domanda verrà inserita in una categoria. Dopodiché,
                  potrai specificare una distribuzione di domande per categoria,
                  ovvero impostare per ogni categoria quante domande di quella
                  categoria dovranno comparire nei test.
                </span>
              </div>
              <div class="radio-option">
                <b-form-radio v-model="categorymode" name="b" value="B"
                  >No</b-form-radio
                >
                <span class="desc text-muted">
                  Le domande non verranno associate a una categoria e avranno
                  tutte la stessa probabilità di comparire nei test.
                </span>
              </div>
            </b-form-group>
            <div v-if="categorymode == 'A'" class="setupfield">
              <h3>Crea categorie</h3>
              <div
                v-for="(category, index) in categories"
                :key="index"
                class="row"
              >
                <div class="col-8">
                  <b-form-input
                    autocomplete="off"
                    class="category-input"
                    v-model="categories[index]"
                    size="lg"
                    placeholder="Categoria"
                  ></b-form-input>
                </div>
                <div class="col-4">
                  <b-button
                    :disabled="categories.length <= 1"
                    variant="danger"
                    @click="categories.splice(index, 1)"
                    >Rimuovi</b-button
                  >
                </div>
              </div>
              <b-button variant="outline-primary" @click="categories.push('')"
                >Aggiungi</b-button
              >
            </div>
          </div>
        </div>
      </transition>
      <transition name="slide-fade">
        <div id="step4" v-if="currstep == 4">
          <div class="setupfield">
            <div v-if="categorymode == 'A'">
              <h3>
                Vuoi che le domande compaiano nei test con una particolare
                distribuzione in base alle categorie?
              </h3>
              <div class="radio-option">
                <b-form-radio v-model="distributionmode" name="a" value="A"
                  >Sì</b-form-radio
                >
              </div>
              <div class="radio-option">
                <b-form-radio v-model="distributionmode" name="b" value="B"
                  >No</b-form-radio
                >
                <span class="desc text-muted">
                  Le domande verranno sempre scelte in maniera casuale
                  indipendentemente dalla loro categoria. Selezionando questa
                  opzione, si rischia che in alcuni test compaiano tutte domande
                  sullo stesso argomento.
                </span>
              </div>
            </div>
            <div v-if="distributionmode == 'A'" class="setupfield">
              <h3>Crea distribuzione</h3>
              <div
                v-for="(category, index) in categories"
                :key="index"
                class="row"
              >
                <div class="col-6">
                  <span class="categoryName h5">{{ category }}</span>
                  <b-form-input
                    autocomplete="off"
                    class="category-input form-control-inline"
                    v-model="distributionvalues[index]"
                    :class="{ 'form-error': distributionvalues[index] < 0 }"
                    size="md"
                    type="number"
                    placeholder="0"
                  ></b-form-input>
                </div>
                <div class="col-2"></div>
              </div>
              <p v-if="questionmode == 'B'">
                <strong>Nota bene:</strong> dato che hai selezionato la modalità
                <em>Domande raggruppate</em>, questi parametri si riferiscono al
                numero di "macro-domande" che compariranno nei test. Per
                ciascuna "macro-domanda", potrai comunque selezionare un numero
                arbitrario di "mini-domande" da associarvi.
              </p>
              <p>Numero di domande per test: {{ questionsPerTest }}</p>
            </div>
            <div v-else class="setupfield">
              <h3>
                Scegli il numero di domande che vuoi che compaiano in ogni test
              </h3>
              <span>Numero di domande per test</span>
              <b-form-input
                autocomplete="off"
                class="category-input form-control-inline"
                v-model="questionspertestValue"
                :class="{ 'form-error': questionspertestValue < 1 }"
                size="md"
                type="number"
                placeholder="1"
              ></b-form-input>
              <p v-if="questionmode == 'B'">
                <strong>Nota bene:</strong> dato che hai selezionato la modalità
                <em>Domande raggruppate</em>, questo parametro si riferisce al
                numero di "macro-domande" che compariranno nei test. Per
                ciascuna "macro-domanda", potrai comunque selezionare un numero
                arbitrario di "mini-domande" da associarvi.
              </p>
            </div>
          </div>
        </div>
      </transition>
      <transition name="slide-fade">
        <div id="step1" v-if="currstep == 5">
          <div class="setupfield">
            <h3>Ci siamo quasi!</h3>
            <p>
              Controlla che le impostazioni riportate qui sotto siano corrette.
              Se hai commesso un errore, puoi tornare indietro per correggerlo.
            </p>
            <div class="summary">
              <div>
                <p><strong>Nome del corso:</strong> {{ coursename }}</p>
                <p>
                  <strong>Tipologia esercizi:</strong>
                  {{ questionmodeAsString }}
                </p>
                <p v-if="categorymode == 'A'">
                  <strong>Categorie:</strong>
                  <span v-if="categorymode == 'B'"><em>nessuna</em></span>
                </p>
                <ul v-if="categorymode == 'A'">
                  <li v-for="category in categories" v-bind:key="category">
                    {{ category }}
                  </li>
                </ul>
                <p v-if="distributionmode == 'A'">
                  <strong>Ogni test conterrà:</strong>
                </p>
                <ul v-if="distributionmode == 'A'">
                  <li
                    v-for="(category, index) in categories"
                    v-bind:key="'distribution_summary_' + index"
                  >
                    <strong>{{ distributionvalues[index] }}</strong>
                    {{
                      parseInt(distributionvalues[index]) == 1
                        ? "domanda"
                        : "domande"
                    }}
                    {{
                      parseInt(distributionvalues[index]) == 1
                        ? "appartenente"
                        : "appartenenti"
                    }}
                    alla categoria <strong>{{ category }}</strong>
                  </li>
                </ul>
              </div>
              <div v-if="questionmode != 'C'">
                <p>
                  Ogni test sarà composto da
                  <strong
                    >{{ questionsPerTest }}
                    {{ questionsPerTest == 1 ? "domanda" : "domande" }}</strong
                  >
                </p>
                <p>
                  Punteggio minimo per la sufficienza:
                  <strong>{{ minpoints }}</strong>
                  {{ parseInt(minpoints) == 1 ? "punto" : "punti" }}
                </p>
                <p>
                  Punteggio per risposte corrette:
                  <strong>{{ corrpoints }}</strong>
                  {{ Math.abs(parseInt(corrpoints)) == 1 ? "punto" : "punti" }}
                </p>
                <p>
                  Punteggio per risposte errate:
                  <strong>{{ incorrpoints }}</strong>
                  {{
                    Math.abs(parseInt(incorrpoints)) == 1 ? "punto" : "punti"
                  }}
                </p>
                <p>
                  Punteggio per domande senza risposta:
                  <strong>{{ unanspoints }}</strong>
                  {{ Math.abs(parseInt(unanspoints)) == 1 ? "punto" : "punti" }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <div class="buttons-grid">
        <b-button
          @click="questionmode == 'C' ? (currstep = 1) : currstep--"
          :disabled="currstep == 1"
          id="goback-button"
          variant="outline-primary"
          style="margin-bottom: 10px"
        >
          Step precedente
        </b-button>
        <b-button
          @click="
            currstep == 5
              ? sendCourseData()
              : questionmode == 'C'
              ? (currstep = 5)
              : currstep++
          "
          id="next-button"
          :disabled="invalidData"
          variant="outline-primary"
          style="margin-bottom: 10px"
          >{{ currstep != 5 ? "Prossimo step" : "Concludi" }}</b-button
        >
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "App",
  components: {},
  props: {
    questions: Array,
  },
  data: () => {
    return {
      currstep: 1,
      loading: false,
      questionmode: null,
      minpoints: 0,
      corrpoints: 1,
      incorrpoints: -1,
      unanspoints: 0,
      coursename: null,
      categorymode: null,
      distributionmode: "B",
      categories: [""],
      distributionvalues: [],
      questionspertestValue: 1,
      // currstep: 5,
      // loading: false,
      // questionmode: "B",
      // minpoints: 5,
      // corrpoints: 1,
      // incorrpoints: -1,
      // unanspoints: 0,
      // coursename: "Ricerca Operativa",
      // categorymode: "A",
      // distributionmode: "A",
      // categories: ["Grafi", "Modelli", "PL"],
      // distributionvalues: [2, 1, 4],
      // questionspertestValue: 1,
    };
  },
  mounted() {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  },
  computed: {
    questionsPerTest() {
      if (this.categorymode == "B" || this.distributionmode == "B") {
        return this.questionspertestValue;
      }
      let count = 0;
      if (!this.distributionvalues.length) {
        return count;
      }
      for (const category of this.distributionvalues) {
        const val = Number.isNaN(parseInt(category)) ? 0 : parseInt(category);
        count += val;
      }
      return count;
    },
    questionmodeAsString() {
      return this.questionmode == "A"
        ? "Domande singole"
        : this.questionmode == "B"
        ? "Domande raggruppate"
        : "Piattaforma esercizi JavaScript";
    },
    invalidData() {
      if (this.currstep == 1) {
        return (
          this.questionmode == null ||
          this.coursename == null ||
          !this.coursename.length
        );
      }
      if (this.currstep == 3) {
        return (
          this.categorymode == null ||
          (this.categorymode == "A" && this.categories.some((c) => !c.length))
        );
      }
      if (this.currstep == 4) {
        return (
          this.distributionmode == "A" &&
          (this.distributionvalues.some((d) => parseInt(d) < 0 || d == "") ||
            this.distributionvalues.length != this.categories.length)
        );
      }
      return false;
    },
  },
  methods: {
    constructDataObject() {
      let data = {
        course_name: this.coursename,
        question_mode: this.questionmode,
      };
      if (this.questionmode != "C") {
        data["min_points"] = this.minpoints;
        data["corr_points"] = this.corrpoints;
        data["incorr_points"] = this.incorrpoints;
        data["unans_points"] = this.unanspoints;
        data["category_mode"] = this.categorymode;
      }
      if (this.categorymode == "A") {
        data["categories"] = this.categories;
        data["distribution_mode"] = this.distributionmode;
      }
      if (this.distributionmode == "A") {
        data["distribution_values"] = this.distributionvalues;
      } else if (this.questionmode != "C") {
        data["questions_per_test"] = this.questionspertestValue;
      }
      return data;
    },
    sendCourseData() {
      const postData = JSON.stringify(this.constructDataObject());
      console.log(postData);
      // this.loading = true;
      axios
        .post("http://127.0.0.1:8000/createcourse", postData)
        .then((response) => {
          // this.$root.$emit("bv::show::modal", "outcome-modal", "#sendAnswers");
          console.log(response);
          // this.loading = false;
        })
        .catch((error) => {
          // alert(error);
          console.log(error);
        });
    },
  },
};
</script>
<style>
@import "../../../static/dashboard-styles.css";

/* .setupfield {
  margin-top: 10px;
  margin-bottom: 30px;
}
.desc {
  margin-left: 20px;
  font-size: 0.9em;
}
.radio-option {
  margin-bottom: 20px;
}
.category-input {
  margin-bottom: 10px;
}
.form-control-inline {
  display: inline-block;
  width: min-content;
  margin-left: 2rem;
}
.buttons-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  margin-top: 0.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgb(129, 129, 129);
}
#goback-button {
  justify-self: flex-start;
}
#next-button {
  justify-self: flex-end;
}
.summary {
  display: grid;
  grid-template-columns: 2fr 1fr;
  margin-top: 1.5rem;
  padding: 0 2rem;
  padding-top: 2.5rem;
  border-top: 1px solid rgb(129, 129, 129);
}

.summary div:nth-of-type(2) {
  justify-self: end;
}

.summary strong {
  font-size: 1.1rem;
}

.summary strong:nth-child(2) {
  padding: 0rem 0.5rem;
  background-color: rgb(80, 80, 80);
  color: white;
  border-radius: 0.2rem;
  font-weight: 400;
  font-size: 1rem;
}
ul {
  padding: 0;
  margin-left: 1rem;
  margin-top: -0.5rem;
} */
</style>