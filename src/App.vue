<template>
  <div id="app">
    <router-view/>
    <div class="footer">
      Информация на сайте не является публичной офертой.
    </div>
  </div>
</template>
<script>

export default {
  name: 'App',
  data() {
    return {};
  },
  metaInfo: {
    title: 'Столпотворение',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover' },
      { name: 'theme-color', content: '#357357', media: '(prefers-color-scheme: dark)' },
    ],
  },
};
</script>
<style lang="scss" scoped>
@import "@/assets/variables.scss";
.footer{
  margin-top: auto;
  text-align: center;
  color: $white;
  font-family: $text-font;
  margin: 10px 0;
}
</style>
