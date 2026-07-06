import TurnosView from '@/views/TurnosView.vue'

const turnos_routes = [
  {
    path: '/turnos',
    name: 'turnos',
    component: TurnosView
  },
  {
    path: '/turnos/:id',
    name: 'turnos-show',
    component: () => import('@/views/turnos/TurnosShowPage.vue')
  },
  {
    path: '/turnos/:id/editar',
    name: 'turnos-edit',
    component: () => import('@/views/turnos/TurnosEditPage.vue')
  }
]

export default turnos_routes
