import request from './axios.service';

class Backend {
  msg = null;

  status = null;

  extra = null;

  manageResp(resp) {
    let result = null;
    if (resp.status !== 'success') {
      this.msg = resp.message;
      return result;
    }

    this.msg = resp.message ? resp.message : '';
    result = resp.body ? resp.body : null;
    this.extra = resp.extra;

    return result;
  }

  manageError(err) {
    this.status = 'error';
    // this.msg = err.response.msg;
    return err;
  }

  async get(url, parameters = null) {
    return request
      .get(url, { params: parameters })
      .then((resp) => this.manageResp(resp))
      .catch((err) => this.manageError(err));
  }

  async post(url, data) {
    return request
      .post(url, data)
      .then((resp) => this.manageResp(resp))
      .catch((err) => this.manageError(err));
  }

  async put(url, data) {
    return request
      .post(url, data)
      .then((resp) => this.manageResp(resp))
      .catch((err) => this.manageError(err));
  }

  async delete(url, parameters) {
    return request
      .delete(url, { params: parameters })
      .then((resp) => this.manageResp(resp))
      .catch((err) => this.manageError(err));
  }
}

export default Backend;
