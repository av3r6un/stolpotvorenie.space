import axios from 'axios';

function gatherToken(state = 'main') {
  const user = JSON.parse(localStorage.getItem('_auth'));
  const actions = { main: 'accs_token', refresh: 'rfsh_token' };
  return user ? { Authorization: `Bearer ${user[actions[state]]}` } : null;
}

class AuthService {
  async login(user) {
    this.msg = null;
    return axios
      .post('/auth/admins', user, { headers: gatherToken() })
      .then((resp) => {
        if (resp.data.status === 'success') {
          localStorage.setItem('_auth', JSON.stringify(resp.data.body));
        }
        return resp.data;
      })
      .catch((err) => err.response.data);
  }

  async logout() {
    this.msg = null;
    localStorage.removeItem('_auth');
    location.href = '/';
    return true;
  }

  async refresh(token) {
    this.msg = null;
    return axios
      .post('/auth/admins/refresh', {}, { headers: token })
      .then((resp) => {
        let rfshToken = null;

        if (resp.data.status === 'success') {
          rfshToken = resp.data.token;
          this.user = JSON.parse(localStorage.getItem('_auth'));
          this.user.accs_token = rfshToken;
          localStorage.setItem('_auth', JSON.stringify(this.user));
        }
        return rfshToken;
      })
      .catch((err) => (err.status === 403 ? 'perm_auth' : null));
  }
}

export default new AuthService();
