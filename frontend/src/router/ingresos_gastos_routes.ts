import type { RouteRecordRaw } from 'vue-router'

const ingresos_gastos_routes: RouteRecordRaw[] = [
  {
    path: '/ingresos-gastos',
    name: 'ingresos-gastos',
    component: { template: '<div style="padding: 2rem; text-align: center;"><h2>Ingresos y Gastos</h2><p style="color: #666; font-size: 1.1rem;">Próximamente...</p></div>' },
    meta: { requiresAuth: true }
  }
]

export default ingresos_gastos_routes
