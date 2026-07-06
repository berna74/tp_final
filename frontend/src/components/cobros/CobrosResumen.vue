<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <div class="resumen-header">
        <h2>{{ title }}</h2>
        <div class="anio-controls">
          <label>Año</label>
          <input type="number" v-model.number="anio" min="2020" max="2035" />
          <button @click="cargarResumen" class="btn-cargar">Actualizar</button>
        </div>
      </div>

      <div v-if="loading" class="loading">Cargando resumen...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <template v-else-if="resumen">
        <div class="totales">
          <span>Deuda global: ${{ formatoMonto(resumen.totales.deuda_global) }}</span>
          <span>Socios con deuda: {{ resumen.totales.cantidad_socios_con_deuda }}</span>
        </div>

        <div class="tabla-wrap">
          <table>
            <thead>
              <tr>
                <th>Socio</th>
                <th v-for="mes in resumen.meses" :key="mes">{{ mesCorto(mes) }}</th>
                <th>Deuda total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="fila in sociosOrdenados" :key="fila.socio_id">
                <td class="socio-cell">{{ fila.socio_nombre }}</td>
                <td v-for="celda in fila.resumen_mensual" :key="`${fila.socio_id}-${celda.mes}`">
                  <span :class="['estado-chip', claseEstado(celda.estado)]" :title="detalleEstado(celda)">
                    {{ abreviarEstado(celda.estado) }}
                  </span>
                </td>
                <td class="deuda">${{ formatoMonto(fila.deuda_total) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>

      <div v-if="showClose" class="panel-actions">
        <button @click="$emit('close')" class="btn-close">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useCobrosStore } from '@/stores/cobros'
import type { CobroResumenMensual } from '@/interfaces/Cobro'

withDefaults(defineProps<{ showClose?: boolean; title?: string }>(), {
  showClose: true,
  title: 'Ver deudas',
})

defineEmits(['close'])

const cobrosStore = useCobrosStore()
const { resumen, loading, error } = storeToRefs(cobrosStore)
const anio = ref(new Date().getFullYear())

const sociosOrdenados = computed(() => {
  if (!resumen.value) return []
  return [...resumen.value.socios].sort((a, b) =>
    (a.socio_nombre || '').localeCompare(b.socio_nombre || '', 'es', { sensitivity: 'base' }),
  )
})

onMounted(() => {
  cargarResumen()
})

function cargarResumen() {
  cobrosStore.fetchResumen(anio.value)
}

function mesCorto(mes: number): string {
  const meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
  return meses[mes - 1]
}

function abreviarEstado(estado: string): string {
  if (estado === 'Pagado') return 'P'
  if (estado === 'Parcial') return 'Par'
  if (estado === 'Pendiente') return 'Pen'
  return 'SR'
}

function claseEstado(estado: string): string {
  if (estado === 'Pagado') return 'ok'
  if (estado === 'Parcial') return 'warn'
  if (estado === 'Pendiente') return 'danger'
  return 'default'
}

function detalleEstado(celda: CobroResumenMensual): string {
  return `${celda.estado} | Cuota: $${formatoMonto(celda.monto_cuota)} | Pagado: $${formatoMonto(celda.monto_pagado)} | Saldo: $${formatoMonto(celda.saldo_mes)} | Registro: ${celda.fecha_registro_pago || '-'}`
}

function formatoMonto(valor: number): string {
  return new Intl.NumberFormat('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(valor || 0))
}
</script>

<style scoped>
.panel-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  margin: 1rem 0;
}

.panel-content {
  background: white;
  padding: 24px;
  border-radius: 8px;
  width: 100%;
  border: 1px solid #e5e7eb;
  box-shadow: 0 6px 18px rgba(2, 47, 157, 0.08);
}

.resumen-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 1rem;
  margin-bottom: 1rem;
}

h2 {
  color: #022f9d;
  margin: 0;
}

.anio-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.anio-controls input {
  width: 110px;
  padding: 6px;
}

.btn-cargar {
  background: #022f9d;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 0.45rem 0.7rem;
  cursor: pointer;
}

.totales {
  display: flex;
  gap: 1.2rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.tabla-wrap {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #e5e7eb;
  padding: 8px;
  text-align: center;
}

th {
  background: #022f9d;
  color: white;
}

.socio-cell {
  text-align: left;
  font-weight: 600;
  min-width: 220px;
}

.deuda {
  font-weight: 700;
  color: #b00020;
}

.estado-chip {
  display: inline-flex;
  justify-content: center;
  min-width: 34px;
  padding: 0.2rem 0.35rem;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
}

.estado-chip.ok {
  background: #d4edda;
  color: #155724;
}

.estado-chip.warn {
  background: #fff3cd;
  color: #856404;
}

.estado-chip.danger {
  background: #f8d7da;
  color: #721c24;
}

.estado-chip.default {
  background: #e2e3e5;
  color: #383d41;
}

.panel-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.btn-close {
  background-color: #022f9d;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error {
  color: #b00020;
}
</style>
