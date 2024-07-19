const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: 'frontend/',
  pwa: {
    workboxOptions: {
      navigateFallback: 'index.html',
    },
    name: 'Столпотворение',
    themeColor: '#374536',
    msTileColor: '#374536',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: '#374536',
  },
  devServer: {
    proxy: {
      '/api': {
        target: 'http://192.168.0.101:48600/api',
        changeOrigin: true,
        pathRewrite: { '^/api': '' },
      },
      '/auth': {
        target: 'http://192.168.0.101:48600/auth',
        changeOrigin: true,
        pathRewrite: { '^/auth': '' },
      },
    }
  },
  // publicPath: process.env.NODE_ENV === 'production'
    // ? '/stolpotvorenie.space'
    // : '/' // only for GitHub Pages
});
