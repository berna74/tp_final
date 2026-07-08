<template>
  <div class="pelotitas-view">
    <section class="operaciones-panel">
      <header class="view-header">
        <h1>Pelotitas</h1>
        <p>Registro de compra y venta de pelotitas</p>
      </header>

      <div v-if="pelotitasStore.loading" class="state-message">Cargando operaciones...</div>
      <div v-else-if="pelotitasStore.error" class="state-message error">
        {{ pelotitasStore.error }}
      </div>
      <div v-else-if="operacionesPelotitas.length === 0" class="state-message">
        No hay operaciones de pelotitas registradas en Ingresos/Gastos.
      </div>

      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Operacion</th>
            <th>Rubro</th>
            <th>Concepto</th>
            <th>Metodo</th>
            <th class="text-right">Monto</th>
            <th>Observaciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="mov in operacionesPelotitas" :key="`${mov.tipo}-${mov.id ?? mov.fecha}`">
            <td>{{ formatDate(mov.fecha) }}</td>
            <td>
              <span class="badge" :class="mov.operacionClase">{{ mov.operacion }}</span>
            </td>
            <td>{{ mov.rubro }}</td>
            <td>{{ mov.concepto }}</td>
            <td>{{ mov.metodo }}</td>
            <td class="text-right">{{ formatMoney(Number(mov.monto)) }}</td>
            <td>{{ mov.observaciones || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import type { MovimientoFinanciero } from '@/interfaces/MovimientoFinanciero'
import { usePelotitasStore } from '@/stores/pelotitas'

type OperacionPelotitas = MovimientoFinanciero & {
  operacion: 'Compra' | 'Venta'
  operacionClase: 'compra' | 'venta'
}

const pelotitasStore = usePelotitasStore()

const operacionesPelotitas = computed<OperacionPelotitas[]>(() => {
  const ingresos = pelotitasStore.ingresosFinancieros.map((mov) => ({
    ...mov,
    operacion: 'Venta' as const,
    operacionClase: 'venta' as const,
  }))

  const gastos = pelotitasStore.gastosFinancieros.map((mov) => ({
    ...mov,
    operacion: 'Compra' as const,
    operacionClase: 'compra' as const,
  }))

  return [...ingresos, ...gastos].sort(
    (a, b) => new Date(b.fecha).getTime() - new Date(a.fecha).getTime(),
  )
})

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-AR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

const formatMoney = (value: number | null | undefined) => {
  if (!value) return '$0'
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    maximumFractionDigits: 0,
  }).format(value)
}

onMounted(async () => {
  await pelotitasStore.fetchFinanzasRelacionadas()
})
</script>

<style scoped>
.pelotitas-view {
  background: #f5f7fa;
  padding: 20px;
}

.operaciones-panel {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
  padding: 1.25rem;
}

.view-header {
  margin-bottom: 1rem;
}

.view-header h1 {
  margin: 0;
  color: #022f9d;
}

.view-header p {
  margin: 0.5rem 0 0;
  color: #64748b;
}

.state-message {
  color: #64748b;
  padding: 1rem 0;
}

.state-message.error {
  color: #b91c1c;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  border-bottom: 1px solid #e2e8f0;
  padding: 0.75rem;
  text-align: left;
  vertical-align: top;
}

.data-table thead th {
  color: #ffffff;
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.data-table thead {
  background: #022f9d;
}

.text-right {
  text-align: right;
}

.badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 700;
}

.badge.compra {
  background: #fff7ed;
  color: #c2410c;
}

.badge.venta {
  background: #ecfeff;
  color: #0e7490;
}

@media (max-width: 900px) {
  .data-table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }
}
</style>
