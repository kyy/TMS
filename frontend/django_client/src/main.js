import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import {createRouter, createWebHistory} from 'vue-router';
import AllTasks from "./components/pages/AllTasks.vue";
import AuthPage from "./components/pages/AuthPage.vue";
import RegPage from "./components/pages/RegPage.vue";
import {createApp} from "vue";


axios.defaults.withCredentials = false
axios.defaults.baseURL = process.env.VUE_APP_API_URL

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', component: AuthPage},
        {path: '/reg', component: RegPage},
        {path: '/tasks', component: AllTasks},
    ],
});

const app = createApp(App)
app.use(VueAxios, axios).use(router)
app.mount('#app')
