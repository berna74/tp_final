import type { RouteRecordRaw } from 'vue-router'

const cobrosRoutes: RouteRecordRaw[] = [
  {
    path: '/cobros',
    name: 'cobros',
    component: () => import('@/views/CobrosView.vue'),
  },
]

export default cobrosRoutes
