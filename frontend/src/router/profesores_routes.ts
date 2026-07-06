import ProfesoresView from '@/views/ProfesoresView.vue'

const profesores_routes = [
  {
    path: '/profesores',
    name: 'profesores',
    component: ProfesoresView
  },
  {
    path: '/profesores/:id',
    name: 'profesores-show',
    component: () => import('@/views/profesores/ProfesoresShowPage.vue')
  },
  {
    path: '/profesores/:id/editar',
    name: 'profesores-edit',
    component: () => import('@/views/profesores/ProfesoresEditPage.vue')
  }
]

export default profesores_routes
