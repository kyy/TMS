<template>
  <layout-div>

    <h1>Welcome to the home page</h1>
  <div v-if="authStore.isAuthenticated">
    <p>Hi there {{ authStore.user }}!</p>
    <p>You are logged in.</p>
    <button @click="logout">Logout</button>
  </div>
  <div v-else>
      <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="auth">
      <div>
        <label for="email">Email:</label>
        <input v-model="email" id="email" type="text" required
               @input="resetError">
      </div>
      <div>
        <label for="password">Password:</label>
        <input v-model="password" id="password" type="password" required
               @input="resetError">
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
  </div>
  </layout-div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import LayoutDiv from "@/components/LayoutDiv.vue";

export default {
  name: 'AuthPage',
  components: {
    LayoutDiv,
  },
  setup() {
    const authStore = useAuthStore()
    return {
      authStore
    }
  },
  data() {
    return {
      email: "",
      password: "",
      error: ""
    }
  },
  methods: {
    async auth(){
      await this.authStore.auth(this.email, this.password)
      if (!this.authStore.isAuthenticated){
        this.error = 'Login failed. Please check your credentials.'
      }
    },
    async logout() {
      try {
        await this.authStore.logout(this.$router)
      } catch (error) {
        console.error(error)
      }
    },
    resetError(){
      this.error = ""
    }
  }
}
</script>