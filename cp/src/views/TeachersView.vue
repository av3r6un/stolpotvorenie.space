<template>
  <article class="teachers">
    <div class="teachers_forms">
      <form class="teachers_add" @submit.prevent="addTeacher">
        <input type="text" class="input_wide" required autocomplete="off"
          v-model="newTeacher.name" placeholder="Имя">
        <input type="text" class="input_wide" required autocomplete="off"
          v-model="newTeacher.surname" placeholder="Фамилия">
        <input type="text" class="input_wide" required autocomplete="off"
          v-model="newTeacher.patronymic" placeholder="Отчество">
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
    </div>
    <div class="teachers_teachers">
      <div class="teachers_teacher changable" v-for="teacher in teachers" :key="teacher.uid">
        Преподаватель: {{ teacher.full_name }}
      </div>
    </div>
  </article>
</template>
<script>
import Backend from '../services/backend.service';

export default {
  name: 'TeachersView',
  data() {
    return {
      backend: new Backend(),
      newTeacher: {
        name: null,
        surname: null,
        patronymic: null,
      },
      teachers: [],
    };
  },
  methods: {
    addTeacher() {
      this.backend.post('/teachers', this.newTeacher)
        .then((resp) => {
          const teacher = this.newTeacher;
          teacher.uid = resp;
          teacher.full_name = `${teacher.surname} ${teacher.name} ${teacher.patronymic}`;
          this.teachers.push(teacher);
        })
        .catch((err) => console.error(err));
    },
    gatherTeachers() {
      this.backend.get('/teachers')
        .then((resp) => {
          this.teachers = resp;
        })
        .catch((err) => console.error(err));
    },
  },
  mounted() {
    this.gatherTeachers();
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.teachers{
  &_add{
    max-width: 420px;
  }
}
</style>
