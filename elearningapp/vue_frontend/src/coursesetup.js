//import Vue from 'vue'
import Vue from "vue/dist/vue.js"
import CourseSetup from './components/CourseSetup.vue'
import { BootstrapVue } from 'bootstrap-vue'

// Install BootstrapVue
Vue.use(BootstrapVue)

Vue.config.productionTip = false

new Vue({
  el: "#app",
  components: {'course-setup': CourseSetup}
});