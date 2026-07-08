
<template>
  <div class="container">
    <header class="view-header">
      <h1>Categorías</h1>
    </header>
    <RouterView />
  </div>
</template>
 <script setup lang="ts">
 import { useRouter } from 'vue-router'
import { onMounted } from 'vue'

const router = useRouter()

onMounted(() => {
  //console.log('componente montado')
  router.push({ name: 'categorias_list' })
})
</script>

<style scoped>
.container {
  padding: 20px;
}

.view-header {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
}

h1 {
  margin: 0;
  color: #022F9D;
}
</style>