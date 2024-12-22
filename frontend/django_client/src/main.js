import App from './App.vue'
import VueAxios from 'vue-axios'
import {createApp} from "vue";
import {createPinia} from 'pinia'
import router from './router'
import apiClient from "@/axios";
import {useAuthStore} from "@/stores/auth";

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"


async function initializeApp() {
    // Создаем приложение Vue и используем необходимые плагины
    // await setupCSRFToken()

    const app = createApp(App);

    app.use(createPinia());
    app.use(VueAxios, apiClient);
    app.use(router); //инициализируем роуты
    // Moнтируем приложение

    app.mount('#app');
    useAuthStore()
}

// Функция для инициализации приложения
initializeApp().catch(err => {
    console.error('Failed to initialize app:', err);
});