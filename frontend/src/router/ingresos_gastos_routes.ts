import type { RouteRecordRaw } from 'vue-router'
import IngresosView from '@/views/IngresosView.vue'
import GastosView from '@/views/GastosView.vue'

const ingresos_gastos_routes: RouteRecordRaw[] = [
  {
    path: '/ingresos',
    name: 'ingresos',
    component: IngresosView,
    meta: { requiresAuth: true }
  },
  {
    path: '/gastos',
    name: 'gastos',
    component: GastosView,
    meta: { requiresAuth: true }
  }
]

export default ingresos_gastos_routes
