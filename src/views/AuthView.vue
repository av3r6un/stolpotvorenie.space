<template>
  <article class="auth">
    <div class="auth_wrapper">
      <div class="auth_title base_title">Авторизация</div>
      <form class="auth_form" @submit.prevent="loginUser">
        <label for="login" class="form_label">Логин</label>
        <input type="text" class="input_wide" id="login" required autocompete="off"
          v-model="uData.login" placeholder="">
        <label for="password" class="form_label">Пароль</label>
        <input type="password" id="password" required autocomplete="off" class="input_wide"
          v-model="uData.password" placeholder="" @input="validatePassword"
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

export default {
  name: 'AuthView',
  components: { checkBox },
  data() {
    return {
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
    loginUser() {
      if (this.$router.path.split('/').includes('admin')) {
        this.$store.dispatch('/admin/login');
      }
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
    backdrop-filter: blur(20px);
    background: rgba(217, 217, 217, .05);
    border-radius: 10px;
    padding: 15px 20px;
  }
  &_form{
    font-family: $text-font;
    &-row{
      color: $white;
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
