<template>
  <div class="">
    <question-editor
      :course-id="courseId"
      :categories="categories"
      @save="saveQuestionToDatabase"
      ref="editor"
    ></question-editor>
    <transition name="overlay-text">
      <div class="overlay-card" v-if="success">
        <b-card bg-variant="light" text-variant="black">
          <b-card-text>
            <b-icon
              class="correct"
              icon="check"
              style="width: 80px; height: auto; margin-right: 1rem"
            ></b-icon>
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
  },
  mounted() {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  },
  data: () => {
    return {
      success: false,
    };
  },
  methods: {
    // TODO send info to server
    saveQuestionToDatabase(postData) {
      console.log(postData);
      axios
        .post(
          "http://127.0.0.1:8000/add_question/" + this.courseId + "/",
          postData
        )
        .then((response) => {
          console.log(response);
          if (response.status == 200) {
            this.showConfirmationAndCleanup();
          }
          // this.loading = false;
        })
        .catch((error) => {
          // alert(error);
          console.log(error);
        });
    },

    showConfirmationAndCleanup() {
      this.$refs.editor.cleanup();
      this.success = true;
      setTimeout(() => {
        this.success = false;
      }, 2000);
    },
  },
  computed: {},
};
</script>

<style>
.overlay-card {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;
  box-shadow: 0 0 15px gray;
  border: none !important;
  border-radius: 0.3rem !important;
}
</style>
