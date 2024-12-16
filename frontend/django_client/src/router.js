import {createRouter, createWebHistory} from 'vue-router'
import AllTasks from "@/components/pages/AllTasks.vue";
import AuthPage from "@/components/pages/AuthPage.vue";
import LoutPage from "@/components/pages/LoutPage.vue";
import RegPage from "@/components/pages/RegPage.vue";


const routes = [
    {
        path: '/tasks',
        name: 'home',
        component: AllTasks
    },
    {
        path: '/',
        name: 'AuthPage',
        component: AuthPage
    },
    {
        path: '/lout',
        name: 'LoutPage',
        component: LoutPage
    },
    {
        path: '/reg',
        name: 'RegPage',
        component: RegPage
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router