<template>
  <sideBar @sidebar-toggled="toggleContent" @theme="toggleTheme"
    ref="sideBar"/>
  <router-view class="main_content"
    :class="[!short ? 'full' : '', dark ? 'dark' : '']"/>
</template>
<script>
import sideBar from '@/components/sideBar.vue';
import Storage from './services/storage.service';

export default {
  name: 'App',
  components: {
    sideBar,
  },
  data() {
    return {
      localStorage: new Storage(),
      short: true,
      dark: false,
    };
  },
  methods: {
    toggleContent(val) {
      this.short = val;
    },
    toggleTheme(dark) {
      this.dark = dark;
    },
    changeGlobalTheme() {
      this.dark = this.localStorage.themeColors.dark;
      this.$refs.sideBar.dark = this.localStorage.themeColors.dark;
    },
  },
  mounted() {
    this.toggleTheme(this.localStorage.themeColors.dark);
    this.$refs.sideBar.dark = this.localStorage.themeColors.dark;
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
#app{
  position: relative;
}
.footer{
  position: absolute;
  bottom: 0;
  // position: absolute;
  // bottom: 0;
  margin-top: 40px;
}
</style>
