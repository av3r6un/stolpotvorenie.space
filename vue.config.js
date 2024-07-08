const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  pwa: {
    name: 'Столпотворение',
    themeColor: '#374536',
    msTileColor: '#374536',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: '#374536',
  }
  // publicPath: process.env.NODE_ENV === 'production'
    // ? '/stolpotvorenie.space'
    // : '/' // only for GitHub Pages
});
