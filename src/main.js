import Vue from 'vue'
import router from './router';
import App from './App.vue';
//import { getData } from './import.js'

import Search from './views/Search'

import vueCustomElement from 'vue-custom-element'
//Vue.use(getData(store))

Vue.config.productionTip = false

Vue.use(vueCustomElement)

new Vue({
    router,
    render: (h) => h(App),
}).$mount('#app');


