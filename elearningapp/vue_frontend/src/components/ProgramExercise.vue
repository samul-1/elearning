<template>
    <div class="row">
        <div class="col-8">
            <b-spinner
                style="position:fixed; top:50%; left:50%; color: white;"
                v-if="loading"
                label="Loading..."
            ></b-spinner>
            <h2>Esercizio</h2>
            <p>{{ text }}</p>
            <prism-editor 
                class="my-editor h-350" 
                v-model="userProgram" 
                :highlight="highlighter"
                line-numbers
            >
            </prism-editor>
            <br />
            <b-button
                id="submit"
                @click="submit()"
                :disabled="userProgram.length == 0"
                variant="outline-primary"
                style="margin-bottom: 10px"
                >Invia</b-button
            >
        </div>
        <div class="col-4">
            <h4>Test case</h4>
            <p class="text-muted">Il programma potrebbe venire testato anche con altri input non presenti in questa lista.</p>
            <ul class="testcase-list">
                <li
                    class="test-case"
                    v-for="(testCase, index) in publicTestCases"
                    :key="index"
                >
                    <strong>Input</strong>
                    <pre>{{ testCase.input.replace('=', '\n') }}</pre>
                    <strong>Output</strong>
                    <pre>{{ testCase.output }}</pre>
                </li>
            </ul>
        </div>

        <b-modal size="xl" id="outcome-modal">
                <template #modal-header="{  }">
                    <h1>Risultati</h1>
                </template>
                <template #default="{  }">
                    <div class="container">
                        <div class="row">
                            <div class="col-10">
                                <p>
                                    <strong>Test case superati:</strong>&nbsp;
                                    <span class="score"
                                        >{{ outcomeObj.positiveCases }}</span
                                    > / {{ outcomeObj.totalCases }}
                                </p>
                            </div>
                            <div class="col-10">
                                <p>
                                    <strong>Esito: </strong>
                                    <span
                                        class="passed"
                                        v-if="outcomeObj.passing"
                                        ><strong>superato</strong>
                                    </span>
                                    <span class="failed" v-else>
                                        <strong>non superato</strong>
                                    </span>
                                </p>
                            </div>
                        </div>
                    </div>
                </template>

                <template #modal-footer="{ ok, cancel, hide }">
                    <!-- Button with custom close trigger value -->
                    <b-button size="md" variant="dark" @click="hide('ok')">
                        Chiudi
                    </b-button>
                </template>
            </b-modal>
    </div>
</template>

<script>
// import Prism Editor
import { PrismEditor } from "vue-prism-editor";
import "vue-prism-editor/dist/prismeditor.min.css"; // import the styles somewhere

// import highlighting library (you can use any library you want just return html string)
import { highlight, languages } from "prismjs/components/prism-core";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-javascript";
import "prismjs/themes/prism-tomorrow.css"; // import syntax highlighting styles

import axios from 'axios'

export default {
    name: 'ProgramExercise',
    props: {
		text: String,
		publicTestCases: Array,
		exerciseId: Number,
    },
    mounted() {
        axios.defaults.xsrfCookieName = 'csrftoken'
        axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
    },
	components: {
        'prism-editor': PrismEditor
    },
	data: () => {
		return {
            userProgram: '',
            loading: false,
            outcomeObj: {},
            code: '',
		}
    },
    methods: {
        submit() {
            const postData = JSON.stringify(this.userProgram)
            console.log(postData)
            this.loading = true
            axios
                .post('http://127.0.0.1:8000/eval_progsol/' + this.exerciseId + '/', postData)
                .then((response) => {
                    this.outcomeObj = response.data
                    this.$root.$emit(
                        'bv::show::modal',
                        'outcome-modal',
                        '#submit'
                    )
                    console.log(response)
                    this.loading = false
                })
                .catch((error) => {
                    alert(error)
                    console.log(error)
                })
        },
        highlighter(code) {
        return highlight(code, languages.js); //returns html
        },
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
    margin: 40px 0 0;
}
ul {
    list-style-type: none;
    padding: 0;
}

a {
    color: #42b983;
}

.passed {
    color: green;
}

.failed {
    color: red;
}

.test-case {
    padding: 5px;
    border-bottom: 1px solid lightgray;
}

.my-editor {
  background: #2d2d2d;
  color: #ccc;

  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  padding: 5px;
}

.prism-editor__textarea:focus {
  outline: none;
}

.h-350 {
  height: 350px;
}
</style>
