//import Vue from 'vue'
import Vue from "vue/dist/vue.js"
import CourseSetup from './components/CourseSetup.vue'
import { BootstrapVue } from 'bootstrap-vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'


// Install BootstrapVue
Vue.use(BootstrapVue)
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.config.devtools = false
Vue.config.productionTip = false

new Vue({
  el: "#app",
  components: {'course-setup': CourseSetup}
});