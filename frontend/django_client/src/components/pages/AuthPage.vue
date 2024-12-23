<template>
  <layout-div>
    <div class="row justify-content-md-center mt-5">
      <div class="col-4">
        <div class="card">
          <div class="card-body">
            <div v-if="authStore.isAuthenticated">
              <h5 class="card-title mb-4">Log Out</h5>
              <p>Hi there {{ authStore.user }}!</p>
              <p>You are logged in.</p>
              <button
                  :disabled="isSubmitting"
                  @click="logoutAction"
                  type="button"
                  class="btn btn-primary btn-block">
                Log Out
              </button>
            </div>

            <div v-else>
              <h5 class="card-title mb-4">Вход</h5>
              <div class="login">
                <form @submit.prevent="auth">
                  <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input
                        v-model="email"
                        id="email"
                        type="text"
                        required
                        @input="resetError"
                        class="form-control"
                        placeholder="name@example.com"
                    >
                    <div v-if="validationErrors.email" class="flex flex-col">
                      <small class="text-danger">
                        {{ validationErrors?.email[0] }}
                      </small>
                    </div>
                  </div>

                  <div class="mb-3">
                    <label for="Password" class="col-form-label">Пароль</label>
                    <input
                        v-model="password"
                        id="password"
                        type="password"
                        required
                        @input="resetError"
                        class="form-control"
                        aria-describedby="passwordHelpInline"
                        placeholder="********"
                    >
                    <div v-if="validationErrors.password" class="flex flex-col">
                      <small class="text-danger">
                        {{ validationErrors?.password[0] }}
                      </small>
                    </div>
                  </div>
                  <div class="d-grid gap-2">
                    <button
                        :disabled="isSubmitting"
                        @click="authAction"
                        type="button"
                        class="btn btn-primary btn-block">
                      Войти
                    </button>
                    <p class="text-center">
                      <router-link :to="{name: 'RegPage'}">Регистрация тут</router-link>
                    </p>
                  </div>
                </form>
                <p v-if="error" class="error">{{ error }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </layout-div>
</template>

<script>
import {useAuthStore} from '@/stores/auth'
import LayoutDiv from "@/components/LayoutDiv.vue";
import apiClient from "@/axios";
import router from "@/router";
// import {useVuelidate} from '@vuelidate/core'
// import {required, email} from '@vuelidate/validators'

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
      validationErrors: {},
      isSubmitting: false,
    }
  },
  methods: {
    async authAction() {

      try {
        const response = await apiClient.post('/api/user/auth/', {
          'email': this.email,
          'password': this.password,
        });
        const authData = {user: response.data.user, isAuthenticated: true};
        const erData = {user: null, isAuthenticated: false};
        if (response.data.success) {
          localStorage.setItem('authState', JSON.stringify(authData));
          await router.push({name: 'AuthPage'});
        } else {
          localStorage.setItem('authState', JSON.stringify(erData));
        }


      } catch (error) {
        this.isSubmitting = false; // Отключаем состояние загрузки
        if (error.response && error.response.data) {
          this.validationErrors = error.response.data;
        }
        console.error(error); // Логируем ошибку для отладки
      }
    },

    async logoutAction() {
      const response = await apiClient.post('/api/user/lout/')
      if (response.data.success) {
        await router.push({name: "AuthPage"})

      }
    },
  }
}
</script>