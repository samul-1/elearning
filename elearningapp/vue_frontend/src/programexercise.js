import Vue from "vue/dist/vue.js"
import ProgramExercise from './components/ProgramExercise.vue'
import { BootstrapVue } from 'bootstrap-vue'

// Install BootstrapVue
Vue.use(BootstrapVue)
Vue.config.productionTip = false
Vue.config.devtools = false
new Vue({
  el: "#app",
  components: {'program-exercise': ProgramExercise}
});