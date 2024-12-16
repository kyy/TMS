<template>
  <layout-div>
    <div class="row justify-content-md-center mt-5">
      <div class="col-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title mb-4">Log Out</h5>
            <form>
              <div class="d-grid gap-2">
                <button
                    :disabled="isSubmitting"
                    @click="logoutAction()"
                    type="button"
                    class="btn btn-primary btn-block">Log Out Now
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
import axios from 'axios';
import LayoutDiv from '../LayoutDiv.vue';

export default {
  name: 'LoutPage',
  components: {
    LayoutDiv,
  },
  data() {
    return {
      validationErrors: {},
      isSubmitting: false,
    };
  },
  methods: {
    logoutAction() {
      this.isSubmitting = true
      axios.post('/api/user/lout/')
          .then(response => {
            localStorage.setItem('token', "")
            this.$router.push('/')
            return response
          })
          .catch(error => {
            this.isSubmitting = false
            if (error.response.data.errors !== undefined) {
              this.validationErrors = error.response.data.errors
            }
            return error
          });
    }
  },
};
</script>