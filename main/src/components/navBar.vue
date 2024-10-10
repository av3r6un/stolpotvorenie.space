<template>
  <nav class="navbar">
    <ul class="navbar_nav">
      <li class="navbar_item"><logoType :inverted="inverted"/></li>
      <li class="navbar_item">
        <router-link to="/about" class="base_link">О проекте</router-link>
      </li>
      <li class="navbar_item">
        <router-link to="/news" class="base_link">Новости</router-link>
      </li>
      <li class="navbar_item">
        <router-link to="/mc" class="base_link">Мастер-классы</router-link>
      </li>
      <li class="navbar_item">
        <router-link to="/lectures" class="base_link">Лекторий</router-link>
      </li>
      <li class="navbar_item">
        <router-link to="/rent" class="base_link">Аренда</router-link>
      </li>
      <li class="navbar_item">
        <router-link to="/shop" class="base_link">Магазин</router-link>
      </li>
      <li class="navbar_item">
        <router-link to="/contacts" class="base_link">Контакты</router-link>
      </li>
    </ul>
  </nav>
</template>
<script>
import logoType from './logoType.vue';

export default {
  name: 'navBar',
  components: { logoType },
  data() {
    return {
      inverted: false,
    };
  },
  methods: {},
  mounted() {},
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.navbar{
  &_nav{
    display: flex;
    list-style-type: none;
    align-items: center;
    padding: 0 48px;
    font-family: $text-font;
  }
  &_item{
    display: flex;
    align-items: center;
    min-height: 60px;
    &:first-child{
      margin-right: auto;
    }
    margin-right: 35px;
    &:last-child{
      margin-right: 0;
    }
  }
}
</style>
