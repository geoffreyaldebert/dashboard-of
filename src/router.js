import Vue from 'vue';
import Router from 'vue-router';
import HomepageWidget from './views/HomepageWidget.vue';
import Organisme from './views/Organisme.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: '/',
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomepageWidget,
    },
    {
      path: '/organisme/:id',
      name: 'organisme',
      component: Organisme,
    },
  ],
});
