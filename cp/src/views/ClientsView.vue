<template>
  <article class="clients">
    <div class="clients_forms">
      <form class="clients_add base_form" @submit.prevent="addClient">
        <div class="clients_form-title plus-sign changable form_title">Добавить пользователя</div>
        <input type="text" placeholder="Имя" required class="input_wide"
          v-model="newClient.name">
        <input type="text" placeholder="Фамилия" required class="input_wide"
          v-model="newClient.surname">
        <input type="text" placeholder="Отчество" class="input_wide"
          v-model="newClient.patronymic">
        <input type="text" placeholder="Телефон" required class="input_wide"
          v-model="newClient.phone">
        <input type="text" placeholder="E-mail" required class="input_wide"
          v-model="newClient.email">
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
      <form class="clients_add-child base_form">
        <div class="clients_form-title plus-sign changable form_title">Добавить ребенка</div>
        <input type="text" placeholder="Имя" required class="input_wide"
          v-model="newChild.name">
        <input type="number" placeholder="Возраст" required class="input_wide"
          v-model="newChild.age">
        <!-- place for selector -->
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
    </div>
    <div class="clients_table">
      <table class="clients_table-table">
        <th class="clients_table-th changable">Имя</th>
        <th class="clients_table-th changable">Фамилия</th>
        <th class="clients_table-th changable">Отчество</th>
        <th class="clients_table-th changable">Номер телефона</th>
        <th class="clients_table-th changable">E-Mail</th>
        <!-- <th class="clients_table-th changable">Действие</th> -->
        <tr class="clients_table-tr" v-for="client in clients" :key="client.uid">
          <td class="clients_table-td changable">{{ client.name }}</td>
          <td class="clients_table-td changable">{{ client.surname }}</td>
          <td class="clients_table-td changable">{{ client.patronymic }}</td>
          <td class="clients_table-td changable" v-html="formatPhone(client.phone)"></td>
          <td class="clients_table-td changable">{{ client.email }}</td>
          <!-- <td class="clients_table-td"></td> -->
        </tr>
      </table>
    </div>
  </article>
</template>
<script>
import Backend from '../services/backend.service';

export default {
  name: 'ClientsView',
  data() {
    return {
      backend: new Backend(),
      newClient: {
        name: null,
        surname: null,
        patronymic: null,
        phone: null,
        email: null,
      },
      newChild: {
        name: null,
        age: null,
        parentUid: null,
      },
      clients: [],
    };
  },
  methods: {
    addClient() {
      this.backend.post('/clients', this.newClient)
        .then((resp) => {
          this.clients.push(resp);
          this.reset('newClient');
        })
        .catch((err) => console.error(err));
    },
    gatherEssentialsData() {
      this.backend.get('/clients/main')
        .then((resp) => {
          this.clients = resp.clients;
        })
        .catch((err) => console.error(err));
    },
    reset(obj) {
      Object.keys(this[obj]).forEach((key) => {
        this[obj][key] = null;
      });
    },
    formatPhone(phoneNumber) {
      const tel = phoneNumber.replace(/^\+?(\d)(\d{3})(\d{3})(\d{2})(\d{2})$/, '+$1($2)$3-$4-$5');
      return `<a href="tel:${phoneNumber}" class="base_link">${tel}</a>`;
    },
  },
  mounted() {
    this.gatherEssentialsData();
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.clients{
  &_forms{
    display: flex;
    justify-content: space-around;
    align-items: start;
  }
  &_table{
    font-family: $text-font;
    &-td{
      text-align: center;
      min-width: 120px;
    }
  }
}
</style>
