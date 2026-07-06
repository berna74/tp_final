<template>
  <div class="alumnos-view">
    <AlumnosCreate 
      v-if="showCreate" 
      @close="showCreate = false" 
      @created="handleCreated" 
    />
    <AlumnosList 
      @create="showCreate = true" 
      @edit="handleEdit"
      @show="handleShow"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AlumnosList from '@/components/alumnos/AlumnosList.vue'
import AlumnosCreate from '@/components/alumnos/AlumnosCreate.vue'

const showCreate = ref(false)
const router = useRouter()

function handleCreated() {
  showCreate.value = false
}

function handleEdit(id: number) {
  router.push({ name: 'alumnos-edit', params: { id } })
}

function handleShow(id: number) {
  router.push({ name: 'alumnos-show', params: { id } })
}
</script>

<style scoped>
.alumnos-view {
  padding: 20px;
}
</style>
