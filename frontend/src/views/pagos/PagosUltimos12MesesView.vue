<template>
  <div class="pagos-ultimos-12-view">
    <CobrosMatrizDosAnios :show-close="false" />
  </div>
</template>

<script setup lang="ts">
import CobrosMatrizDosAnios from '@/components/cobros/CobrosMatrizDosAnios.vue'
</script>

<style scoped>
.pagos-ultimos-12-view {
  width: 100%;
}
</style>
