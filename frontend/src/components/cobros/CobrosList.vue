<template>
  <div class="cobros-list">
    <div class="list-header">
      <h2>Gestión de Cobros</h2>
      <div class="header-actions">
        <button v-if="authStore.puedeEscribir" class="btn-secondary" @click="$emit('create-lote')">
          Registrar cobro/s
        </button>
        <button class="btn-secondary" @click="$emit('show-resumen')">
          Ver deudas
        </button>
        <button class="btn-secondary" @click="$emit('show-matriz')">
          Ver últimos 12 meses
        </button>
      </div>
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
            <th>Tipo</th>
            <th>Período</th>
            <th>Cuota</th>
            <th>Pagado</th>
            <th>Saldo</th>
            <th>Estado</th>
            <th>Fecha de registro de pago</th>
            <th>Método</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in cobros" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.socio_nombre }}</td>
            <td>{{ item.tipo_cobro === 'dia_cancha' ? 'Día de cancha' : 'Mensual' }}</td>
            <td>{{ formatoPeriodo(item.mes, item.anio) }}</td>
            <td class="monto">${{ formatoMonto(item.monto_cuota) }}</td>
            <td class="monto">${{ formatoMonto(item.monto_pagado) }}</td>
            <td class="monto saldo">${{ formatoMonto(item.saldo_mes) }}</td>
            <td>
              <span :class="['badge', badgeEstado(item.estado)]">{{ item.estado }}</span>
            </td>
            <td>{{ formatoFecha(item.fecha_registro_pago) }}</td>
            <td>{{ item.metodo_pago || '-' }}</td>
            <td class="actions">
              <button @click="$emit('show', item.id)" class="btn-icon" title="Ver">Ver</button>
              <button
                v-if="authStore.puedeEscribir"
                @click="$emit('edit', item.id)"
                class="btn-icon"
                title="Editar"
              >
                Editar
              </button>
              <button
                v-if="authStore.puedeEscribir"
                @click="eliminar(item.id)"
                class="btn-icon btn-delete"
                title="Eliminar"
              >
                Eliminar
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="pagination-controls">
        <button @click="irAPagina(currentPage - 1)" :disabled="currentPage <= 1" class="btn-pagination">
          Anterior
        </button>
        <span class="pagination-info">Página {{ currentPage }} de {{ totalPages }}</span>
        <button
          @click="irAPagina(currentPage + 1)"
          :disabled="currentPage >= totalPages"
          class="btn-pagination"
        >
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
import { useAuthStore } from '@/stores/auth'

const emit = defineEmits(['show', 'edit', 'show-resumen', 'show-matriz', 'create-lote'])

const cobrosStore = useCobrosStore()
const authStore = useAuthStore()
const { cobros, loading, error, currentPage, totalPages } = storeToRefs(cobrosStore)

onMounted(() => {
  cobrosStore.fetchCobros()
})

function badgeEstado(estado: string): string {
  if (estado === 'Pagado') return 'badge-ok'
  if (estado === 'Parcial') return 'badge-warn'
  if (estado === 'Pendiente') return 'badge-danger'
  return 'badge-default'
}

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

async function eliminar(id: number) {
  if (!authStore.puedeEscribir) {
    return
  }

  if (confirm('¿Está seguro de eliminar este cobro?')) {
    await cobrosStore.deleteCobro(id)
  }
}

function irAPagina(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    cobrosStore.fetchCobros(page)
  }
}

</script>

<style scoped>
.cobros-list {
  padding: 20px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

h2 {
  color: #022f9d;
  margin: 0;
}

.btn-secondary {
  border: none;
  padding: 0.7rem 1rem;
  border-radius: 6px;
  cursor: pointer;
}


.btn-secondary {
  background: #022f9d;
  color: #fff;
}

.table-container {
  overflow-x: auto;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: #022f9d;
  color: #fff;
}

th,
td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ccc;
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

.actions {
  display: flex;
  gap: 0.35rem;
}

.btn-icon {
  border: 1px solid #d0d7de;
  background: #fff;
  border-radius: 4px;
  padding: 0.35rem 0.45rem;
  cursor: pointer;
}

.btn-delete {
  color: #b00020;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  padding: 12px;
}

.btn-pagination {
  border: 1px solid #d0d7de;
  background: #fff;
  border-radius: 6px;
  padding: 0.4rem 0.7rem;
  cursor: pointer;
}

.loading,
.error,
.empty {
  padding: 1rem;
}

.error {
  color: #b00020;
}
</style>
