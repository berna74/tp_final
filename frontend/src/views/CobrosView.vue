<template>
  <div class="cobros-view">
    <CobrosList
      v-if="!mostrarLote"
      @create-lote="mostrarLote = true"
      @edit="manejarEditar"
      @show="manejarMostrar"
      @show-resumen="manejarMostrarResumen"
      @show-matriz="manejarMostrarMatriz"
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

    <CobrosMatrizDosAnios
      v-if="mostrarMatriz"
      @close="mostrarMatriz = false"
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
import CobrosMatrizDosAnios from '@/components/cobros/CobrosMatrizDosAnios.vue'

const mostrarEditar = ref(false)
const mostrarDetalle = ref(false)
const mostrarResumen = ref(false)
const mostrarMatriz = ref(false)
const mostrarLote = ref(false)
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

function manejarMostrarMatriz() {
  mostrarMatriz.value = true
}
</script>

<style scoped>
.cobros-view {
  padding: 20px;
}
</style>
