<template>
  <layout-div>
    <div class="row justify-content-md-center mt-5">
      <div class="col-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title mb-4">Регистрация</h5>
            <form>
              <div class="mb-3">
                <label
                    htmlFor="username"
                    class="form-label">Имя
                </label>
                <input
                    type="text"
                    class="form-control"
                    id="username"
                    name="username"
                    v-model="username"
                    placeholder="username"
                />
                <div v-if="validationErrors.username" class="flex flex-col">
                  <small class="text-danger">
                    {{ validationErrors?.username[0] }}
                  </small>
                </div>
              </div>
              <div class="mb-3">
                <label
                    htmlFor="email"
                    class="form-label">Email
                </label>
                <input
                    type="email"
                    class="form-control"
                    id="email"
                    name="email"
                    v-model="email"
                    placeholder="name@example.com"
                />
                <div v-if="validationErrors.email" class="flex flex-col">
                  <small class="text-danger">
                    {{ validationErrors?.email[0] }}
                  </small>
                </div>
              </div>
              <div class="mb-3">
                <label
                    htmlFor="password"
                    class="form-label">Пароль
                </label>
                <input
                    type="password"
                    class="form-control"
                    id="password"
                    name="password"
                    v-model="password"
                    placeholder="********"
                />
                <div v-if="validationErrors.password" class="flex flex-col">
                  <small class="text-danger">
                    {{ validationErrors?.password[0] }}
                  </small>
                </div>
              </div>
              <div class="d-grid gap-2">
                <button
                    :disabled="isSubmitting"
                    @click="registerAction()"
                    type="button"
                    class="btn btn-primary btn-block">Вперед!
                </button>
                <p
                    class="text-center">
                  <router-link :to="{name: 'AuthPage'}">Вход тут</router-link>
                </p>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </layout-div>
</template>

<script>
import apiClient from "@/axios";
import LayoutDiv from '../LayoutDiv.vue';

export default {
  name: 'RegPage',
  components: {
    LayoutDiv,
  },
  data() {
    return {
      username: '',
      email: '',
      password: '',
      validationErrors: {},
      isSubmitting: false,
    };
  },
  methods: {
    registerAction() {
      this.isSubmitting = true

      apiClient.post('/api/user/reg/', {
        username: this.username,
        email: this.email,
        password: this.password,
      }).then(response => {
        this.$router.push({name: 'AuthPage'})
        return response
      })
          .catch(error => {
            this.isSubmitting = false
            if (error.response.data !== undefined) {
              this.validationErrors = error.response.data
            }
            return error
          });
    }
  },
};
</script>