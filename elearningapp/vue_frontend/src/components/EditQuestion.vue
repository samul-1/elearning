<template>
  <div>
    <b-spinner
      style="position: fixed; top: 50%; left: 50%; color: black"
      v-if="loading"
      label="Loading..."
    ></b-spinner>
    <div class="grid question-filter-grid">
      <!-- // TODO implement question filtering  -->
      <span>Filtra per:</span>
      <span>Categoria</span>
      <span>Autore</span>
    </div>
    <div
      class="mt-4 grid edit-question-grid rem-1-gap"
      v-infinite-scroll="loadMoreQuestions"
    >
      <div
        v-for="question in questionsData"
        :key="question.questionId"
        :class="{
          'column-span-2': editingId == question.questionId,
          'successfully-edited': successfullyEditedId == question.questionId,
        }"
        :id="'q-' + question.questionId"
      >
        <!-- Display a collapsable preview for each question, and put a question editor near it
        which is rendered when the question is edited. The editor gets wired to the question via the props -->
        <QuestionEditor
          v-if="editingId == question.questionId"
          class="distinct p-5 mb-5 mt-5"
          :course-id="courseId"
          :questionText="question.text"
          :answers="question.answers"
          :correct-answer-index="question.correctAnswerIndex"
          :questionId="question.questionId"
          :categories="categories"
          :category="question.category"
          :solution="question.solution"
          :ref="'editor' + parseInt(question.questionId)"
          @save="saveQuestionToDatabase"
        ></QuestionEditor>
        <CollapsableQuestionPreview
          v-else
          :text="question.text"
          :answers="question.answers"
          :correct-answer-index="question.correctAnswerIndex"
          :questionId="question.questionId"
          :solution="question.solution"
          @editQuestion="editQuestion"
        ></CollapsableQuestionPreview>
      </div>
    </div>
  </div>
</template>

<script>
import CollapsableQuestionPreview from "./CollapsableQuestionPreview.vue";
import QuestionEditor from "./QuestionEditor.vue";

import axios from "axios";
import infiniteScroll from "vue-infinite-scroll";

export default {
  name: "EditQuestion",
  components: {
    CollapsableQuestionPreview,
    QuestionEditor,
  },
  directives: {
    infiniteScroll,
  },
  props: {
    questions: Array,
    userId: Number,
    courseId: Number,
    categories: {
      type: Array,
      default: () => [],
    },
    editQuestionApiUrl: String,
  },
  mounted() {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    // copy prop value to local data (questionsData can be updated by the infinite scroll)
    this.questionsData = this.questions;
  },
  data: () => {
    return {
      questionsData: [],
      loading: false,
      editingId: null,
      successfullyEditedId: null,
      scrollToConfig: {
        easing: "linear",
        cancelable: true,
        offset: -250,
      },
    };
  },
  methods: {
    editQuestion(id) {
      this.editingId = id;
      console.log(this.$refs);
    },
    // send server request to update question according to changes made by the user
    saveQuestionToDatabase(postData) {
      console.log(postData);
      this.loading = true;

      axios
        .put(
          // "http://127.0.0.1:8000/edit_question/" + this.courseId + "/",
          this.editQuestionApiUrl,
          postData
        )
        .then((response) => {
          console.log(response);
          // update QuestionPreview for updated question
          const updatedQuestion = response.data;
          if (response.status == 200) {
            this.questionsData[
              this.questionsData.findIndex(
                (q) => q.questionId === this.editingId
              )
            ] = updatedQuestion;
            this.showConfirmationAndCloseEditor();
          }
          this.loading = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    showConfirmationAndCloseEditor() {
      // call QuestionEditor method to reset the fields
      const editor = this.$refs["editor" + this.editingId][0];
      editor.cleanup();
      this.$scrollTo("#q-" + this.editingId, 0, this.scrollToConfig);
      this.successfullyEditedId = this.editingId;
      // show success message and hide it programmatically

      setTimeout(() => {
        this.successfullyEditedId = null;
      }, 3000);
      this.editingId = null;
    },

    // ask server for more questions (used for infinite scroll)
    loadMoreQuestions() {
      this.loading = true;
      axios
        .get(
          "http://127.0.0.1:8000/get_questions/" +
            this.courseId +
            "/5/" +
            this.maxQuestionId +
            "/"
        )
        // TODO pass this url as a prop
        .then((response) => {
          this.loading = false;
          console.log(response.data);
          this.questionsData.push(...response.data);
        })
        .catch((error) => {
          // alert(error);
          console.log(error);
        });
    },
  },
  computed: {
    // returns the highest question id present: used to poll the server for subsequent questions
    // (which are retrieved sorted by id)
    maxQuestionId() {
      return Math.max(...this.questionsData.map((q) => parseInt(q.questionId)));
    },
  },
};
</script>

<style>
.distinct {
  background-color: rgb(250, 250, 250) !important;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  border-radius: 0.8rem;
}
.successfully-edited:after {
  position: absolute;
  content: "Salvata!";
  bottom: 2%;
  right: 2%;
  color: green;
  font-weight: bold;
}

.successfully-edited {
  box-shadow: 0 0 10px green;
  border-radius: 0.8rem;
  position: relative;
}

.edit-question-grid div {
  transition: box-shadow 0.2s linear;
}
</style>
