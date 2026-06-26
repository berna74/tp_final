<template>
  <div class="form-panel">
    <div class="form-content">
      <h2>Registrar Pago</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Tipo de Pago:*</label>
          <select v-model="formData.tipo" required>
            <option value="Abono Mensual">Abono Mensual</option>
          </select>
        </div>

        <div class="form-group">
          <label>Pagado por (Socio):*</label>
          <select v-model.number="formData.socio_id" required>
            <option value="">Seleccionar socio</option>
            <option v-for="socio in socios" :key="socio.id" :value="socio.id">
              {{ socio.apellido }}, {{ socio.nombre }}
            </option>
          </select>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Monto:*</label>
            <input type="number" v-model.number="formData.monto" step="0.01" min="0" required />
          </div>
          <div class="form-group">
            <label>Fecha de Pago:*</label>
            <input type="date" v-model="formData.fecha_pago" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Mes:*</label>
            <select v-model.number="formData.mes" required>
              <option value="">Mes</option>
              <option v-for="n in 12" :key="n" :value="n">{{ getMesNombre(n) }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Año:*</label>
            <input type="number" v-model.number="formData.anio" min="2020" max="2030" required />
          </div>
        </div>

        <div class="form-group">
          <label>Método de Pago:</label>
          <select v-model="formData.metodo_pago">
            <option value="">Seleccionar</option>
            <option value="Efectivo">Efectivo</option>
            <option value="Transferencia">Transferencia</option>
            <option value="Débito">Débito</option>
          </select>
        </div>

        <div class="form-group">
          <label>Observaciones:</label>
          <textarea v-model="formData.observaciones" rows="3"></textarea>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-submit" :disabled="submitLoading">
            {{ submitLoading ? 'Guardando...' : 'Registrar Pago' }}
          </button>
          <button type="button" class="btn-cancel" @click="$emit('close')">Cancelar</button>
        </div>
        
        <div v-if="error" class="error">{{ error }}</div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { usePagosStore } from '@/stores/pagos'
import { useSociosStore } from '@/stores/socios'
import { storeToRefs } from 'pinia'

const emit = defineEmits(['close', 'created'])
const pagosStore = usePagosStore()
const sociosStore = useSociosStore()

const { socios } = storeToRefs(sociosStore)

const currentDate = new Date()
const formData = ref({
  tipo: 'Abono Mensual',
  monto: 0,
  fecha_pago: currentDate.toISOString().split('T')[0],
  mes: currentDate.getMonth() + 1,
  anio: currentDate.getFullYear(),
  socio_id: null as number | null,
  alumno_id: null as number | null,
  profesor_id: null as number | null,
  metodo_pago: '',
  observaciones: ''
})

const submitLoading = ref(false)
const error = ref<string | null>(null)

onMounted(() => {
  sociosStore.fetchSocios()
})

function getMesNombre(mes: number): string {
  const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  return meses[mes - 1]
}

async function handleSubmit() {
  submitLoading.value = true
  error.value = null
  
  try {
    const pagoData = {
      ...formData.value,
      alumno_id: null,
      profesor_id: null,
    }

    await pagosStore.createPago(pagoData)
    emit('created')
  } catch (e: any) {
    error.value = e.response?.data?.mensaje || 'Error al registrar pago'
  } finally {
    submitLoading.value = false
  }
}
</script>

<style scoped>
.form-panel {
  width: 100%;
  display: flex;
  justify-content: center;
  margin: 1rem 0;
}

.form-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 600px;
  width: 100%;
  border: 1px solid #e5e7eb;
  box-shadow: 0 6px 18px rgba(2, 47, 157, 0.08);
}

h2 {
  color: #022F9D;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #022F9D;
  font-weight: bold;
}

input, select, textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #CCCCCC;
  border-radius: 4px;
  font-size: 14px;
}

textarea {
  resize: vertical;
  font-family: inherit;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-submit, .btn-cancel {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-submit {
  background-color: #022F9D;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background-color: #00CDFF;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background-color: #CCCCCC;
  color: #000000;
}

.btn-cancel:hover {
  background-color: #999999;
}

.error {
  color: #dc3545;
  margin-top: 10px;
  padding: 10px;
  background-color: #f8d7da;
  border-radius: 4px;
}
</style>
