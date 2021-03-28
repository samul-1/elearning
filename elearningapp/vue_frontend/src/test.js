//import Vue from 'vue'
import Vue from "vue/dist/vue.js"
import Test from './components/Test.vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Install BootstrapVue
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.config.productionTip = false
Vue.config.devtools = false
new Vue({
  el: "#app",
  components: {'test': Test}
});