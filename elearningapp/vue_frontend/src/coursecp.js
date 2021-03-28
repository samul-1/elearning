import Vue from "vue/dist/vue.js"
import CourseCp from './components/CourseCp.vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Install BootstrapVue
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.config.devtools = false
Vue.config.productionTip = false

 new Vue({
  el: "#app",
  components: {'course-cp': CourseCp}
})
