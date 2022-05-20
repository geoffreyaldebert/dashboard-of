import Vue from 'vue';
import Router from 'vue-router';
import Search from './views/Search.vue';
import Organisme from './views/Organisme.vue';
import Home from './views/Home.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: '/',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/recherche/:search/page/:page',
      name: 'detail-search',
      component: Search,
    },
    {
      path: '/recherche/:search',
      name: 'search',
      component: Search,
    },
    {
      path: '/organisme/:id',
      name: 'organisme',
      component: Organisme,
    },
  ],
});
