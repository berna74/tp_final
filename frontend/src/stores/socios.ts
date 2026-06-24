import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Socio } from '@/interfaces/Socio'
import ApiService from '@/services/ApiService'

export const useSociosStore = defineStore('socios', () => {
  const socios = ref<Socio[]>([])
  const socio = ref<Socio | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPage = ref(1)
  const totalPages = ref(1)
  const totalCount = ref(0)
  const pageSize = ref(10)

  function ordenarPorApellidoYNombre<T extends { apellido?: string; nombre?: string }>(items: T[]): T[] {
    return [...items].sort((a, b) => {
      const apellidoA = (a.apellido || '').toLowerCase().trim()
      const apellidoB = (b.apellido || '').toLowerCase().trim()
      const porApellido = apellidoA.localeCompare(apellidoB, 'es', { sensitivity: 'base' })

      if (porApellido !== 0) {
        return porApellido
      }

      const nombreA = (a.nombre || '').toLowerCase().trim()
      const nombreB = (b.nombre || '').toLowerCase().trim()
      return nombreA.localeCompare(nombreB, 'es', { sensitivity: 'base' })
    })
  }

  async function fetchSocios(page: number = 1) {
    loading.value = true
    error.value = null
    try {
      currentPage.value = page
      const response = await ApiService.get(`/socios/?page=${page}`)
      const data = response.data

      if (Array.isArray(data)) {
        socios.value = ordenarPorApellidoYNombre(data)
        totalCount.value = data.length
        pageSize.value = data.length || 10
        totalPages.value = 1
      } else {
        socios.value = ordenarPorApellidoYNombre(data.items || [])
        totalPages.value = data.total_pages || 1
        totalCount.value = data.total_count || 0
        pageSize.value = data.page_size || 10
      }
    } catch (err: any) {
      error.value = err.message || 'Error al cargar los socios'
    } finally {
      loading.value = false
    }
  }

  async function fetchSocio(id: number) {
    loading.value = true
    error.value = null
    try {
      const response = await ApiService.get(`/socios/${id}`)
      socio.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Error al cargar el socio'
    } finally {
      loading.value = false
    }
  }

  async function createSocio(socioData: any) {
    loading.value = true
    error.value = null
    try {
      await ApiService.post('/socios/', socioData)
      await fetchSocios(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al crear el socio'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateSocio(id: number, socioData: any) {
    loading.value = true
    error.value = null
    try {
      await ApiService.put(`/socios/${id}`, socioData)
      await fetchSocios(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al actualizar el socio'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteSocio(id: number) {
    loading.value = true
    error.value = null
    try {
      await ApiService.delete(`/socios/${id}`)
      await fetchSocios(currentPage.value)
    } catch (err: any) {
      error.value = err.message || 'Error al eliminar el socio'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    socios,
    socio,
    loading,
    error,
    currentPage,
    totalPages,
    totalCount,
    pageSize,
    fetchSocios,
    fetchSocio,
    createSocio,
    updateSocio,
    deleteSocio
  }
})
