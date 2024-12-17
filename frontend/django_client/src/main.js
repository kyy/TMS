import App from './App.vue'
import VueAxios from 'vue-axios'
import {createApp} from "vue";
import { createPinia } from 'pinia'
import router from './router'
import apiClient from "@/axios";
import {useAuthStore} from "@/stores/auth";

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"


createApp(App)
    .use(createPinia())
    .use(VueAxios, apiClient)
    .use(router)
    .mount('#app')

useAuthStore()