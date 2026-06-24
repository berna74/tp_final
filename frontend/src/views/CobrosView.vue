<template>
  <div class="cobros-view">
    <CobrosList
      v-if="!mostrarLote"
      @create-lote="mostrarLote = true"
      @edit="manejarEditar"
      @show="manejarMostrar"
      @show-resumen="manejarMostrarResumen"
    />

    <CobrosLote
      v-if="mostrarLote"
      @close="mostrarLote = false"
    />

    <CobrosUpdate
      v-if="mostrarEditar && cobroSeleccionadoId"
      :cobro-id="cobroSeleccionadoId"
      @close="mostrarEditar = false"
      @updated="manejarActualizado"
    />

    <CobrosShow
      v-if="mostrarDetalle && cobroSeleccionadoId"
      :cobro-id="cobroSeleccionadoId"
      @close="mostrarDetalle = false"
    />

    <CobrosResumen
      v-if="mostrarResumen"
      @close="mostrarResumen = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CobrosList from '@/components/cobros/CobrosList.vue'
import CobrosUpdate from '@/components/cobros/CobrosUpdate.vue'
import CobrosShow from '@/components/cobros/CobrosShow.vue'
import CobrosResumen from '@/components/cobros/CobrosResumen.vue'
import CobrosLote from '@/components/cobros/CobrosLote.vue'

const mostrarEditar = ref(false)
const mostrarDetalle = ref(false)
const mostrarResumen = ref(false)
const mostrarLote = ref(true)
const cobroSeleccionadoId = ref<number | null>(null)

function manejarEditar(id: number) {
  cobroSeleccionadoId.value = id
  mostrarEditar.value = true
}

function manejarMostrar(id: number) {
  cobroSeleccionadoId.value = id
  mostrarDetalle.value = true
}

function manejarActualizado() {
  mostrarEditar.value = false
  cobroSeleccionadoId.value = null
}

function manejarMostrarResumen() {
  mostrarResumen.value = true
}
</script>

<style scoped>
.cobros-view {
  padding: 20px;
}
</style>
