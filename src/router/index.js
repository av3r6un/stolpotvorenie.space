import Vue from 'vue';
import VueRouter from 'vue-router';
import HomeView from '../views/HomeView.vue';
import AuthView from '../views/AuthView.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Главная',
    component: HomeView,
  },
  {
    path: '/login',
    name: 'Авторизация',
    component: AuthView,
  },
  {
    path: '/login/admin',
    name: 'Вход в панель управления',
    component: AuthView,
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;
