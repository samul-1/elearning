import Vue from "vue/dist/vue.js"
import CourseCp from './components/CourseCp.vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'

// Install BootstrapVue
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

Vue.config.productionTip = false

 new Vue({
  el: "#app",
  components: {'course-cp': CourseCp}
})
