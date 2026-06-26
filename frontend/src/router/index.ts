import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import turnos_routes from './turnos_routes'
import socios_routes from './socios_routes'
import categorias_routes from './categorias_routes'
import profesores_routes from './profesores_routes'
import alumnos_routes from './alumnos_routes'
import pagos_routes from './pagos_routes'
import pelotitas_routes from './pelotitas_routes'
import cobros_routes from './cobros_routes'
import ingresos_gastos_routes from './ingresos_gastos_routes'

// Club de Tenis - Sistema de Administración

const rutasApp: RouteRecordRaw[] = [
  ...turnos_routes,
  ...socios_routes,
  ...categorias_routes,
  ...profesores_routes,
  ...alumnos_routes,
  ...pagos_routes,
  ...cobros_routes,
  ...pelotitas_routes,
  ...ingresos_gastos_routes,
]

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { guestOnly: true },
  },
  ...rutasApp,
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach(async (destino) => {
  const authStore = useAuthStore()

  if (!authStore.estaAutenticado && authStore.tokenRefresh) {
    await authStore.restaurarSesionSiEsPosible()
  }

  if (destino.meta.requiresAuth && !authStore.estaAutenticado) {
    return { name: 'login', query: { redirect: destino.fullPath } }
  }

  if (destino.meta.requiresWrite && !authStore.puedeEscribir) {
    return { name: 'home' }
  }

  if (destino.meta.guestOnly && authStore.estaAutenticado) {
    return { name: 'home' }
  }

  return true
})

export default router