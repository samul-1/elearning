import Vue from "vue/dist/vue.js"
import EditQuestion from './components/EditQuestion.vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
const VueScrollTo = require("vue-scrollto");


// Install BootstrapVue
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(VueScrollTo);

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.config.devtools = false
Vue.config.productionTip = false

 new Vue({
  el: "#app",
  components: {'edit-question': EditQuestion, 'vue-scrollto': VueScrollTo}
})
