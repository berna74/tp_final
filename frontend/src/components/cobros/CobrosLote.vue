<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <h2>Registrar cobro/s</h2>

      <form @submit.prevent="procesarLote">
        <div class="form-row">
          <div class="form-group">
            <label>Mes:*</label>
            <select v-model.number="mes" required>
              <option v-for="n in 12" :key="n" :value="n">{{ nombreMes(n) }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Año:*</label>
            <input type="number" v-model.number="anio" min="2020" max="2035" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Monto cuota:*</label>
            <input type="number" step="0.01" min="0" v-model.number="montoCuota" required />
          </div>
          <div class="form-group">
            <label>Monto pagado:</label>
            <input type="number" step="0.01" min="0" v-model.number="montoPagado" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Fecha de registro de pago:</label>
            <input type="date" v-model="fechaRegistroPago" />
          </div>
          <div class="form-group">
            <label>Método de pago:</label>
            <select v-model="metodoPago">
              <option value="">Seleccionar</option>
              <option value="Efectivo">Efectivo</option>
              <option value="Transferencia">Transferencia</option>
              <option value="Débito">Débito</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>Observaciones:</label>
          <textarea v-model="observaciones" rows="2"></textarea>
        </div>

        <div class="selector-header">
          <h3>Socios a incluir</h3>
          <div class="selector-tools">
            <input
              v-model="busqueda"
              type="text"
              placeholder="Buscar por nombre, apellido o DNI"
              class="search-input"
            />
            <button type="button" class="btn-link" @click="seleccionarTodosFiltrados">Seleccionar filtrados</button>
            <button type="button" class="btn-link" @click="limpiarSeleccion">Limpiar selección</button>
          </div>
        </div>

        <div class="socios-box">
          <label v-for="socio in sociosFiltrados" :key="socio.id" class="socio-item">
            <input type="checkbox" :value="socio.id" v-model="sociosSeleccionados" />
            <span>{{ socio.nombre }} {{ socio.apellido }} ({{ socio.dni }})</span>
          </label>
        </div>

        <div class="resumen-seleccion">
          Seleccionados: {{ sociosSeleccionados.length }}
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-submit" :disabled="submitLoading">{{ submitLoading ? 'Procesando...' : 'Procesar lote' }}</button>
          <button type="button" class="btn-cancel" @click="$emit('close')">Cerrar</button>
        </div>
      </form>

      <div v-if="error" class="error">{{ error }}</div>

      <div v-if="resultado" class="resultado-box">
        <h3>Resultado del lote</h3>
        <p>
          Creados: {{ resultado.resumen.creados }} |
          Actualizados: {{ resultado.resumen.actualizados }} |
          Omitidos: {{ resultado.resumen.omitidos }} |
          Errores: {{ resultado.resumen.errores }}
        </p>
        <p v-if="resultado.resumen.usuarios_socio">
          Usuarios socio marcados: {{ resultado.resumen.usuarios_socio.marcados }} |
          Ya eran socio: {{ resultado.resumen.usuarios_socio.ya_eransocio }} |
          Sin usuario: {{ resultado.resumen.usuarios_socio.sin_usuario }}
        </p>

        <table class="resultado-table">
          <thead>
            <tr>
              <th>Acción</th>
              <th>Socio</th>
              <th>Detalle</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filasResultado" :key="item.key">
              <td>{{ item.accion }}</td>
              <td>{{ item.socio }}</td>
              <td>{{ item.detalle }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useSociosStore } from '@/stores/socios'
import { useCobrosStore } from '@/stores/cobros'

interface ResultadoLote {
  resumen: {
    creados: number
    actualizados: number
    omitidos: number
    errores: number
    usuarios_socio?: {
      marcados: number
      ya_eransocio: number
      sin_usuario: number
      detalle_sin_usuario: Array<{ socio_id: number; socio_nombre: string }>
    }
  }
  detalle: {
    creados: Array<{ socio_id: number; socio_nombre: string; cobro_id: number }>
    actualizados: Array<{ socio_id: number; socio_nombre: string; cobro_id: number }>
    omitidos: Array<{ socio_id: number; socio_nombre: string; mensaje: string }>
    errores: Array<{ socio_id: number; mensaje: string }>
  }
}

defineEmits(['close'])

const sociosStore = useSociosStore()
const cobrosStore = useCobrosStore()
const { socios } = storeToRefs(sociosStore)

const hoy = new Date()
const anio = ref(hoy.getFullYear())
const mes = ref(hoy.getMonth() + 1)
const montoCuota = ref(0)
const montoPagado = ref(0)
const fechaRegistroPago = ref(hoy.toISOString().split('T')[0])
const metodoPago = ref('')
const observaciones = ref('')
const busqueda = ref('')
const sociosSeleccionados = ref<number[]>([])

const submitLoading = ref(false)
const error = ref<string | null>(null)
const resultado = ref<ResultadoLote | null>(null)

onMounted(async () => {
  await sociosStore.fetchSocios()
})

const sociosFiltrados = computed(() => {
  const q = busqueda.value.trim().toLowerCase()
  if (!q) return socios.value

  return socios.value.filter((s) => {
    const nombre = `${s.nombre} ${s.apellido}`.toLowerCase()
    const dni = (s.dni || '').toLowerCase()
    return nombre.includes(q) || dni.includes(q)
  })
})

const filasResultado = computed(() => {
  if (!resultado.value) return []

  const filas: Array<{ key: string; accion: string; socio: string; detalle: string }> = []
  resultado.value.detalle.creados.forEach((item) => {
    filas.push({ key: `c-${item.socio_id}`, accion: 'Creado', socio: item.socio_nombre, detalle: `Cobro #${item.cobro_id}` })
  })
  resultado.value.detalle.actualizados.forEach((item) => {
    filas.push({ key: `a-${item.socio_id}`, accion: 'Actualizado', socio: item.socio_nombre, detalle: `Cobro #${item.cobro_id}` })
  })
  resultado.value.detalle.omitidos.forEach((item) => {
    filas.push({ key: `o-${item.socio_id}`, accion: 'Omitido', socio: item.socio_nombre, detalle: item.mensaje })
  })
  resultado.value.detalle.errores.forEach((item, idx) => {
    filas.push({ key: `e-${item.socio_id}-${idx}`, accion: 'Error', socio: `Socio ${item.socio_id}`, detalle: item.mensaje })
  })

  return filas
})

function nombreMes(n: number): string {
  const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  return meses[n - 1]
}

function seleccionarTodosFiltrados() {
  sociosSeleccionados.value = Array.from(new Set([...sociosSeleccionados.value, ...sociosFiltrados.value.map((s) => s.id)]))
}

function limpiarSeleccion() {
  sociosSeleccionados.value = []
}

async function procesarLote() {
  error.value = null
  resultado.value = null

  if (!sociosSeleccionados.value.length) {
    error.value = 'Seleccione al menos un socio'
    return
  }

  submitLoading.value = true
  try {
    const response = await cobrosStore.createCobrosLote({
      socios_ids: sociosSeleccionados.value,
      anio: anio.value,
      mes: mes.value,
      monto_cuota: Number(montoCuota.value || 0),
      monto_pagado: Number(montoPagado.value || 0),
      fecha_registro_pago: fechaRegistroPago.value || null,
      metodo_pago: metodoPago.value,
      observaciones: observaciones.value,
    })
    resultado.value = response as ResultadoLote
  } catch (e: any) {
    error.value = e.response?.data?.mensaje || 'Error al procesar lote de cobros'
  } finally {
    submitLoading.value = false
  }
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

h2 {
  color: #022f9d;
  margin-bottom: 16px;
}

h3 {
  color: #022f9d;
  margin: 0;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.form-group {
  margin-bottom: 12px;
}

label {
  display: block;
  margin-bottom: 4px;
  font-weight: 700;
  color: #022f9d;
}

input,
select,
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

input[type='checkbox'] {
  width: auto;
  margin: 0;
}

.inline-checks {
  margin-top: 4px;
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.inline-check {
  display: inline-flex;
  gap: 0.5rem;
  align-items: center;
  font-weight: 500;
  color: #1f2937;
}

.selector-header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 0.8rem;
  margin-top: 12px;
}

.selector-tools {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.search-input {
  min-width: 260px;
}

.btn-link {
  border: 1px solid #d0d7de;
  background: #fff;
  color: #022f9d;
  border-radius: 4px;
  padding: 0.35rem 0.55rem;
  font-weight: 600;
  line-height: 1.2;
  cursor: pointer;
}

.btn-link:hover {
  background: #022f9d;
  color: #fff;
  border-color: #022f9d;
}

.btn-link:focus-visible {
  outline: 2px solid #00cdff;
  outline-offset: 1px;
}

.socios-box {
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 10px;
  max-height: 220px;
  overflow: auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.socio-item {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  font-weight: 500;
}

.resumen-seleccion {
  margin-top: 10px;
  font-weight: 700;
}

.form-actions {
  margin-top: 14px;
  display: flex;
  gap: 10px;
}

.btn-submit,
.btn-cancel {
  border: none;
  border-radius: 6px;
  padding: 0.65rem 1rem;
  cursor: pointer;
}

.btn-submit {
  background: #022f9d;
  color: #fff;
}

.btn-cancel {
  background: #d9d9d9;
}

.error {
  margin-top: 10px;
  color: #b00020;
}

.resultado-box {
  margin-top: 18px;
  border-top: 1px solid #e5e7eb;
  padding-top: 12px;
}

.resultado-table {
  width: 100%;
  border-collapse: collapse;
}

.resultado-table th,
.resultado-table td {
  border: 1px solid #e5e7eb;
  padding: 6px;
  text-align: left;
}

@media (max-width: 900px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .selector-header {
    flex-direction: column;
    align-items: stretch;
  }

  .selector-tools {
    flex-wrap: wrap;
  }

  .search-input {
    min-width: 100%;
  }

  .socios-box {
    grid-template-columns: 1fr;
  }
}
</style>
