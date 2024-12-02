import { useNotification } from '@kyvg/vue3-notification';
import request from './axios.service';

const { notify } = useNotification();

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

    if (this.msg && this.msg !== '') {
      notify({
        title: 'Успешно!',
        text: this.msg,
        type: 'success',
      });
    }
    return result;
  }

  manageError(err) {
    this.status = 'error';
    this.msg = err.response.data.message || err.response.msg;
    notify({
      title: 'Ошибка!',
      text: this.msg,
      type: this.status,
    });
    return Promise.reject(err);
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
      .put(url, data)
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
