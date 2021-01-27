<template>
  <div class="col-10 question-wrapper">
    <p class="question-text">
      <strong
        >Domanda{{
          questionIndex != -1 ? " " + (questionIndex + 1) : ""
        }}.</strong
      >
      <!--{{ text }}-->
      <!--<span v-html="text"></span>-->
      <vue-mathjax :formula="text" :safe="false"></vue-mathjax>
    </p>
    <ol class="answer-list">
      <li v-for="(answer, index) in answers" :key="index">
        <input
          type="radio"
          :value="index"
          :id="index + questionIndex"
          v-model="chosenAnswer"
          @change="$emit('answer', chosenAnswer)"
        />
        &nbsp;<label class="answer" :for="index + questionIndex">
          <!--{{answer}}-->
          <!--<span v-html="answer"></span>-->
          <vue-mathjax :formula="answer" :safe="false"></vue-mathjax>
        </label>
      </li>
    </ol>
  </div>
</template>

<script>
import { VueMathjax } from "vue-mathjax";

export default {
  name: "Question",
  props: {
    text: String,
    answers: Object,
    givenAnswer: Number,
    questionIndex: Number,
  },
  components: { "vue-mathjax": VueMathjax },
  data: () => {
    return {
      chosenAnswer: -1,
    };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}

a {
  color: #42b983;
}

.question-wrapper {
  padding: 2rem 0;
}

.question-box {
  border: 1px solid grey;
  border-radius: 3px;
  width: fit-content;
  padding: 15px;
  overflow-x: auto;
}

.answer:hover {
  cursor: pointer;
  background-color: rgba(194, 194, 194, 0.2);
  border-radius: 5px;
  transition: 0.1s ease;
}

.answer {
  width: 90%;
  transition: 0.1s ease;
}

.answer-list {
  padding: 0.5rem 1rem;
}

.answer-list li {
  padding: 0.2rem 0;
}
</style>
