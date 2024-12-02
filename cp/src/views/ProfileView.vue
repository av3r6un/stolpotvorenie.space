<template>
  <article class="profile">
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
        <PassInput required placeholder="Старый пароль" v-model:text="changePass.old" />
        <PassInput required placeholder="Новый пароль" v-model:text="changePass.new" />
        <PassInput required placeholder="Подтвердите новый пароль" v-model:text="changePass.new2"
          ref="validatable" @input="validate" class="validatable"/>
        <button type="submit" class="btn btn_submit">Сохранить</button>
      </form>
    </div>
    <div class="profile_form-toggle">
      <mIcon name="sun" :reversed="!localStorage.themeColors.dark"/>
      <Toggle v-model:checked="localStorage.themeColors.dark" />
      <mIcon name="moon" :reversed="!localStorage.themeColors.dark"/>
    </div>
    <div class="profile_leave">
      <button type="button" class="btn btn_submit"
        @click="$store.dispatch('logout')">Выйти из аккаунта</button>
    </div>
  </article>
</template>
<script>
import Backend from '@/services/backend.service';
import Toggle from '@/components/toggle.vue';
import PassInput from '@/components/PassInput.vue';
import mIcon from '@/components/materialIcon.vue';

export default {
  name: 'ProfileView',
  components: { mIcon, Toggle, PassInput },
  data() {
    return {
      backend: new Backend(),
      profileInfo: {},
      localStorage: this.$parent.$parent.localStorage,
      changePass: {
        old: null,
        new: null,
        new2: null,
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
    editTheme(value) {
      this.localStorage.changeColorSettings('dark', value);
      this.$parent.$parent.changeGlobalTheme();
    },
    validate() {
      const inputObj = this.$refs.validatable.$el;
      const isValidPassword = this.changePass.new === this.changePass.new2;
      return isValidPassword ? inputObj.classList.remove('invalid') : inputObj.classList.add('invalid');
    },
  },
  computed: {},
  mounted() {
    this.gatherEssentialsData();
    console.log(this.$refs);
  },
  watch: {
    'localStorage.themeColors.dark': 'editTheme',
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
    max-width: 85%;
    .profile_form{
      min-width: 300px;
    }
    @media screen {
      @media (max-width: 640px) {
        max-width: 100%;
        .profile_form{
          margin-top: 10px;
          &:first-of-type{
            margin-top: 0;
          }
        }
      }
    }
  }
  &_form{
    max-width: 400px;
    width: 100%;
    &-toggle{
      position: absolute;
      @media screen {
        @media (max-width: 640px) {
          position: relative;
          display: flex;
          top: auto;
          right: auto;
          justify-content: center;
          margin-top: 10px;
        }
      }
      right: 15px;
      top: 40px;
      display: flex;
      align-items: center;
    }
  }
  &_leave{
    margin-top: 15px;
    .btn_submit{
      margin-top: 0px;
    }
  }
}
</style>
