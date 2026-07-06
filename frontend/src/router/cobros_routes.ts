import type { RouteRecordRaw } from 'vue-router'

const cobrosRoutes: RouteRecordRaw[] = [
  {
    path: '/cobros',
    name: 'cobros',
    component: () => import('@/views/CobrosView.vue'),
  },
  {
    path: '/cobros/:id',
    name: 'cobros-show',
    component: () => import('@/views/cobros/CobrosShowPage.vue'),
  },
  {
    path: '/cobros/:id/editar',
    name: 'cobros-edit',
    component: () => import('@/views/cobros/CobrosEditPage.vue'),
  },
]

export default cobrosRoutes
