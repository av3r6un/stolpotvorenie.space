<template>
  <div class="home">
    <div class="home_text changable" :class="mobile ? 'mobile' : ''" >
      Пустая страница для статистики. <br>
      <router-link to="/schedule" class="base_link text_link">Перейти к расписанию</router-link>
    </div>
  </div>
</template>
<script>
export default {
  name: 'HomeView',
  data() {
    return {
      mobile: false,
    };
  },
  mounted() {
    this.mobile = this.$isMobile();
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.home{
  &_text{
    margin-top: 55px;
    font-size: 20px;
    font-family: $text-font;
    &.mobile{
      margin-top: 10px;
    }
  }
}
</style>
