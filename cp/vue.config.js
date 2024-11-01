const { defineConfig } = require('@vue/cli-service');
const webpack = require('webpack');

module.exports = defineConfig({
  transpileDependencies: true,
  pwa: {
    workboxOptions: {
      navigateFallback: 'index.html',
    },
    name: 'Панель управление - СТОЛПОТВОРЕНИЕ',
    themeColor: '#374536',
    msTileColor: '#374536',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: '#374536',
  },
  outputDir: '../frontend/cp',
  devServer: {
    proxy: {
      '/api': {
        target: `http://${process.env.HOST}:48600/api`,
        changeOrigin: true,
        pathRewrite: { '^/api': '' },
      },
      '/auth': {
        target: `http://${process.env.HOST}:48600/auth`,
        changeOrigin: true,
        pathRewrite: { '^/auth': '' },
      },
    }
  },
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'false',
      }),
    ],
  },
  // publicPath: process.env.NODE_ENV === 'production'
    // ? '/stolpotvorenie.space'
    // : '/' // only for GitHub Pages
});
