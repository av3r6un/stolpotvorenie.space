<template>
  <article class="home">
    <navBar />
  </article>
</template>
<script>
import navBar from '@/components/navBar.vue';

export default {
  name: 'HomeView',
  components: { navBar },
  data() {
    return {};
  },
  methods: {},
  mounted() {},
};
</script>
<style lang="scss" scoped>
@import '@/assets/variables.scss';
</style>
