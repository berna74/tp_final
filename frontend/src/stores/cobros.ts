import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'
import type { Cobro, CobroMatrizDosAnios, CobroResumenAnual } from '@/interfaces/Cobro'

interface CobroLotePayload {
  socios_ids: number[]
  socios_rojo_ids?: number[]
  anio: number
  mes: number
  tipo_cobro?: 'mensual' | 'dia_cancha'
  monto_cuota: number
  monto_pagado?: number
  fecha_registro_pago?: string | null
  metodo_pago?: string
  observaciones?: string
  actualizar_existentes?: boolean
  usar_todos_los_socios?: boolean
  marcar_todos_como_usuarios_socio?: boolean
}

export const useCobrosStore = defineStore('cobros', () => {
  const cobros = ref<Cobro[]>([])
  const cobro = ref<Cobro | null>(null)
  const resumen = ref<CobroResumenAnual | null>(null)
  const matrizDosAnios = ref<CobroMatrizDosAnios | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalCount = ref(0)
  const pageSize = ref(10)

  async function fetchCobros(page: number = 1) {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const response = await ApiService.get(`/cobros/?page=${page}`)
      cobros.value = response.data.items || []
      totalPages.value = response.data.total_pages || 1
      totalCount.value = response.data.total_count || 0
      pageSize.value = response.data.page_size || 10
    } catch (e: any) {
      error.value = e.message || 'Error al cargar cobros'
      console.error('Error fetching cobros:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchCobro(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/cobros/${id}`)
      cobro.value = response.data
    } catch (e: any) {
      error.value = e.message || 'Error al cargar cobro'
      console.error('Error fetching cobro:', e)
    } finally {
      loading.value = false
    }
  }

  async function createCobro(cobroData: Partial<Cobro>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/cobros/', cobroData)
      await fetchCobros(currentPage.value)
    } catch (e: any) {
      error.value = e.message || 'Error al crear cobro'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateCobro(id: number, cobroData: Partial<Cobro>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/cobros/${id}`, cobroData)
      await fetchCobros(currentPage.value)
    } catch (e: any) {
      error.value = e.message || 'Error al actualizar cobro'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteCobro(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/cobros/${id}`)
      await fetchCobros(currentPage.value)
    } catch (e: any) {
      error.value = e.message || 'Error al eliminar cobro'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchResumen(anio: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/cobros/resumen/?anio=${anio}`)
      resumen.value = response.data
    } catch (e: any) {
      error.value = e.message || 'Error al cargar resumen de cobros'
      console.error('Error fetching resumen cobros:', e)
    } finally {
      loading.value = false
    }
  }

  async function createCobrosLote(payload: CobroLotePayload) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.post('/cobros/lote/', payload)
      await fetchCobros(currentPage.value)
      return response.data
    } catch (e: any) {
      error.value = e.message || 'Error al crear cobros por lote'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchMatrizDosAnios(page: number = 1, pageSize: number = 15) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/cobros/matriz-dos-anios/?page=${page}&page_size=${pageSize}`)
      matrizDosAnios.value = response.data
    } catch (e: any) {
      error.value = e.message || 'Error al cargar matriz de cobros'
      console.error('Error fetching matriz cobros:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    cobros,
    cobro,
    resumen,
    matrizDosAnios,
    loading,
    error,
    currentPage,
    totalPages,
    totalCount,
    pageSize,
    fetchCobros,
    fetchCobro,
    createCobro,
    updateCobro,
    deleteCobro,
    fetchResumen,
    createCobrosLote,
    fetchMatrizDosAnios,
  }
})
