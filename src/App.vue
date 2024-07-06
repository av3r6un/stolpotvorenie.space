<template>
  <div id="app">
    <curTains />
    <router-view/>
  </div>
</template>
<script>
import curTains from './components/curTains.vue';

export default {
  name: 'App',
  components: { curTains },
  data() {
    return {};
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
</style>
