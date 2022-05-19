import Vue from 'vue';
import Router from 'vue-router';
import HomepageWidget from './views/HomepageWidget.vue';
import Test from './views/Test.vue';

Vue.use(Router);


export default new Router({
  mode: 'history',
  base: '/dashboard-of/',
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomepageWidget,
    },
    {
      path: '/test',
      name: 'test',
      component: Test,
    },
  ],
});
