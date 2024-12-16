<template>
  <layout-div>
    <div class="row justify-content-md-center mt-5">
      <div class="col-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title mb-4">Смена пароля</h5>
            <form>
              <p v-if="Object.keys(validationErrors).length !== 0" class='text-center '>
                <small class='text-danger'>Incorrect Password</small></p>
              <div class="mb-3">
                <label
                    htmlFor="old_password"
                    class="form-label">
                  Старый пароль
                </label>
                <input
                    v-model="old_password"
                    type="password"
                    class="form-control"
                    id="old_password"
                    name="old_password"
                />
              </div>
              <div class="mb-3">
                <label
                    htmlFor="new_password"
                    class="form-label">Новый пароль
                </label>
                <input
                    v-model="new_password"
                    type="password"
                    class="form-control"
                    id="new_password"
                    name="new_password"
                />
              </div>
              <div class="d-grid gap-2">
                <button
                    :disabled="isSubmitting"
                    @click="ChpswdAction()"
                    type="button"
                    class="btn btn-primary btn-block">Сменить
                </button>
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
  name: 'AuthPage',
  components: {
    LayoutDiv,
  },
  data() {
    return {
      old_password: '',
      new_password: '',
      validationErrors: {},
      isSubmitting: false,
    };
  },
  methods: {
    ChpswdAction() {
      this.isSubmitting = true
      let payload = {
        old_password: this.old_password,
        new_password: this.new_password,
      }
      apiClient.post('/api/user/chpswd/', payload)
          .then(response => {
            localStorage.setItem('csrftoken', response.data['csrftoken'])
            this.$router.push('/')
            return response
          })
          .catch(error => {
            this.isSubmitting = false
            if (error.response.data.errors !== undefined) {
              this.validationErrors = error.response.data.errors
            }
            if (error.response.data.error !== undefined) {
              this.validationErrors = error.response.data.error
            }
            return error
          });
    }
  },
};
</script>