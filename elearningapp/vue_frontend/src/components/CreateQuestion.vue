<template>
  <div class="">
    <b-spinner
      style="position: fixed; top: 50%; left: 50%; color: black"
      v-if="loading"
      label="Loading..."
    ></b-spinner>
    <question-editor
      :course-id="courseId"
      :categories="categories"
      @save="saveQuestionToDatabase"
      ref="editor"
    ></question-editor>
    <transition name="overlay-text">
      <div class="overlay-card" v-if="success">
        <b-card bg-variant="light" text-variant="black">
          <b-card-text class="grid-card">
            <font-awesome-icon
              class="correct"
              icon="check-circle"
              style="width: 80px; height: 80px"
            />
            Domanda salvata con successo
          </b-card-text>
        </b-card>
      </div>
    </transition>
  </div>
</template>

<script>
import QuestionEditor from "./QuestionEditor.vue";
import axios from "axios";

export default {
  name: "CreateQuestion",
  components: {
    QuestionEditor,
  },
  props: {
    courseId: Number,
    categories: Array,
    apiUrl: String,
  },
  mounted() {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  },
  data: () => {
    return {
      success: false,
      loading: false,
    };
  },
  methods: {
    // send the server a request to create a new question
    saveQuestionToDatabase(postData) {
      console.log(postData);
      this.loading = true;
      axios
        .post(
          // "http://127.0.0.1:8000/add_question/" + this.courseId + "/",
          this.apiUrl,
          postData
        )
        .then((response) => {
          console.log(response);
          if (response.status == 200) {
            this.showConfirmationAndCleanup();
          }
          this.loading = false;
        })
        .catch((error) => {
          // alert(error);
          console.log(error);
        });
    },

    showConfirmationAndCleanup() {
      // call QuestionEditor method to reset the fields
      this.$refs.editor.cleanup();

      // show success message and hide it programmatically
      this.success = true;
      setTimeout(() => {
        this.success = false;
      }, 2000);
    },
  },
  computed: {},
};
</script>

<style scoped>
@import "../../../static/editor-styles.css";

/* .grid-card {
  display: grid;
  grid-template-columns: 110px auto;
  align-items: center;
} */
</style>