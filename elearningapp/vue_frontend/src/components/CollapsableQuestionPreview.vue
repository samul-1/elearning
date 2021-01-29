<template>
  <div>
    <div class="question-box" :class="{ 'preview-box': collapsed }">
      <!-- this shorter preview is shown when the question isn't expanded -->
      <div class="preview-text" :class="{ hidden: !collapsed }">
        <vue-mathjax :formula="text" :safe="false"></vue-mathjax>
        <p
          class="mt-3 answer-paragraph"
          v-for="(answer, index) in answers"
          :key="index"
        >
          <strong>{{ parseInt(index + 1) }}.</strong>&nbsp;
          <!--<span v-html="answer"></span>-->
          <vue-mathjax :formula="answer" :safe="false"></vue-mathjax>

          <span class="comment" v-if="index + 1 == correctAnswerIndex"
            ><em class="text-muted">(Risposta corretta)</em></span
          >
        </p>
        <div class="preview-text-fade"></div>
      </div>

      <!-- this standard preview is shown when the question is expanded -->
      <QuestionPreview
        :class="{ hidden: collapsed }"
        :text="text"
        :solution="solution"
        :answers="answers"
        :correctAnswerIndex="correctAnswerIndex"
        :questionId="questionId"
        :styled="false"
      >
      </QuestionPreview>

      <div style="z-index: 2" class="mt-4 pt-2">
        <b-button
          class="mr-2"
          variant="outline-primary"
          @click="collapsed = !collapsed"
        >
          <b-icon
            class="mb-1"
            :icon="collapsed ? 'file-plus' : 'file-minus'"
          ></b-icon>
          {{ collapsed ? "Mostra di più" : "Mostra di meno " }}
        </b-button>
        <b-button
          variant="outline-secondary"
          @click="$emit('editQuestion', questionId)"
        >
          <b-icon class="inline-icon" icon="pencil-square"></b-icon>Modifica
        </b-button>
      </div>
    </div>
  </div>
</template>

<script>
import QuestionPreview from "./QuestionPreview";
import { VueMathjax } from "vue-mathjax";

export default {
  name: "CollapsableQuestionPreview",
  components: {
    QuestionPreview,
    "vue-mathjax": VueMathjax,
  },
  props: {
    text: String,
    solution: String,
    answers: Array,
    correctAnswerIndex: Number,
    questionId: [String, Number],
  },
  mounted() {},
  data: () => {
    return {
      collapsed: true,
    };
  },
  methods: {},
  computed: {},
};
</script>

<style scoped>
.preview-box {
  height: 300px;
  background: linear-gradient(to top, rgb(228, 228, 228) 21%, white 10%);
}

/* {
  display: grid;
  grid-template-rows: repeat(4, 1fr);
  align-items: center;
  justify-items: center;
  border: none;
  border-radius: 0.8rem;
  padding: 10px;
  box-shadow: 0px 0px 3px 0px rgba(19, 19, 19, 0.8);
  background: linear-gradient(to bottom, rgb(228, 228, 228) 21%, white 10%);
}*/

.preview-text {
  height: 200px;
  word-break: break-all;
  overflow-y: hidden;
  position: relative;
}

.preview-text-fade {
  background-image: linear-gradient(to bottom, transparent, white);
  position: absolute;
  width: 100%;
  bottom: 0;
  margin: 0;
  padding: 30px 0;
}

.hidden {
  height: 0;
  opacity: 0;
  margin: 0;
  position: fixed;
  bottom: -1000px;
}

.comment {
  margin-left: 50px;
}

.answer-paragraph:first-of-type {
  padding-top: 1.2rem;
  position: relative;
}

.answer-paragraph:first-of-type:before {
  content: "";
  border-top: 1px solid rgb(211, 211, 211);
  box-shadow: 0 0 3px rgba(114, 114, 114, 0.2);
  position: absolute;
  top: 0;
  width: 100%;
}
</style>
