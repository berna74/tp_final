<template>
  <div class="cobros-view">
    <CobrosList
      v-if="!mostrarLote"
      @create-lote="mostrarLote = true"
      @edit="manejarEditar"
      @show="manejarMostrar"
    />

    <CobrosLote
      v-if="mostrarLote"
      @close="mostrarLote = false"
    />

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import CobrosList from '@/components/cobros/CobrosList.vue'
import CobrosLote from '@/components/cobros/CobrosLote.vue'

const mostrarLote = ref(false)
const router = useRouter()

function manejarEditar(id: number) {
  router.push({ name: 'cobros-edit', params: { id } })
}

function manejarMostrar(id: number) {
  router.push({ name: 'cobros-show', params: { id } })
}
</script>

<style scoped>
.cobros-view {
  padding: 20px;
}
</style>
