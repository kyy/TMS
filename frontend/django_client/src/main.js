import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import {createApp} from "vue";
import {createPinia} from 'pinia'
import {useAuthStore} from './stores/auth'
import router from './router'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

axios.defaults.withCredentials = false
axios.defaults.baseURL = process.env.VUE_APP_API_URL


createApp(App)
    .use(VueAxios, axios)
    .use(router)
    .use(createPinia())
    .mount('#app')

const authStore = useAuthStore()
authStore.setCsrfToken()