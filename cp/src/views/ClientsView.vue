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
          <dropDown placeholder="Выбрать родителя" nested :options="clients" v-if="clients"
          v-model:selected="newChild.parentUid" ref="parentDD" nested-param="fullName" />
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
    </div>
    <div class="clients_table">
      <div class="clients_table-wrapper">
        <div class="clients_table-headers tr">
          <div class="client_table-title td changable">Имя</div>
          <div class="client_table-title td changable">Фамилия</div>
          <div class="client_table-title td changable">Отчество</div>
          <div class="client_table-title td changable">Номер телефона</div>
          <div class="client_table-title td changable">E-mail</div>
          <div class="client_table-title td changable">Группа</div>
        </div>
        <div class="clients_table-data tr" v-for="client in clients" :key="client.uid">
          <div class="client_table-row folder" v-if="client.children"></div>
          <div class="clients_table-row td changable">{{ client.name }}</div>
          <div class="clients_table-row td changable">{{ client.surname }}</div>
          <div class="clients_table-row td changable">{{ client.patronymic }}</div>
          <div class="clients_table-row td changable" v-html="formatPhone(client.phone)"></div>
          <div class="clients_table-row td changable" v-html="formatMail(client.email)"></div>
          <div class="clients_table-row td changable" v-if="client.group">
            {{ client.group.name }}
          </div>
          <div class="clients_table-row td group_selector" v-else></div>
        </div>
      </div>
    </div>
  </article>
</template>
<script>
import Backend from '../services/backend.service';
import dropDown from '../components/dropDown.vue';

export default {
  name: 'ClientsView',
  components: { dropDown },
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
      const tel = phoneNumber.replace(/^\+?(\d)(\d{3})(\d{3})(\d{2})(\d{2})$/, '+$1($2) $3-$4-$5');
      return `<a href="tel:${phoneNumber}" class="base_link">${tel}</a>`;
    },
    formatMail(emailAddress) {
      return `<a href="mailto:${emailAddress}" class="base_link">${emailAddress}</a>`;
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
    margin-top: 20px;
    &-wrapper{
      display: table;
      .tr{
        display: table-row;
      }
      .td{
        min-width: 100px;
        padding: 4px;
        display: table-cell;
      }
    }
    &-headers{
      font-weight: bold;
      text-align: center;
    }
    font-family: $text-font;
    &-td{
      text-align: center;
      min-width: 120px;
    }
  }
}
</style>
