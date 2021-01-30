import Vue from "vue/dist/vue.js"
import CourseDashboard from './components/CourseDashboard.vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import TrendChart from "vue-trend-chart"
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Install BootstrapVue
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(TrendChart)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

 new Vue({
  el: "#app",
  components: {'course-dashboard': CourseDashboard}
})
