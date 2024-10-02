<template>
  <nav class="navbar">
    <ul class="navbar_nav">
      <li class="navbar_item"><logoType/></li>
      <li class="navbar_item">О проекте</li>
      <li class="navbar_item">Новости</li>
      <li class="navbar_item">Мастер-классы</li>
      <li class="navbar_item">Лекторий</li>
      <li class="navbar_item">Аренда</li>
      <li class="navbar_item">Магазин</li>
      <li class="navbar_item">Контакты</li>
    </ul>
  </nav>
</template>
<script>
import logoType from './logoType.vue';

export default {
  name: 'navBar',
  components: { logoType },
  data() {
    return {};
  },
  methods: {},
  mounted() {},
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
</style>
