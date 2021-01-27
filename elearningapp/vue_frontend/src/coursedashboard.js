import Vue from "vue/dist/vue.js"
import CourseDashboard from './components/CourseDashboard.vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import TrendChart from "vue-trend-chart"
// Install BootstrapVue
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(TrendChart)

Vue.config.productionTip = false

 new Vue({
  el: "#app",
  components: {'course-dashboard': CourseDashboard}
})
