<template>
  <article class="clients">
    <div class="clients_forms">
      <form class="clients_add base_form" @submit.prevent="addClient">
        <div class="clients_form-title plus-sign changable form_title"
          v-if="editClient">Изменить пользователя</div>
        <div class="clients_form-title plus-sign changable form_title"
          v-else>Добавить пользователя</div>
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
      <form class="clients_add-child base_form" @submit.prevent="addNewChild">
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
        <div class="clients_table-headers">
          <div class="clients_table-headers_title changable">Фамилия</div>
          <div class="clients_table-headers_title changable">Имя</div>
          <div class="clients_table-headers_title changable">Отчество</div>
          <div class="clients_table-headers_title changable">Номер телефона</div>
          <div class="clients_table-headers_title email-th changable">E-mail</div>
          <div class="clients_table-headers_title changable">Группа</div>
          <div class="clients_table-headers_title changable">Действие</div>
        </div>
        <div class="clients_table-body">
          <div class="clients_table-row changable"
            v-for="(client, idx) in clients" :key="client.uid"
            @click="toggleParent(idx)"
            :class="[client.children.length > 0 ? 'has_children': '',
              currentParent == idx ? 'opened': '', `children--${client.children.length}`,
            ]">
            <div class="clients_children child-row" v-if="idx === currentParent">
              <div class="clients_table-row changable"
                v-for="child in client.children" :key="child.uid">
                <div class="clients_table-data child-data">
                  {{ child.name }} {{ formatAge(child.age) }}
                </div>
              </div>
            </div>
            <div class="clients_table-data">{{ client.surname }}</div>
            <div class="clients_table-data">{{ client.name }}</div>
            <div class="clients_table-data">{{ client.patronymic }}</div>
            <div class="clients_table-data" v-html="formatPhone(client.phone)"></div>
            <div class="clients_table-data email-td" v-html="formatMail(client.email)"></div>
            <div class="clients_table-data">{{ client.group }}</div>
            <div class="clients_table-data actions-td">
              <div class="clients_table-action action-edit" @click.stop="initEditClient(idx)">
                <mIcon name="user-edit" :width="24" :height="24" />
              </div>
              <div class="clients_table-action action-add_abon"
                @click.stop="addAbonement(client.uid)"
                title="Добавить абонемент">
                <mIcon name="abonement" :width="24" :height="24" />
              </div>
              <div class="clients_table-action action-delete"
                @click="deleteClient.stop(client.uid, idx)">
                <mIcon name="delete" :width="24" :height="24" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </article>
</template>
<script>
import Backend from '../services/backend.service';
import dropDown from '../components/dropDown.vue';
import mIcon from '../components/materialIcon.vue';

export default {
  name: 'ClientsView',
  components: { dropDown, mIcon },
  data() {
    return {
      backend: new Backend(),
      currentParent: null,
      editClient: false,
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
      if (this.editClient) {
        const currentUid = this.newClient.uid;
        this.backend.put(`/client/${currentUid}`, this.newClient)
          .then((resp) => {
            const currentClient = this.clients.forEach((client, idx) => {
              let returningIndex = null;
              if (client.uid === currentUid) {
                returningIndex = idx;
              }
              return returningIndex;
            });
            console.log(currentClient);
            this.clients = this.clients.toSpliced(currentClient, 1, resp);
            this.reset('newClient');
            this.editClient = false;
          })
          .catch((err) => console.error(err));
      } else {
        this.backend.post('/clients', this.newClient)
          .then((resp) => {
            this.clients.push(resp);
            this.reset('newClient');
          })
          .catch((err) => console.error(err));
      }
    },
    addNewChild() {
      this.backend.put('/clients', this.newChild)
        .then((resp) => {
          const childParentUid = this.newChild.parentUid;
          this.reset('newChild');
          this.$refs.parentDD.reset();
          this.addChildToParent(childParentUid, resp);
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
    addChildToParent(parentUid, child) {
      this.clients.forEach((parent) => {
        if (parent.uid === parentUid) {
          parent[parentUid].children.push(child);
        }
      });
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
    toggleParent(idx) {
      if (this.currentParent === null) {
        this.currentParent = idx;
      } else if (this.currentParent !== idx) {
        this.currentParent = idx;
      } else {
        this.currentParent = null;
      }
    },
    formatAge(age) {
      const lastNumber = age % 100 || age % 10;
      switch (lastNumber) {
        case 1: return `${age} год`;
        case 2:
        case 3:
        case 4:
          return `${age} года`;
        default:
          return `${age} лет`;
      }
    },
    deleteClient(uid, idx) {
      this.backend.delete(`/client/${uid}`)
        .then(() => { this.clients.splice(idx, 1); })
        .catch((err) => console.error(err));
    },
    initEditClient(idx) {
      this.editClient = true;
      this.newClient = this.clients[idx];
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
  &_children{
    position: absolute;
    left: 0;
  }
  .cct_row{
    position: relative;
  }
  &_table{
    margin-top: 20px;
    font-family: $text-font;
    &-wrapper{
      padding: 0 10px;
    }
    &-data{
      min-width: 150px;
      text-align: center;
      user-select: none;
      padding: 5px 0;
      &.child-data{
        min-width: 300px;
      }
      &.email-td{
        min-width: 210px;
        max-width: 210px;
        text-overflow: ellipsis;
        overflow: hidden;
        padding: 5px;
      }
      &.actions-td{
        display: flex;
        width: 150px;
        justify-content: space-around;
      }
    }
    &-row{
      display: flex;
      position: relative;
      &.has_children{
        cursor: pointer;
        &.opened{
          margin-bottom: 30px;
          &:before{
            content: '\f078';
          }
        }
        @for $i from 0 through 4 {
          &.children--#{$i}.opened{
            margin-bottom: calc(30px * #{$i});
          }
        }
        &:before{
          content: '\f054';
          position: absolute;
          font-family: 'FontAwesome';
          top: calc(50% - 7.5px);
          left: -15px;
          width: 15px;
          height: 15px;
          font-size: 15px;
        }
      }
      .child-row{
        position: absolute;
        top: 100%;
      }
    }
    &-headers{
      display: flex;
      font-weight: bold;
      text-align: center;
      &_title{
        min-width: 150px;
        &.email-th{
          min-width: 210px;
        }
      }
    }
  }
}
</style>
