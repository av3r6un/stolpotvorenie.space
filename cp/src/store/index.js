import { createStore } from 'vuex';
import AuthService from '@/services/auth.service';

const user = JSON.parse(localStorage.getItem('_auth'));

export default createStore({
  state: user
    ? {
      isAuth: true,
      accsToken: user.accsToken,
      rfshToken: user.rfshToken,
      name: user.name,
      uid: user.uid,
      login: user.login,
    }
    : {
      isAuth: false,
      uid: null,
      accsToken: null,
      rfshToken: null,
      name: null,
      login: null,
      admin: null,
    },
  getters: {
    isAuth: (state) => state.isAuth,
    uid: (state) => state.uid,
    login: (state) => state.login,
    name: (state) => state.name,
    accsToken: (state) => state.accsToken,
    rfshToken: (state) => state.rfshToken,
  },
  mutations: {
    login(state, userInfo) {
      state.uid = userInfo.uid;
      state.login = userInfo.login;
      state.accsToken = userInfo.accs_token;
      state.rfshToken = userInfo.rfsh_token;
      state.name = userInfo.name;
      state.isAuth = true;
    },
    logout(state) {
      state.uid = null;
      state.login = null;
      state.rfshToken = null;
      state.accsToken = null;
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
    async logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
    async refresh({ commit }, userInfo) {
      return AuthService.refresh(userInfo)
        .then(() => commit('refresh', userInfo))
        .catch((err) => console.error(err));
    },
  },
  modules: {
  },
});
