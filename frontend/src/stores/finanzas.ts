import { defineStore } from 'pinia'
import { ref } from 'vue'
import ApiService from '@/services/ApiService'
import type { MovimientoFinanciero, TipoMovimientoFinanciero } from '@/interfaces/MovimientoFinanciero'

export const useFinanzasStore = defineStore('finanzas', () => {
  const movimientos = ref<MovimientoFinanciero[]>([])
  const movimiento = ref<MovimientoFinanciero | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalCount = ref(0)
  const pageSize = ref(20)

  async function fetchMovimientos(tipo: TipoMovimientoFinanciero, page: number = 1, q: string = '', grupo: string = '') {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const query = new URLSearchParams({
        tipo,
        page: String(page),
        page_size: String(pageSize.value),
      })
      if (q.trim()) query.set('q', q.trim())
      if (grupo.trim()) query.set('grupo', grupo.trim())

      const response = await ApiService.get(`/movimientos-financieros/?${query.toString()}`)
      movimientos.value = response.data.items || []
      totalPages.value = response.data.total_pages || 1
      totalCount.value = response.data.total_count || 0
      pageSize.value = response.data.page_size || 20
    } catch (e: any) {
      error.value = e.message || 'Error al cargar movimientos'
      console.error('Error fetching movimientos:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchMovimiento(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/movimientos-financieros/${id}`)
      movimiento.value = response.data
    } catch (e: any) {
      error.value = e.message || 'Error al cargar movimiento'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function createMovimiento(data: MovimientoFinanciero) {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/movimientos-financieros/', data)
    } catch (e: any) {
      error.value = e.message || 'Error al crear movimiento'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateMovimiento(id: number, data: Partial<MovimientoFinanciero>) {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/movimientos-financieros/${id}`, data)
    } catch (e: any) {
      error.value = e.message || 'Error al actualizar movimiento'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteMovimiento(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/movimientos-financieros/${id}`)
    } catch (e: any) {
      error.value = e.message || 'Error al eliminar movimiento'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    movimientos,
    movimiento,
    loading,
    error,
    currentPage,
    totalPages,
    totalCount,
    pageSize,
    fetchMovimientos,
    fetchMovimiento,
    createMovimiento,
    updateMovimiento,
    deleteMovimiento,
  }
})