<template>
  <div class="col-12 col-md-10 question-wrapper">
    <p class="question-text">
      <strong class="question-label"
        >Domanda{{
          questionIndex != -1 ? " " + (questionIndex + 1) : ""
        }}.</strong
      >

      <!-- <vue-mathjax
        :formula="text"
        :safe="false"
        :options="mathjaxOptions"
      ></vue-mathjax> -->
      <span v-html="text"></span>
    </p>
    <ol class="answer-list">
      <li v-for="(answer, index) in answers" :key="index">
        <input
          type="radio"
          :value="index"
          :id="index + '_' + questionIndex"
          v-model="chosenAnswer"
          @change="$emit('answer', chosenAnswer + 1)"
        />
        &nbsp;<label class="answer" :for="index + '_' + questionIndex">
          <!-- <vue-mathjax
            :formula="answer"
            :safe="false"
            :options="mathjaxOptions"
          ></vue-mathjax> -->
          <span v-html="answer"></span>
        </label>
      </li>
    </ol>
  </div>
</template>

<script>
// import { VueMathjax } from "vue-mathjax";

export default {
  name: "Question",
  props: {
    text: String,
    answers: Array,
    givenAnswer: Number,
    questionIndex: Number,
  },
  components: {
    //"vue-mathjax": VueMathjax
  },
  data: () => {
    return {
      chosenAnswer: -1,
      mathjaxOptions: {
        tex2jax: {
          inlineMath: [
            ["$", "$"],
            ["\\(", "\\)"],
          ],
          displayMath: [
            ["$$", "$$"],
            ["[", "]"],
          ],
          processEscapes: true,
          processEnvironments: true,
        },
      },
    };
  },
};
</script>

<style scoped>
/* ul {
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
} */
</style>
