<template>
  <div class="panel-wrapper">
    <div class="panel-content">
      <div class="header-row">
        <h2>Pagos últimos 12 meses</h2>
        <div class="header-actions">
          <button class="btn-export" @click="exportarPdf" :disabled="exportandoPdf || loading">
            {{ exportandoPdf ? 'Exportando...' : 'Exportar PDF' }}
          </button>
          <button class="btn-close" @click="$emit('close')">Cerrar</button>
        </div>
      </div>

      <div v-if="loading" class="loading">Cargando matriz...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="!matriz || matriz.socios.length === 0" class="empty">No hay datos de cobros para mostrar</div>

      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th class="col-socio">Socio</th>
              <th v-for="col in matriz.columnas" :key="col.key">{{ etiquetaMes(col.mes) }} {{ col.anio }}</th>
              <th class="col-total">Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="fila in matriz.socios" :key="fila.socio_id">
              <td class="col-socio">{{ fila.socio_nombre }}</td>
              <td
                v-for="col in matriz.columnas"
                :key="`${fila.socio_id}-${col.key}`"
                :class="['monto-cell', { 'monto-cell-rojo': fila.en_rojo?.[col.key] }]"
              >
                {{ formatoMonto(fila.montos[col.key] || 0) }}
              </td>
              <td class="col-total">{{ formatoMonto(fila.total_registrado || 0) }}</td>
            </tr>
          </tbody>
        </table>

        <div class="pagination-controls" v-if="matriz.total_pages > 1">
          <button class="btn-page" :disabled="matriz.page <= 1" @click="irAPagina(matriz.page - 1)">Anterior</button>
          <span class="page-info">Página {{ matriz.page }} de {{ matriz.total_pages }}</span>
          <button class="btn-page" :disabled="matriz.page >= matriz.total_pages" @click="irAPagina(matriz.page + 1)">Siguiente</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useCobrosStore } from '@/stores/cobros'
import ApiService from '@/services/ApiService'
import { jsPDF } from 'jspdf'
import autoTable from 'jspdf-autotable'

defineEmits(['close'])

const cobrosStore = useCobrosStore()
const { matrizDosAnios: matriz, loading, error } = storeToRefs(cobrosStore)
const exportandoPdf = ref(false)

onMounted(() => {
  cobrosStore.fetchMatrizDosAnios(1)
})

const meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

function etiquetaMes(mes: number): string {
  return meses[mes - 1] || String(mes)
}

function formatoMonto(valor: number): string {
  return new Intl.NumberFormat('es-AR', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(Number(valor || 0))
}

function irAPagina(page: number) {
  cobrosStore.fetchMatrizDosAnios(page)
}

async function exportarPdf() {
  if (exportandoPdf.value) return
  exportandoPdf.value = true

  try {
    const response = await ApiService.get('/cobros/matriz-dos-anios/?page=1&page_size=5000')
    const data = response.data

    const doc = new jsPDF({ orientation: 'landscape', unit: 'pt', format: 'a3' })
    const columnas = data.columnas || []
    const socios = data.socios || []

    const head = [
      ['Socio', ...columnas.map((c: any) => `${etiquetaMes(c.mes)} ${c.anio}`), 'Total'],
    ]

    const body = socios.map((fila: any) => {
      const montos = columnas.map((c: any) => formatoMonto(fila.montos?.[c.key] || 0))
      return [fila.socio_nombre, ...montos, formatoMonto(fila.total_registrado || 0)]
    })

    const bodyStylesPorCelda: Record<
      string,
      { fillColor?: [number, number, number]; textColor?: [number, number, number]; fontStyle?: 'bold' }
    > = {}
    socios.forEach((fila: any, rowIndex: number) => {
      columnas.forEach((c: any, colIndex: number) => {
        if (fila.en_rojo?.[c.key]) {
          bodyStylesPorCelda[`${rowIndex}-${colIndex + 1}`] = {
            fillColor: [254, 205, 211],
            textColor: [127, 29, 29],
            fontStyle: 'bold',
          }
        }
      })
    })

    doc.setFontSize(14)
    doc.text('Pagos últimos 12 meses', 40, 30)
    doc.setFontSize(10)
    doc.text(`Registros: ${socios.length}`, 40, 48)

    autoTable(doc, {
      head,
      body,
      startY: 60,
      styles: { fontSize: 7, cellPadding: 2 },
      headStyles: { fillColor: [2, 47, 157] },
      columnStyles: {
        0: { cellWidth: 170 },
      },
      margin: { left: 20, right: 20 },
      horizontalPageBreak: true,
      didParseCell: (hookData) => {
        if (hookData.section !== 'body') return

        const rowIndex = hookData.row.index
        const colIndex = hookData.column.index
        const estilo = bodyStylesPorCelda[`${rowIndex}-${colIndex}`]
        if (!estilo) return

        if (estilo.fillColor) hookData.cell.styles.fillColor = estilo.fillColor
        if (estilo.textColor) hookData.cell.styles.textColor = estilo.textColor
        if (estilo.fontStyle) hookData.cell.styles.fontStyle = estilo.fontStyle
      },
    })

    const fecha = new Date().toISOString().slice(0, 10)
    doc.save(`pagos-ultimos-12-meses-${fecha}.pdf`)
  } catch (e) {
    console.error('Error al exportar PDF:', e)
  } finally {
    exportandoPdf.value = false
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
  padding: 20px;
  border-radius: 8px;
  width: 100%;
  border: 1px solid #e5e7eb;
  box-shadow: 0 6px 18px rgba(2, 47, 157, 0.08);
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.header-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

h2 {
  color: #022f9d;
  margin: 0;
}

.btn-close {
  border: none;
  padding: 0.5rem 0.9rem;
  border-radius: 6px;
  background: #022f9d;
  color: #fff;
  cursor: pointer;
}

.btn-export {
  border: none;
  padding: 0.5rem 0.9rem;
  border-radius: 6px;
  background: #00a0d8;
  color: #fff;
  cursor: pointer;
}

.btn-export:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.table-wrap {
  overflow-x: auto;
}

table {
  width: max-content;
  min-width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #dbe4f3;
  padding: 8px;
  text-align: center;
  white-space: nowrap;
  font-size: 13px;
}

th {
  background: #022f9d;
  color: white;
}

.col-socio {
  text-align: left;
  position: sticky;
  left: 0;
  background: #f5f8ff;
  min-width: 220px;
  z-index: 1;
}

thead .col-socio {
  background: #022f9d;
  color: white;
}

.col-total {
  font-weight: 700;
  background: #eef4ff;
}

.monto-cell {
  min-width: 82px;
}

.monto-cell-rojo {
  background: #fecdd3;
  color: #7f1d1d;
  font-weight: 700;
}

.loading,
.error,
.empty {
  padding: 1rem;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
}

.btn-page {
  border: none;
  padding: 0.45rem 0.8rem;
  border-radius: 6px;
  background: #022f9d;
  color: #fff;
  cursor: pointer;
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #022f9d;
  font-weight: 600;
}

.error {
  color: #b00020;
}
</style>
