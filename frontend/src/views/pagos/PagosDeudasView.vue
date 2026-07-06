<template>
  <div class="pagos-deudas-view">
    <CobrosResumen :show-close="false" title="Pagos" />
  </div>
</template>

<script setup lang="ts">
import CobrosResumen from '@/components/cobros/CobrosResumen.vue'
</script>

<style scoped>
.pagos-deudas-view {
  width: 100%;
}
</style>
