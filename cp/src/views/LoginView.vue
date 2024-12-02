<template>
  <article class="login">
    <div class="login_wrapper">
      <form class="login_form" @submit.prevent="login">
        <input type="text" class="input_wide" required autofocus autocomplete="off"
          placeholder="Логин" v-model="userInfo.login">
        <PassInput placeholder="Пароль" required v-model:text="userInfo.password" />
        <button type="submit" class="btn btn_submit">Войти</button>
      </form>
    </div>
  </article>
</template>
<script>
import PassInput from '@/components/PassInput.vue';

export default {
  name: 'LoginView',
  components: { PassInput },
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
          this.$notify({
            title: resp.status === 'success' ? 'Успешно!' : 'Ошибка!',
            text: resp.message,
            type: resp.status,
          });
        })
        .catch((err) => {
          this.$notify({
            title: err.response.data.status === 'success' ? 'Успешно' : 'Ошибка!',
            text: err.response.data.message,
            type: err.response.data.status,
          });
        });
    },
  },
  mounted() {
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
    max-width: 400px;
    width: 100%;
  }
  .base_title{
    margin-bottom: 10px;
  }
}
</style>
