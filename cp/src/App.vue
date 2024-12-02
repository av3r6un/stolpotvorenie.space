<template>
  <sideBar @sidebar-toggled="toggleContent" @theme="toggleTheme"
    ref="sideBar"/>
  <Notifications width="340" :max="3" ignore-duplicates/>
  <div class="page_title base_title changable" >{{ $route.name }}</div>
  <router-view class="main_content"
    :class="[!short ? 'full' : '', dark ? 'dark' : '', mobile ? 'mobile' : '']"/>
</template>
<script>
import { Notifications } from '@kyvg/vue3-notification';
import sideBar from '@/components/sideBar.vue';
import Storage from './services/storage.service';

export default {
  name: 'App',
  components: {
    sideBar, Notifications,
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
    manageTitle() {
      document.title = `${this.$route.name} - Панель управления`;
    },
  },
  watch: {
    $route: 'manageTitle',
  },
  mounted() {
    this.mobile = this.$isMobile();
    this.short = !this.mobile;
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
