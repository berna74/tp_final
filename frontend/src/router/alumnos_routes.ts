import type { RouteRecordRaw } from 'vue-router'

const alumnosRoutes: RouteRecordRaw[] = [
  {
    path: '/alumnos',
    name: 'alumnos',
    component: () => import('@/views/AlumnosView.vue')
  },
  {
    path: '/alumnos/:id',
    name: 'alumnos-show',
    component: () => import('@/views/alumnos/AlumnosShowPage.vue'),
  },
  {
    path: '/alumnos/:id/editar',
    name: 'alumnos-edit',
    component: () => import('@/views/alumnos/AlumnosEditPage.vue'),
  }
]

export default alumnosRoutes
