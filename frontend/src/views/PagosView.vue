<template>
  <div class="pagos-view">
    <div class="pagos-top-actions">
      <RouterLink :to="{ name: 'pagos-ultimos-12' }" class="btn-tab">Ver últimos 12 meses</RouterLink>
    </div>

    <RouterView />
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.pagos-view {
  padding: 20px;
}

.pagos-top-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
  padding: 1rem;
}

.btn-tab {
  text-decoration: none;
  border: none;
  padding: 0.7rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  background: #022f9d;
  color: #fff;
  font-weight: 600;
}

.btn-tab.router-link-active {
  background: #00cdff;
  color: #001a57;
}
</style>
