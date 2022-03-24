import {createApp} from 'vue';
import App from './App.vue';
import store from './store';
import router from "./router";
import axios from './plugins/axios';
import VueAxios from 'vue-axios';
import vClickOutside from "click-outside-vue3";
import './index.css';

createApp(App).use(store).use(router).use(VueAxios, axios).use(vClickOutside).mount('#app')
