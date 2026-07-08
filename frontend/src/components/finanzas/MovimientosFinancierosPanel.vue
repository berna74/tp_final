<template>
  <section class="finanzas-panel">
    <header class="hero">
      <div>
        <h1>{{ titulo }}</h1>
        <p v-if="descripcion" class="hero-copy">{{ descripcion }}</p>
      </div>
      <div class="hero-actions">
        <button
          v-if="authStore.puedeEscribir"
          type="button"
          class="btn-primary btn-new"
          @click="abrirAlta()"
        >
          {{ editandoId ? 'Editar movimiento' : '+ Nuevo movimiento' }}
        </button>
      </div>
    </header>

    <section v-if="mostrarFormulario" class="form-panel">
      <div class="panel-header">
        <h2>{{ editandoId ? 'Editar movimiento' : `Nuevo ${titulo.toLowerCase().slice(0, -1)}` }}</h2>
        <button type="button" class="btn-close" @click="cerrarFormulario">&times;</button>
      </div>
      <form class="form-grid" @submit.prevent="guardarMovimiento">
        <div class="form-group">
          <label for="fecha">Fecha *</label>
          <input id="fecha" v-model="form.fecha" type="date" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="grupo">Grupo *</label>
          <select id="grupo" v-model="form.grupo" class="form-control" required>
            <option value="">Seleccione...</option>
            <option v-for="item in grupos" :key="item.grupo" :value="item.grupo">{{ item.grupo }}</option>
          </select>
        </div>

        <div class="form-group">
          <label for="rubro">Rubro *</label>
          <select id="rubro" v-model="form.rubro" class="form-control" required>
            <option value="">Seleccione...</option>
            <option v-for="rubro in rubrosDisponibles" :key="rubro" :value="rubro">{{ rubro }}</option>
          </select>
        </div>

        <div v-if="form.rubro === 'Otro'" class="form-group full-width">
          <label for="rubroPersonalizado">Rubro personalizado *</label>
          <input
            id="rubroPersonalizado"
            v-model="rubroPersonalizado"
            type="text"
            class="form-control"
            placeholder="Escriba el rubro"
            required
          />
        </div>

        <div class="form-group full-width">
          <label for="concepto">Concepto *</label>
          <input
            id="concepto"
            v-model="form.concepto"
            type="text"
            class="form-control"
            placeholder="Ej.: Cobro abono marzo, pago de gas, compra de remeras"
            required
          />
        </div>

        <div class="form-group">
          <label for="monto">Monto *</label>
          <input id="monto" v-model.number="form.monto" type="number" min="0" step="0.01" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="metodo">Metodo</label>
          <input id="metodo" v-model="form.metodo" type="text" class="form-control" placeholder="Efectivo, transferencia, cuenta, tarjeta" />
        </div>

        <div class="form-group full-width">
          <label for="observaciones">Observaciones</label>
          <textarea id="observaciones" v-model="form.observaciones" class="form-control" rows="3"></textarea>
        </div>

        <div class="form-actions full-width">
          <button type="button" class="btn-secondary" @click="cerrarFormulario">Cancelar</button>
          <button type="submit" class="btn-primary" :disabled="finanzasStore.loading">
            {{ finanzasStore.loading ? 'Guardando...' : 'Guardar' }}
          </button>
        </div>
      </form>
    </section>

    <section class="filters-panel">
      <div class="filters-grid">
        <div class="form-group">
          <label for="buscar">Buscar</label>
          <input id="buscar" v-model="filtroTexto" type="text" class="form-control" placeholder="Rubro, concepto u observaciones" @keyup.enter="aplicarFiltros" />
        </div>
        <div class="form-group">
          <label for="grupoFiltro">Grupo</label>
          <select id="grupoFiltro" v-model="filtroGrupo" class="form-control">
            <option value="">Todos</option>
            <option v-for="item in grupos" :key="item.grupo" :value="item.grupo">{{ item.grupo }}</option>
          </select>
        </div>
        <div class="filter-actions">
          <button type="button" class="btn-secondary" @click="limpiarFiltros">Limpiar</button>
          <button type="button" class="btn-primary" @click="aplicarFiltros">Aplicar</button>
        </div>
      </div>
    </section>

    <section class="table-panel">
      <div v-if="finanzasStore.loading" class="state-message">Cargando...</div>
      <div v-else-if="finanzasStore.error" class="state-message error">{{ finanzasStore.error }}</div>
      <div v-else-if="finanzasStore.movimientos.length === 0" class="state-message">No hay movimientos registrados.</div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Grupo</th>
            <th>Rubro</th>
            <th>Concepto</th>
            <th>Monto</th>
            <th>Metodo</th>
            <th>Observaciones</th>
            <th v-if="authStore.puedeEscribir">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="movimiento in finanzasStore.movimientos" :key="movimiento.id">
            <td>{{ formatearFecha(movimiento.fecha) }}</td>
            <td>{{ movimiento.grupo }}</td>
            <td>{{ movimiento.rubro }}</td>
            <td>{{ movimiento.concepto }}</td>
            <td class="text-right">{{ formatearMoneda(Number(movimiento.monto)) }}</td>
            <td>{{ movimiento.metodo || '-' }}</td>
            <td>{{ movimiento.observaciones || '-' }}</td>
            <td v-if="authStore.puedeEscribir" class="actions-cell">
              <button type="button" class="btn-icon" @click="abrirEdicion(movimiento)">Editar</button>
              <button type="button" class="btn-icon btn-delete" @click="eliminarMovimiento(movimiento.id!)">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <div v-if="finanzasStore.movimientos.length > 0" class="pagination-controls">
      <button type="button" class="btn-secondary" :disabled="finanzasStore.currentPage <= 1" @click="cambiarPagina(finanzasStore.currentPage - 1)">
        Anterior
      </button>
      <span>Pagina {{ finanzasStore.currentPage }} de {{ finanzasStore.totalPages }}</span>
      <button type="button" class="btn-secondary" :disabled="finanzasStore.currentPage >= finanzasStore.totalPages" @click="cambiarPagina(finanzasStore.currentPage + 1)">
        Siguiente
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useFinanzasStore } from '@/stores/finanzas'
import type { MovimientoFinanciero, TipoMovimientoFinanciero } from '@/interfaces/MovimientoFinanciero'
import { configuracionRubros, formatearFecha, formatearMoneda, obtenerRubrosDeGrupo } from '@/data/finanzasPlantilla'

const props = defineProps<{
  tipo: TipoMovimientoFinanciero
  titulo: string
  descripcion?: string
}>()

const authStore = useAuthStore()
const finanzasStore = useFinanzasStore()

const mostrarFormulario = ref(false)
const editandoId = ref<number | null>(null)
const rubroPersonalizado = ref('')
const filtroTexto = ref('')
const filtroGrupo = ref('')

const grupos = computed(() => configuracionRubros[props.tipo])

const form = ref<MovimientoFinanciero>({
  tipo: props.tipo,
  fecha: new Date().toISOString().split('T')[0],
  grupo: '',
  rubro: '',
  concepto: '',
  monto: 0,
  metodo: '',
  observaciones: '',
})

const rubrosDisponibles = computed(() => {
  if (!form.value.grupo) return []
  return obtenerRubrosDeGrupo(props.tipo, form.value.grupo)
})

watch(() => form.value.grupo, () => {
  form.value.rubro = ''
  rubroPersonalizado.value = ''
})

const recargar = async (page: number = finanzasStore.currentPage) => {
  await finanzasStore.fetchMovimientos(props.tipo, page, filtroTexto.value, filtroGrupo.value)
}

const resetFormulario = () => {
  form.value = {
    tipo: props.tipo,
    fecha: new Date().toISOString().split('T')[0],
    grupo: '',
    rubro: '',
    concepto: '',
    monto: 0,
    metodo: '',
    observaciones: '',
  }
  rubroPersonalizado.value = ''
  editandoId.value = null
}

const abrirAlta = () => {
  resetFormulario()
  mostrarFormulario.value = true
}

const abrirEdicion = (movimiento: MovimientoFinanciero) => {
  form.value = {
    id: movimiento.id,
    tipo: props.tipo,
    fecha: movimiento.fecha,
    grupo: movimiento.grupo,
    rubro: movimiento.rubro,
    concepto: movimiento.concepto,
    monto: Number(movimiento.monto),
    metodo: movimiento.metodo || '',
    observaciones: movimiento.observaciones || '',
  }
  const rubros = obtenerRubrosDeGrupo(props.tipo, movimiento.grupo)
  if (!rubros.includes(movimiento.rubro)) {
    form.value.rubro = 'Otro'
    rubroPersonalizado.value = movimiento.rubro
  }
  editandoId.value = movimiento.id || null
  mostrarFormulario.value = true
}

const cerrarFormulario = () => {
  mostrarFormulario.value = false
  resetFormulario()
}

const guardarMovimiento = async () => {
  const payload: MovimientoFinanciero = {
    ...form.value,
    tipo: props.tipo,
    rubro: form.value.rubro === 'Otro' ? rubroPersonalizado.value.trim() : form.value.rubro,
  }

  if (!payload.rubro) {
    alert('Debe completar el rubro.')
    return
  }

  try {
    if (editandoId.value) {
      await finanzasStore.updateMovimiento(editandoId.value, payload)
    } else {
      await finanzasStore.createMovimiento(payload)
    }
    cerrarFormulario()
    await recargar(editandoId.value ? finanzasStore.currentPage : 1)
  } catch (error) {
    console.error('Error al guardar movimiento:', error)
    alert('No se pudo guardar el movimiento.')
  }
}

const eliminarMovimiento = async (id: number) => {
  if (!confirm('¿Eliminar este movimiento?')) return
  try {
    await finanzasStore.deleteMovimiento(id)
    await recargar()
  } catch (error) {
    console.error('Error al eliminar movimiento:', error)
    alert('No se pudo eliminar el movimiento.')
  }
}

const aplicarFiltros = async () => {
  await recargar(1)
}

const limpiarFiltros = async () => {
  filtroTexto.value = ''
  filtroGrupo.value = ''
  await recargar(1)
}

const cambiarPagina = async (page: number) => {
  await recargar(page)
}

onMounted(async () => {
  await recargar(1)
})
</script>

<style scoped>
.finanzas-panel {
  padding: 20px;
  display: grid;
  gap: 1rem;
}

.hero {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 14px;
  background: #fff;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
}

.eyebrow {
  margin: 0 0 0.35rem;
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  opacity: 0.8;
}

.hero h1,
.panel-header h2 {
  margin: 0;
}

.hero h1 {
  color: #022f9d;
}

.hero-copy {
  margin: 0.75rem 0 0;
  max-width: 760px;
  line-height: 1.5;
  color: #64748b;
}

.hero-actions {
  display: flex;
  align-items: flex-start;
}

.form-panel,
.filters-panel,
.table-panel {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
}

.filters-panel,
.table-panel {
  padding: 1rem;
}

.form-panel {
  border: 1px solid #e2e8f0;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1rem 0;
}

.btn-close {
  border: none;
  background: transparent;
  font-size: 1.8rem;
  cursor: pointer;
  color: #64748b;
}

.form-grid,
.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.filters-grid {
  grid-template-columns: minmax(180px, 320px) minmax(220px, 280px) auto;
  align-items: end;
}

.full-width {
  grid-column: 1 / -1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-control {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 0.75rem 0.85rem;
  font-size: 0.95rem;
}

.form-actions,
.filter-actions,
.pagination-controls,
.actions-cell {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.filter-actions {
  justify-content: flex-end;
  align-self: end;
  white-space: nowrap;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 0.9rem 0.75rem;
  border-bottom: 1px solid #e2e8f0;
  text-align: left;
  vertical-align: top;
}

.data-table th {
  background: #f8fafc;
}

.text-right {
  text-align: right !important;
}

.state-message {
  padding: 1rem 0;
}

.error {
  color: #b91c1c;
}

.btn-primary,
.btn-secondary,
.btn-icon {
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary {
  background: #022f9d;
  color: #fff;
}

.btn-new {
  background: #00cdff;
  color: #fff;
  font-weight: 400;
}

.btn-secondary {
  background: #e2e8f0;
  color: #0f172a;
}

.btn-icon {
  padding: 0.5rem 0.75rem;
  background: #e0f2fe;
  color: #075985;
}

.btn-delete {
  background: #fee2e2;
  color: #b91c1c;
}

.pagination-controls {
  justify-content: center;
}

@media (max-width: 768px) {
  .hero {
    flex-direction: column;
  }

  .filters-grid {
    grid-template-columns: 1fr;
  }

  .filter-actions {
    justify-content: flex-start;
  }

  .filter-actions,
  .actions-cell,
  .pagination-controls {
    flex-wrap: wrap;
  }
}
</style>