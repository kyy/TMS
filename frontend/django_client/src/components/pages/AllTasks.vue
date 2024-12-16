<script>
import axios from "axios";

export default {
  data() {
    return {
      // tasks
      tasks: ['']
    }
  },
  methods: {
    async getData() {
      try {
        // fetch tasks
        const response = await axios.get('http://localhost:8000/api/task/');
        // set the data returned as tasks
        this.tasks = response.data;
        console.log(response);
      } catch (error) {
        // log the error
        console.log(error);
      }
    },
  },
  created() {
    // Fetch tasks on page load
    this.getData();
  }
}
</script>

<template>
  <div class="tasks_container">
    <div class="tasks_content">
      <h1>Tasks</h1>
      <ul class="tasks_list">
        <li v-for="task in tasks['results']" :key="task.id">
          <h2>{{ task.name }}</h2>
          <p>{{ task.description }}</p>
          <button @click="toggleTask(task)">
            {{ task.status ? 'Undo' : 'Complete' }}
          </button>
          <button @click="deleteTask(task)">Delete</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>

</style>