import { defineStore } from 'pinia'
import apiClient from "@/axios";

export const useAuthStore = defineStore('auth', {
    state: () => {
        const storedState = localStorage.getItem('authState')
        return storedState ? JSON.parse(storedState) : {
            user: null,
            isAuthenticated: false
        }
    },
    actions: {

        async auth(email, password) {
            let response = await apiClient.post('/api/user/auth/', {
                'email': email,
                'password': password,
            })

            if (response.data.success) {
                this.isAuthenticated = true
                this.user = response.data['user']
                this.saveState()

            } else {
                this.user = null
                this.isAuthenticated = false
                this.saveState()
            }
        },


        async logout(router=null) {
            try {
                const response = await apiClient.post('api/user/lout/')
                if (response.data.success) {
                    this.user = null
                    this.isAuthenticated = false
                    this.saveState()
                    if (router){
                        await router.push({name: "AuthPage"})
                    }
                }
            } catch (error) {
                console.error('Logout failed', error)
                throw error
            }
        },

        async fetchUser() {
            try {
                const response = await apiClient.get('api/user/auth/')
                let data = response.data
                if (data.status === 200) {
                    this.user = data.username
                    this.isAuthenticated = true
                }
                else{
                    this.user = null
                    this.isAuthenticated = false
                }
            } catch (error) {
                console.error('Failed to fetch user', error)
                this.user = null
                this.isAuthenticated = false
            }
            this.saveState()
        },

        saveState() {
            /*
            We save state to local storage to keep the
            state when the user reloads the page.

            This is a simple way to persist state. For a more robust solution,
            use pinia-persistent-state.
             */
            localStorage.setItem('authState', JSON.stringify({
                user: this.user,
                isAuthenticated: this.isAuthenticated
            }))
        }
    }
})

