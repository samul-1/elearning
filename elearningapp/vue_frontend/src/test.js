//import Vue from 'vue'
import Vue from "vue/dist/vue.js"
import Test from './components/Test.vue'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'

// Install BootstrapVue
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

Vue.config.productionTip = false

new Vue({
  el: "#app",
  components: {'test': Test}
});