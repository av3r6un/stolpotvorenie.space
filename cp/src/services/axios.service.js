import axios from 'axios';
import AuthService from './auth.service';

const request = axios.create({
  baseURL: '/api/cp',
});

function gatherToken(state = 'main') {
  const user = JSON.parse(localStorage.getItem('_auth'));
  const actions = { main: 'accs_token', refresh: 'rfsh_token' };
  return user ? { Authorization: `Bearer ${user[actions[state]]}` } : null;
}

request.interceptors.request.use(
  (config) => {
    const accs = gatherToken();
    const cfg = config;
    cfg.headers.Authorization = accs.Authorization;
    return cfg;
  },
  (err) => Promise.reject(err),
);

async function refreshAccessToken() {
  const refToken = gatherToken('refresh');
  return AuthService.refresh(refToken);
}

let isRef = false;

request.interceptors.response.use(
  (resp) => resp.data,
  async (err) => {
    const { response, config } = err;
    if (response.status === 403) {
      if (!isRef) isRef = true;
      const newAcessToken = await refreshAccessToken();
      if (newAcessToken && newAcessToken === 'perm_auth') {
        return Promise.reject(err);
      }
      if (newAcessToken) {
        config.headers.Authorization = `Bearer ${newAcessToken}`;
        return request(config);
      }
    }
    return Promise.reject(err);
  },
);

export default request;
