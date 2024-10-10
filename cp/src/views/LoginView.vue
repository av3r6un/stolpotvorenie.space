<template>
  <article class="login">
    <div class="login_wrapper">
      <div class="login_title base_title changable">Авторизация</div>
      <form class="login_form" @submit.prevent="login">
        <input type="text" class="input_wide" required autofocus autocomplete="off"
          placeholder="Логин" v-model="userInfo.login">
        <input type="password" class="input_wide" required autocomplete="off"
          placeholder="Пароль" v-model="userInfo.password">
        <button type="submit" class="btn btn_submit">Войти</button>
      </form>
    </div>
  </article>
</template>
<script>
export default {
  name: 'LoginView',
  data() {
    return {
      userInfo: {
        login: null,
        password: null,
      },
    };
  },
  methods: {
    login() {
      this.$store.dispatch('login', this.userInfo)
        .then((resp) => {
          console.log(resp);
        });
    },
  },
  mounted() {
    console.log(this.$parent);
    this.$parent.$parent.$refs.sideBar.hideSidebar();
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.login{
  display: flex;
  align-items: center;
  justify-content: center;
  &_wrapper{
    max-width: 420px;
  }
}
</style>
