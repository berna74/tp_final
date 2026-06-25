<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <h2>Editar Cobro</h2>
      <form @submit.prevent="actualizarCobro">
        <div class="form-group">
          <label>Socio:*</label>
          <select v-model.number="formData.socio" required>
            <option value="">Seleccionar socio</option>
            <option v-for="s in socios" :key="s.id" :value="s.id">
              {{ s.apellido }}, {{ s.nombre }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Tipo de cobro:*</label>
          <select v-model="formData.tipo_cobro" required>
            <option value="mensual">Mensual</option>
            <option value="dia_cancha">Día de cancha</option>
          </select>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Mes:*</label>
            <select v-model.number="formData.mes" required>
              <option v-for="n in 12" :key="n" :value="n">{{ nombreMes(n) }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Año:*</label>
            <input type="number" v-model.number="formData.anio" min="2020" max="2035" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>{{ esDiaCancha ? 'Monto acumulado actual' : 'Monto cuota:*' }}</label>
            <input
              type="number"
              step="0.01"
              min="0"
              v-model.number="formData.monto_cuota"
              :required="!esDiaCancha"
              :disabled="esDiaCancha"
            />
          </div>
          <div class="form-group">
            <label>{{ esDiaCancha ? 'Monto a sumar por día:*' : 'Monto pagado:*' }}</label>
            <input type="number" step="0.01" min="0" v-model.number="formData.monto_pagado" required />
          </div>
        </div>

        <div class="form-group">
          <label>Fecha de registro de pago:</label>
          <input type="date" v-model="formData.fecha_registro_pago" />
        </div>

        <div class="form-group">
          <label>Método de pago:</label>
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
            {{ submitLoading ? 'Actualizando...' : 'Actualizar Cobro' }}
          </button>
          <button type="button" class="btn-cancel" @click="$emit('close')">Cancelar</button>
        </div>

        <div v-if="error" class="error">{{ error }}</div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useCobrosStore } from '@/stores/cobros'
import { useSociosStore } from '@/stores/socios'

const props = defineProps<{ cobroId: number }>()
const emit = defineEmits(['close', 'updated'])
const cobrosStore = useCobrosStore()
const sociosStore = useSociosStore()
const { socios } = storeToRefs(sociosStore)

const formData = ref({
  socio: null as number | null,
  anio: new Date().getFullYear(),
  mes: 1,
  tipo_cobro: 'mensual' as 'mensual' | 'dia_cancha',
  monto_cuota: 0,
  monto_pagado: 0,
  fecha_registro_pago: '',
  metodo_pago: '',
  observaciones: '',
})

const esDiaCancha = computed(() => formData.value.tipo_cobro === 'dia_cancha')

const submitLoading = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  await sociosStore.fetchSocios()
  await cobrosStore.fetchCobro(props.cobroId)

  const data = cobrosStore.cobro
  if (data) {
    formData.value = {
      socio: data.socio,
      anio: data.anio,
      mes: data.mes,
      tipo_cobro: (data.tipo_cobro || 'mensual') as 'mensual' | 'dia_cancha',
      monto_cuota: Number(data.monto_cuota),
      monto_pagado: (data.tipo_cobro || 'mensual') === 'dia_cancha' ? 0 : Number(data.monto_pagado),
      fecha_registro_pago: data.fecha_registro_pago ? data.fecha_registro_pago.split('T')[0] : '',
      metodo_pago: data.metodo_pago || '',
      observaciones: data.observaciones || '',
    }
  }
})

function nombreMes(mes: number): string {
  const meses = [
    'Enero',
    'Febrero',
    'Marzo',
    'Abril',
    'Mayo',
    'Junio',
    'Julio',
    'Agosto',
    'Septiembre',
    'Octubre',
    'Noviembre',
    'Diciembre',
  ]
  return meses[mes - 1]
}

async function actualizarCobro() {
  submitLoading.value = true
  error.value = null

  try {
    if (formData.value.socio === null) {
      error.value = 'Debe seleccionar un socio'
      return
    }

    const payload = {
      ...formData.value,
      socio: formData.value.socio,
      monto_cuota: esDiaCancha.value ? Number(formData.value.monto_pagado || 0) : Number(formData.value.monto_cuota || 0),
      monto_pagado: Number(formData.value.monto_pagado || 0),
    }

    await cobrosStore.updateCobro(props.cobroId, payload)
    emit('updated')
  } catch (e: any) {
    error.value = e.response?.data?.mensaje || 'Error al actualizar cobro'
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
  color: #022f9d;
  font-weight: 700;
}

input,
select,
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.btn-submit,
.btn-cancel {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-submit {
  background-color: #022f9d;
  color: white;
}

.btn-cancel {
  background-color: #ccc;
}

.error {
  color: #b00020;
  margin-top: 10px;
}
</style>
