import store from '../store';

class UserService {
  tokens = null;

  constructor() {
    this.authToken = store.getters.accs_token;
    this.rfshToken = store.getters.rfsh_token;
  }

  verifyJwt() {
    return !this.isExpiredToken(this.rfshToken);
  }

  isExpiredToken(token) {
    console.log(token);
    if (!token) {
      return true;
    }
    this.expired = true;
    const tokenParts = token.split('.');
    const body = JSON.parse(atob(tokenParts[1]));
    const exp = new Date(body.exp * 1000);
    const now = new Date();
    return now > exp;
  }
}

export default UserService;
