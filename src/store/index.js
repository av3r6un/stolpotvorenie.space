import Vue from 'vue';
import Vuex from 'vuex';
import AuthService from '@/services/auth.service';

Vue.use(Vuex);

const user = JSON.parse(localStorage.getItem('_auth'));

export default new Vuex.Store({
  state: user
    ? {
      isAuth: true,
      accsToken: user.accs_token,
      rfshToken: user.rfsh_token,
      uid: user.uid,
      login: user.login,
    }
    : {
      isAuth: false,
      uid: null,
      accsToken: null,
      rfshToken: null,
      login: null,
      admin: null,
    },
  getters: {
    isAuth: (state) => state.isAuth,
    uid: (state) => state.uid,
    login: (state) => state.login,
    admin: (state) => state.admin,
    accsToken: (state) => state.accsToken,
    rfshToken: (state) => state.rfshToken,
  },
  mutations: {
    login(state, userInfo) {
      state.uid = userInfo.uid;
      state.login = userInfo.login;
      state.accsToken = userInfo.accs_token;
      state.rfshToken = userInfo.rfsh_token;
      state.isAuth = true;
    },
    loginAdmin(state, userInfo) {
      state.uid = userInfo.uid;
      state.login = userInfo.login;
      state.accsToken = userInfo.accs_token;
      state.rfshToken = userInfo.rfsh_token;
      state.admin = true;
      state.isAuth = true;
    },
    logout(state) {
      state.uid = null;
      state.login = null;
      state.rfshToken = null;
      state.accsToken = null;
      state.isAuth = null;
    },
    register(state, userInfo) {
      state.uid = userInfo.uid;
      state.isAuth = false;
    },
    refresh(state, userInfo) {
      state.isAuth = true;
      state.accsToken = userInfo;
    },
  },
  actions: {
    async login({ commit }, userInfo) {
      return AuthService.login(userInfo)
        .then((userData) => {
          commit('login', userData);
          return Promise.resolve(userData);
        })
        .catch((err) => console.error(err));
    },
    async loginAdmin({ commit }, userInfo) {
      return AuthService.loginAdmin(userInfo)
        .then((userData) => {
          commit('loginAdmin', userData);
          return Promise.resolve(userData);
        })
        .catch((err) => console.error(err));
    },
    async logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
    async refresh({ commit }, userInfo) {
      return AuthService.refresh(userInfo)
        .then(() => commit('refresh', userInfo));
    },
    async register({ commit }, userInfo) {
      return AuthService.register(userInfo)
        .then((userData) => {
          commit('register', userData);
          return Promise.resover(userData);
        })
        .catch((err) => console.error(err));
    },
  },
  modules: {
  },
});
