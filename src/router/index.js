import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '../store';
import UserService from '../services/user.service';
import HomeView from '../views/HomeView.vue';
import AuthView from '../views/AuthView.vue';
import PanelView from '../views/PanelView.vue';

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
    path: '/cp',
    name: 'Панель управления',
    component: PanelView,
    meta: {
      adminAccess: true,
    },
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

const us = new UserService();

router.beforeEach((to, from, next) => {
  const isAdmin = store.getters.admin;
  const canGoNext = us.verifyJwt();
  console.log('user can go next: ', canGoNext);
  if (to.matched.some((route) => route.meta.adminAccess)) {
    const adminCanGoNext = canGoNext && isAdmin;
    if (adminCanGoNext) next();
    if (!canGoNext) next('/login');
    if (!isAdmin) from();
  } else {
    next();
  }
});

export default router;
