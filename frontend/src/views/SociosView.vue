<template>
  <div class="socios-view">
    <header class="view-header">
      <h1>Gestión de Socios</h1>
    </header>
    <SociosList />
  </div>
</template>

<script setup lang="ts">
import SociosList from '@/components/socios/SociosList.vue'
</script>

<style scoped>
.socios-view {
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
  color: #022F9D;
  margin: 0;
}
</style>
