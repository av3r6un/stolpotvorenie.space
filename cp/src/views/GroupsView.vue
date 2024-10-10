<template>
  <article class="groups">
    <div class="groups_forms">
      <form class="groups_add" @submit.prevent="addGroup">
        <div class="groups_add-title plus-sign changable form_title">Создать группу</div>
        <dropDown :options="courses" nested placeholder="Выбрать курс"
          v-model:selected="newGroup.courseUid" ref="courseDd"/>
        <dropDown :options="types" seminested placeholder="Выбрать тип"
          v-model:selected="newGroup.type" ref="typeDd"/>
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
      <form class="groups_populate" @submit.prevent="populateGroup">
        <div class="groups_populate-title plus-sign changable form_title">Пополнить группу</div>
        <dropDown :options="clients" nested placeholder="Выбрать пользователя"
          v-model:selected="addUserToGroup.userUid" ref="clientsDd" />
        <dropDown :options="groups" nested placeholder="Выбрать группу"
          v-model:selected="addUserToGroup.groupId" ref="groupsDd" />
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
    </div>
    <div class="groups_table">
      <div class="groups_group changable" v-for="group in groups" :key="group.id">
        {{ group.name }}
      </div>
    </div>
  </article>
</template>
<script>
import dropDown from '../components/dropDown.vue';
import Backend from '../services/backend.service';

export default {
  name: 'GroupsView',
  components: { dropDown },
  data() {
    return {
      backend: new Backend(),
      newGroup: {
        courseUid: null,
        type: null,
        steaded: true,
      },
      types: { mature: 'Взрослая', children: 'Детская', mixed: 'Смешанная' },
      groups: [],
      courses: null,
      steaded: true,
      addUserToGroup: {
        groupId: null,
        userUid: null,
      },
      clients: [],
    };
  },
  methods: {
    gatherEssentialsData() {
      this.backend.get('/groups/main')
        .then((resp) => {
          this.types = this.backend.extra;
          this.groups = resp.groups;
          this.courses = resp.courses;
          this.clients = resp.clients;
        })
        .catch((err) => console.error(err));
    },
    addGroup() {
      this.backend.post('/groups', this.newGroup)
        .then((resp) => {
          this.groups.push(resp);
          this.$refs.courseDd.reset();
          this.$refs.typeDd.reset();
        })
        .catch((err) => console.error(err));
    },
  },
  mounted() {
    this.gatherEssentialsData();
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.groups{
  &_forms{
    display: flex;
    justify-content: space-around;
    align-items: start;
  }
  &_add, &_populate{
    max-width: 400px;
    min-width: 380px;
  }
}
</style>
