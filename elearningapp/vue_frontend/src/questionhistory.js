//import Vue from 'vue'
import Vue from "vue/dist/vue.js"
import QuestionHistory from './components/QuestionHistory.vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Install BootstrapVue
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.config.productionTip = false

// new Vue({
//   render: h => h(QuestionHistory),
// }).$mount('#app')

 new Vue({
  el: "#app",
  components: {'question-history': QuestionHistory}
})
