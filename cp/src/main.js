import { createApp } from 'vue';
import Notifications from '@kyvg/vue3-notification';
import App from './App.vue';
import './registerServiceWorker';
import router from './router';
import store from './store';
import '@/assets/main.scss';

createApp(App)
  .use(store)
  .use(router)
  .use(Notifications)
  .mount('#app');
