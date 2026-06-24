<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <h2>Detalle del Cobro</h2>

      <div v-if="loading" class="loading">Cargando...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="cobro" class="detalles">
        <div class="detail-row"><span class="label">ID:</span><span>{{ cobro.id }}</span></div>
        <div class="detail-row"><span class="label">Socio:</span><span>{{ cobro.socio_nombre }}</span></div>
        <div class="detail-row"><span class="label">Período:</span><span>{{ periodo(cobro.mes, cobro.anio) }}</span></div>
        <div class="detail-row"><span class="label">Monto cuota:</span><span>${{ monto(cobro.monto_cuota) }}</span></div>
        <div class="detail-row"><span class="label">Monto pagado:</span><span>${{ monto(cobro.monto_pagado) }}</span></div>
        <div class="detail-row"><span class="label">Saldo:</span><span>${{ monto(cobro.saldo_mes) }}</span></div>
        <div class="detail-row"><span class="label">Estado:</span><span>{{ cobro.estado }}</span></div>
        <div class="detail-row">
          <span class="label">Fecha de registro de pago:</span>
          <span>{{ fecha(cobro.fecha_registro_pago) }}</span>
        </div>
        <div class="detail-row"><span class="label">Método:</span><span>{{ cobro.metodo_pago || '-' }}</span></div>
        <div class="detail-row"><span class="label">Observaciones:</span><span>{{ cobro.observaciones || '-' }}</span></div>
      </div>

      <div class="panel-actions">
        <button @click="$emit('close')" class="btn-close">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useCobrosStore } from '@/stores/cobros'

const props = defineProps<{ cobroId: number }>()
defineEmits(['close'])

const cobrosStore = useCobrosStore()
const { cobro, loading, error } = storeToRefs(cobrosStore)

onMounted(() => {
  cobrosStore.fetchCobro(props.cobroId)
})

function monto(valor: number | string): string {
  return new Intl.NumberFormat('es-AR', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(valor || 0))
}

function fecha(valor: string | null): string {
  if (!valor) return '-'
  return new Date(`${valor}T00:00:00`).toLocaleDateString('es-AR')
}

function periodo(mes: number, anio: number): string {
  const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  return `${meses[mes - 1]} ${anio}`
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
  padding: 30px;
  border-radius: 8px;
  max-width: 640px;
  width: 100%;
  border: 1px solid #e5e7eb;
  box-shadow: 0 6px 18px rgba(2, 47, 157, 0.08);
}

h2 {
  color: #022f9d;
  margin-bottom: 20px;
}

.detalles {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}

.detail-row {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 10px;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.4rem;
}

.label {
  font-weight: 700;
  color: #022f9d;
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
