import App from './App.vue'
import VueAxios from 'vue-axios'
import {createApp} from "vue";
import router from './router'
import apiClient from "@/axios";

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

createApp(App)
    .use(VueAxios, apiClient)
    .use(router)
    .mount('#app')
