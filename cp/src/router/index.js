import { createRouter, createWebHashHistory } from 'vue-router';
// import store from '@/store';
// import UserService from '@/services/user.service';
import HomeView from '../views/HomeView.vue';
import ClientsView from '../views/ClientsView.vue';
import GroupsView from '../views/GroupsView.vue';
import ScheduleView from '../views/ScheduleView.vue';
import AttendenceView from '../views/AttendenceView.vue';
import TeachersView from '../views/TeachersView.vue';
import LoginView from '../views/LoginView.vue';

const routes = [
  {
    path: '/',
    name: 'Панель Управления',
    component: HomeView,
  },
  {
    path: '/clients',
    name: 'Пользователи',
    component: ClientsView,
  },
  {
    path: '/groups',
    name: 'Группы',
    component: GroupsView,
  },
  {
    path: '/schedule',
    name: 'Расписание',
    component: ScheduleView,
  },
  {
    path: '/attendence',
    name: 'Посещения',
    component: AttendenceView,
  },
  {
    path: '/teachers',
    name: 'Преподаватели',
    component: TeachersView,
  },
  {
    path: '/login',
    name: 'Авторизация',
    component: LoginView,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  linkExactActiveClass: 'active',
  linkActiveClass: '',
});

// const us = new UserService();
// router.beforeEach((to, from, next) => {
//   // const userAuthenticated = store.getters.isAuth;
//   // if (!userAuthenticated) next('/login');
// });

// router.beforeEach((to, from, next) => {
//   const isAdmin = store.getters.admin;
//   const canGoNext = us.verifyJwt();
//   console.log('user can go next: ', canGoNext);
//   if (to.matched.some((route) => route.meta.adminAccess)) {
//     const adminCanGoNext = canGoNext && isAdmin;
//     if (adminCanGoNext) next();
//     if (!canGoNext) next('/login');
//     if (!isAdmin) from();
//   } else {
//     next();
//   }
// });

export default router;
