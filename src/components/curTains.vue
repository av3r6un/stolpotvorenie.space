<template>
  <transition name="appearance">
    <article class="curtains" v-show="curtainsShown">
      <div class="curtains_left curtain"></div>
      <div class="curtains_middle curtain"></div>
      <div class="curtains_right curtain"></div>
      <div class="title">Столпотворение</div>
    </article>
  </transition>
</template>
<script>
export default {
  name: 'curTains',
  data() {
    return {
      curtainsShown: true,
    };
  },
  mounted() {
    setTimeout(() => {
      this.curtainsShown = false;
    }, 3000);
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.curtains{
  position: fixed;
  height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  z-index: 3;
  .curtain{
    height: calc(100% + 100px);
    width: 960px;
  }
  &_left{
    background: url('@/assets/imgs/left_curtain.png') no-repeat 50% 0% / cover;
  }
  &_right{
    background: url('@/assets/imgs/right_curtain.png') no-repeat 50% 0% / cover;
  }
  &_middle{
    display: none;
    background: none;
  }
  .title{
    position: absolute;
    font-family: $title-font;
    text-transform: uppercase;
    font-size: 96px;
    color: $white;
    user-select: none;
    @media screen {
      @media (max-width: 960px) {
        font-size: 36px;
      }
    }
  }
}
.appearance-leave-active {
  animation: appear 3s linear;
}
@keyframes appear {
  100% {
    transform: translateY(calc(-100vh - 100px));
  }
}
</style>
