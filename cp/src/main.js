import { createApp } from 'vue';
import Notifications from '@kyvg/vue3-notification';
import VueMobileDetection from 'vue-mobile-detection';
import App from './App.vue';
import './registerServiceWorker';
import router from './router';
import store from './store';
import '@/assets/main.scss';

createApp(App)
  .use(router)
  .use(store)
  .use(Notifications)
  .use(VueMobileDetection)
  .mount('#app');
