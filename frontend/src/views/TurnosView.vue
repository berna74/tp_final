<template>
  <div class="turnos-view">
    <header class="view-header">
      <h1>Gestión de Turnos</h1>
    </header>
    <TurnosList />
  </div>
</template>

<script setup lang="ts">
import TurnosList from '@/components/turnos/TurnosList.vue'
</script>

<style scoped>
.turnos-view {
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
