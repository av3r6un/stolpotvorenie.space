<template>
  <article class="auth">
    <div class="auth_wrapper">
      <div class="auth_title base_title">Авторизация</div>
      <form class="auth_form" @submit.prevent="login">
        <input type="text" class="input_wide" id="login" required autocompete="off"
          v-model="uData.login" placeholder="Логин">
        <input type="password" id="password" required autocomplete="off" class="input_wide"
          v-model="uData.password" placeholder="Пароль" @input="validatePassword"
          ref="passwordInput">
        <div class="auth_form-row">
          <checkBox name="Запомнить пароль" id="rm" />
          <router-link to="/lost" class="base_link">Забыли пароль?</router-link>
        </div>
        <button type="submit" class="btn btn_submit">Войти</button>
      </form>
    </div>
  </article>
</template>
<script>
import checkBox from '@/components/checkBox.vue';
import Backend from '../services/backend.service';

export default {
  name: 'AuthView',
  components: { checkBox },
  data() {
    return {
      backend: new Backend(),
      uData: {
        login: null,
        password: null,
        rm: null,
      },
    };
  },
  methods: {
    validatePassword() {
      let validPassword = false;
      const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{5,}$/;
      validPassword = pattern.test(this.uData.password);
      return validPassword ? this.$refs.passwordInput.classList.remove('not-valid') : this.$refs.passwordInput.classList.add('not-valid');
    },
    login() {
      this.$store.dispatch('loginAdmn', this.uData)
        .then((resp) => {
          console.log(resp);
          setTimeout(() => {
            this.$router.push('/');
          }, 1500);
        })
        .catch((err) => console.error(err));
    },
  },
  mounted() {},
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.auth{
  height: calc(100vh - 45px);
  display: flex;
  align-items: center;
  justify-content: center;
  &_wrapper{
    width: 470px;
    border-radius: 10px;
    padding: 25px 20px;
    box-shadow: 1px 1px 10px 1px rgba($color: $black, $alpha: .3);
  }
  &_form{
    font-family: $text-font;
    &-row{
      color: $black;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin: 10px 0;
    }
  }
  @media screen {
    @media (max-width: 535px) {
      max-width: 95%;
      margin: 0 auto;
    }
  }
}
</style>
