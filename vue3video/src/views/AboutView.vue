<template>
  <div class="about">
    <h1>This is a new about page</h1>
    <button color="primary"
           size="large"
            block @click="getTodoById(1)">
        Test
  </button>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>

<script setup>
import { ref } from 'vue'
import { getTodo } from '@/api/todo';

const todo = ref({});

function getTodoById(id) {
  todo.value = getTodo(id);
}

</script><
