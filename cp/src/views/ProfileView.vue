<template>
  <article class="profile">
    <div class="profile_title base_title changable">Мой профиль</div>
    <div class="profile_forms">
      <form class="profile_forms-edit profile_form" @submit.prevent="changeInfo">
        <div class="profile_forms-title plus-sign changable form_title">Изменить информацию</div>
        <input type="text" class="input_wide" required autocomplete="off"
          v-model="profileInfo.login" placeholder="Логин">
        <input type="text" autocomplete="off" required placeholder="Фамилия"
          class="input_wide" v-model="profileInfo.surname">
        <input type="text" autocomplete="off" required placeholder="Имя"
          class="input_wide" v-model="profileInfo.name">
        <input type="text" autocomplete="off" placeholder="Отчество"
          class="input_wide" v-model="profileInfo.patronymic">
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
      <form class="profile_form-edit_password profile_form" @submit.prevent="changePassword">
        <div class="profile_forms-title plus-sign changable form_title">Изменить пароль</div>
        <input type="password" required autocomplete="off" placeholder="Старый пароль"
          class="input_wide" v-model="changePass.old">
        <input type="password" required autocomplete="off" placeholder="Новый пароль"
          class="input_wide" v-model="changePass.new">
        <input type="password" required autocomplete="off" @input="validate"
          placeholder="Подтвердите новый пароль" class="input_wide validatable"
          v-model="changePass.new2" ref="validatable">
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
      <form class="profile_form-edit-theme profile_form" @submit.prevent="editTheme">
        <div class="profile_forms-title plus-sign changable form_title">Изменить тему</div>
        <dropDown placeholder="Выбрать тему" :options="pageThemes" nested
          v-model:selected="themeSettings.dark" ref="darkThemeDD" />
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
    </div>
    <div class="profile_leave">
      <button type="button" class="btn btn_submit"
        @click="$store.dispatch('logout')">Выйти из аккаунта</button>
    </div>
  </article>
</template>
<script>
import Backend from '@/services/backend.service';
import dropDown from '@/components/dropDown.vue';

export default {
  name: 'ProfileView',
  components: { dropDown },
  data() {
    return {
      backend: new Backend(),
      profileInfo: {},
      changePass: {
        old: null,
        new: null,
        new2: null,
      },
      themeSettings: {
        dark: false,
      },
      pageThemes: [
        { uid: false, name: 'Светлая' },
        { uid: true, name: 'Тёмная' },
      ],
    };
  },
  methods: {
    gatherEssentialsData() {
      this.backend.get('/me')
        .then((resp) => { this.profileInfo = resp; })
        .catch((err) => console.error(err));
    },
    changePassword() {
      delete this.changePass.new2;
      this.backend.put('/admins/info', this.changePass)
        .then(() => {
          console.log(this.backend.msg);
          this.changePass.new = null;
          this.changePass.old = null;
        })
        .catch((err) => console.error(err));
    },
    changeInfo() {
      this.backend.post('/admins/info', this.profileInfo)
        .then(() => {
          console.log(this.backend.msg);
        })
        .catch((err) => console.error(err));
    },
    editTheme() {
      Object.keys(this.themeSettings).forEach((key) => {
        this.$parent.$parent.localStorage.changeColorSettings(key, this.themeSettings[key]);
      });
      this.$refs.darkThemeDD.reset();
      this.$parent.$parent.changeGlobalTheme();
    },
    validate() {
      const isValidPassword = this.changePass.new === this.changePass.new2;
      return isValidPassword ? this.$refs.validatable.classList.remove('invalid') : this.$refs.validatable.classList.add('invalid');
    },
  },
  computed: {},
  mounted() {
    this.gatherEssentialsData();
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.profile{
  &_title{
    margin-bottom: 20px;
  }
  &_forms{
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
  }
  &_form{
    max-width: 400px;
  }
}
</style>
