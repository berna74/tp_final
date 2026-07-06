import PelotitasView from '@/views/PelotitasView.vue'

export default [
  {
    path: '/pelotitas',
    name: 'pelotitas',
    component: PelotitasView
  },
  {
    path: '/pelotitas/:id',
    name: 'pelotitas-show',
    component: () => import('@/views/pelotitas/PelotitasShowPage.vue')
  },
  {
    path: '/pelotitas/:id/editar',
    name: 'pelotitas-edit',
    component: () => import('@/views/pelotitas/PelotitasEditPage.vue')
  }
]
