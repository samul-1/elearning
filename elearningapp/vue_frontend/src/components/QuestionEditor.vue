<template>
  <div
    class="grid question-editor-grid one-col-mobile one-col-tablet"
  >
    <div class="grid-col">
      <div>
        <h3>Testo della domanda</h3>
        <vue-editor
          :id="'questionText'"
          :editorToolbar="customToolbar"
          class="big-editor"
          v-model="questionTextData"
        ></vue-editor>
      </div>
      <div v-if="categories.length > 0">
        <h3>Categoria</h3>
        <select v-model="categoryData">
          <option disabled value="">Scegli la categoria</option>

          <option
            v-for="(category, index) in categories"
            :key="index"
            :value="Object.keys(category)[0]"
          >
            {{ category[Object.keys(category)[0]] }}
          </option>
        </select>
      </div>
      <div>
        <h3>Risposte</h3>
        <div
          style="margin-bottom: 0.5rem"
          class="grid two-to-one-col-fr rem-1-gap"
          v-for="(answer, index) in answersData"
          :key="index"
        >
          <div>
            <vue-editor
              :id="'answer_' + index"
              :editorToolbar="customToolbar"
              class="answer-editor"
              v-model="answersData[index]"
            ></vue-editor>
          </div>
          <div style="align-self: center">
            <b-button
              style="align-self: center"
              :disabled="answersData.length <= 2"
              variant="danger"
              @click="
                if (correctAnswerIndexData + 1 == index)
                  correctAnswerIndexData = 0;
                answersData.splice(index, 1);
              "
              >Rimuovi</b-button
            >
            <div class="radio-option">
              <b-form-radio
                v-model="correctAnswerIndexData"
                :name="String(index + 1)"
                :value="index + 1"
                >Risposta corretta</b-form-radio
              >
            </div>
          </div>
        </div>

        <b-button
          class="w-100"
          variant="outline-primary"
          @click="answersData.push('')"
        >
          <b-icon
            icon="plus-circle"
            class="inline-icon"
            style="margin-bottom: 2px"
          ></b-icon>
          Aggiungi risposta</b-button
        >
      </div>
      <div>
        <h3>Soluzione</h3>
        <vue-editor
          class="big-editor"
          :id="'solutionText'"
          :editorToolbar="customToolbar"
          v-model="solutionData"
        ></vue-editor>
      </div>
    </div>

    <!-- real-time question preview -->
    <div class="grid-col preview-col">
      <div class="preview">
        <h3>Anteprima</h3>
        <QuestionPreview
          :text="questionTextWithoutParagraphTag"
          :answers="answerTextsWithoutParagraphTag"
          :correctAnswerIndex="correctAnswerIndexData"
          :solution="solutionData"
        ></QuestionPreview>
        <b-button
          class="w-100 mt-4"
          variant="outline-success"
          @click="$emit('save', serializedQuestionData)"
          :disabled="invalidForm || disableSave"
        >
          <font-awesome-icon class="mr-1" icon="check-circle" />

          Salva domanda</b-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import { VueEditor } from "vue2-editor";
import QuestionPreview from "./QuestionPreview.vue";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faCheckCircle } from "@fortawesome/free-solid-svg-icons";

library.add(faCheckCircle);

export default {
  name: "QuestionEditor",
  components: {
    VueEditor,
    QuestionPreview,
  },
  props: {
    courseId: Number,
    disableSave: {
      type: Boolean,
      default: false,
    },
    questionId: {
      type: Number,
      default: -1,
    },
    questionText: {
      type: String,
      default: "",
    },
    answers: {
      type: Array,
      default: () => ["", ""],
    },
    correctAnswerIndex: {
      type: Number,
      default: 0,
    },
    solution: {
      type: String,
      default: "",
    },
    categories: {
      type: [Array, Number],
      default: () => [],
    },
    category: {
      type: [String, Number],
      default: "",
    },
  },
  mounted() {
    // set data values to match props (can't modify props directly)
    this.questionTextData = this.questionText;
    this.answersData = this.answers;
    this.correctAnswerIndexData = this.correctAnswerIndex;
    this.solutionData = this.solution;
    this.categoryData = String(this.category);
  },
  watch: {},
  data: () => {
    return {
      questionTextData: "",
      solutionData: "",
      answersData: [],
      previewElements: [],
      categoryData: "",
      correctAnswerIndexData: -1,
      customToolbar: [
        ["bold", "italic", "underline"],
        [{ list: "ordered" }, { list: "bullet" }],
        ["image"],
      ],
    };
  },
  methods: {
    // resets the editor to initial state
    cleanup() {
      this.questionTextData = this.solutionData = this.categoryData =
        "";
      this.answersData = ["", ""];
      this.correctAnswerIndexData = 0;
    },
  },
  computed: {
    // remove the automatically-generated (by vue-editor) <p> tags from the fields
    questionTextWithoutParagraphTag() {
      return this.questionTextData.replaceAll(/<[/]?p>/gi, "");
    },
    answerTextsWithoutParagraphTag() {
      return this.answersData.map((a) =>
        a.replaceAll(/<[/]?p>/gi, "")
      );
    },
    solutionTextWithoutParagraphTag() {
      return this.solutionData.replaceAll(/<[/]?p>/gi, "");
    },
    // returns an object containing the question data for the parent to consume
    serializedQuestionData() {
      const obj = {
        text: this.questionTextWithoutParagraphTag,
        solution_text: this.solutionTextWithoutParagraphTag.length
          ? this.solutionData
          : "(soluzione non ancora inserita)", // TODO handle this on serverside
        category: this.categoryData,
        answers: this.answerTextsWithoutParagraphTag,
        correct_answer_index: this.correctAnswerIndexData,
        course: this.courseId,
      };
      if (this.questionId != -1) {
        obj.questionId = this.questionId;
      }
      return obj;
    },
    // used to disable the save button when invalid information is supplied
    invalidForm() {
      return (
        !this.questionTextData.length || // question is empty
        this.correctAnswerIndexData == 0 || // no correct answer is selected
        this.answersData.some((a) => !a.length) || // there are empty answers
        (this.categories.length && !this.categoryData.length) // course has categories and no category is selected
      );
    },
  },
};
</script>

<style scoped>
@import "../../../static/editor-styles.css";
</style>
