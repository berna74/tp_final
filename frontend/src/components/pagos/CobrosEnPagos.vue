<template>
  <div class="cobros-en-pagos">
    <div class="list-header">
      <h2>Cobros registrados</h2>
    </div>

    <div v-if="loading" class="loading">Cargando cobros...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="cobros.length === 0" class="empty">No hay cobros registrados</div>

    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Socio</th>
            <th>Período</th>
            <th>Cuota</th>
            <th>Pagado</th>
            <th>Saldo</th>
            <th>Estado</th>
            <th>Fecha de registro de pago</th>
            <th>Método</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in cobros" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.socio_nombre }}</td>
            <td>{{ formatoPeriodo(item.mes, item.anio) }}</td>
            <td class="monto">${{ formatoMonto(item.monto_cuota) }}</td>
            <td class="monto">${{ formatoMonto(item.monto_pagado) }}</td>
            <td class="monto saldo">${{ formatoMonto(item.saldo_mes) }}</td>
            <td>
              <span :class="['badge', claseEstado(item.estado)]">{{ item.estado }}</span>
            </td>
            <td>{{ formatoFecha(item.fecha_registro_pago) }}</td>
            <td>{{ item.metodo_pago || '-' }}</td>
          </tr>
        </tbody>
      </table>

      <div class="pagination-controls">
        <button @click="irAPagina(currentPage - 1)" :disabled="currentPage <= 1" class="btn-pagination">
          Anterior
        </button>
        <span class="pagination-info">Página {{ currentPage }} de {{ totalPages }}</span>
        <button @click="irAPagina(currentPage + 1)" :disabled="currentPage >= totalPages" class="btn-pagination">
          Siguiente
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useCobrosStore } from '@/stores/cobros'

const cobrosStore = useCobrosStore()
const { cobros, loading, error, currentPage, totalPages } = storeToRefs(cobrosStore)

onMounted(() => {
  cobrosStore.fetchCobros()
})

function formatoMonto(valor: number | string): string {
  return new Intl.NumberFormat('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(valor || 0))
}

function formatoFecha(valor: string | null): string {
  if (!valor) return '-'
  const fecha = new Date(`${valor}T00:00:00`)
  return fecha.toLocaleDateString('es-AR')
}

function formatoPeriodo(mes: number, anio: number): string {
  const meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
  return `${meses[mes - 1]} ${anio}`
}

function claseEstado(estado: string): string {
  if (estado === 'Pagado') return 'badge-ok'
  if (estado === 'Parcial') return 'badge-warn'
  if (estado === 'Pendiente') return 'badge-danger'
  return 'badge-default'
}

function irAPagina(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    cobrosStore.fetchCobros(page)
  }
}
</script>

<style scoped>
.cobros-en-pagos {
  padding: 20px;
}

.list-header {
  margin-bottom: 20px;
}

h2 {
  color: #022f9d;
  margin: 0;
}

.table-container {
  overflow-x: auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: #022f9d;
  color: white;
}

th,
td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #cccccc;
}

.monto {
  font-weight: 700;
}

.saldo {
  color: #c1121f;
}

.badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
}

.badge-ok {
  background: #d4edda;
  color: #155724;
}

.badge-warn {
  background: #fff3cd;
  color: #856404;
}

.badge-danger {
  background: #f8d7da;
  color: #721c24;
}

.badge-default {
  background: #e2e3e5;
  color: #383d41;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  margin-top: 1rem;
  padding: 1rem;
}

.btn-pagination {
  background: #022f9d;
  color: white;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}

.btn-pagination:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  color: #022f9d;
  font-weight: 600;
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 1rem;
}

.error {
  color: #b00020;
}
</style>
