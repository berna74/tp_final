import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { instance as axios } from '@/plugins/axios'

const ACCESS_TOKEN_KEY = 'auth.access'
const REFRESH_TOKEN_KEY = 'auth.refresh'
const USERNAME_KEY = 'auth.username'
const ROLE_KEY = 'auth.role'

export type AuthRole = 'superadmin' | 'admin' | 'socio'

interface LoginResponse {
  access: string
  refresh: string
}

interface RefreshResponse {
  access: string
}

export const useAuthStore = defineStore('auth', () => {
  const tokenAcceso = ref<string>(localStorage.getItem(ACCESS_TOKEN_KEY) || '')
  const tokenRefresh = ref<string>(localStorage.getItem(REFRESH_TOKEN_KEY) || '')
  const username = ref<string>(localStorage.getItem(USERNAME_KEY) || '')
  const role = ref<AuthRole>((localStorage.getItem(ROLE_KEY) as AuthRole) || 'socio')

  const estaAutenticado = computed(() => Boolean(tokenAcceso.value))
  const isSuperadmin = computed(() => role.value === 'superadmin')
  const isAdmin = computed(() => role.value === 'admin')
  const puedeEscribir = computed(() => isSuperadmin.value || isAdmin.value)

  function decodeJwtPayload(token: string): Record<string, unknown> | null {
    const parts = token.split('.')
    if (parts.length < 2) {
      return null
    }

    try {
      const decoded = atob(parts[1].replace(/-/g, '+').replace(/_/g, '/'))
      return JSON.parse(decoded) as Record<string, unknown>
    } catch {
      return null
    }
  }

  function actualizarIdentidadDesdeTokenDeAcceso(access: string) {
    const payload = decodeJwtPayload(access)
    if (!payload) {
      return
    }

    if (typeof payload.username === 'string') {
      username.value = payload.username
      localStorage.setItem(USERNAME_KEY, payload.username)
    }

    if (payload.role === 'superadmin' || payload.role === 'admin' || payload.role === 'socio') {
      role.value = payload.role
      localStorage.setItem(ROLE_KEY, payload.role)
    }
  }

  function setTokens(access: string, refresh?: string) {
    tokenAcceso.value = access
    localStorage.setItem(ACCESS_TOKEN_KEY, access)
    actualizarIdentidadDesdeTokenDeAcceso(access)

    if (typeof refresh === 'string') {
      tokenRefresh.value = refresh
      localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
    }
  }

  function clearTokens() {
    tokenAcceso.value = ''
    tokenRefresh.value = ''
    username.value = ''
    role.value = 'socio'

    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    localStorage.removeItem(USERNAME_KEY)
    localStorage.removeItem(ROLE_KEY)
  }

  async function iniciarSesion(user: string, password: string) {
    const payload = { username: user, password }
    const response = await axios.post<LoginResponse>('/auth/login/', payload)
    setTokens(response.data.access, response.data.refresh)
    if (!username.value) {
      username.value = user
      localStorage.setItem(USERNAME_KEY, user)
    }
  }

  async function refrescarTokenDeAcceso() {
    if (!tokenRefresh.value) {
      throw new Error('No hay refresh token disponible')
    }

    const response = await axios.post<RefreshResponse>('/auth/refresh/', {
      refresh: tokenRefresh.value,
    })

    setTokens(response.data.access)
    return response.data.access
  }

  async function restaurarSesionSiEsPosible() {
    if (tokenAcceso.value || !tokenRefresh.value) {
      return
    }

    try {
      await refrescarTokenDeAcceso()
    } catch {
      clearTokens()
    }
  }

  function cerrarSesion() {
    clearTokens()
  }

  return {
    tokenAcceso,
    tokenRefresh,
    username,
    role,
    estaAutenticado,
    isSuperadmin,
    isAdmin,
    puedeEscribir,
    iniciarSesion,
    cerrarSesion,
    setTokens,
    refrescarTokenDeAcceso,
    restaurarSesionSiEsPosible,
  }
})
