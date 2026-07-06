import SociosView from '@/views/SociosView.vue'

const socios_routes = [
  {
    path: '/socios',
    name: 'socios',
    component: SociosView
  },
  {
    path: '/socios/:id',
    name: 'socios-show',
    component: () => import('@/views/socios/SociosShowPage.vue')
  },
  {
    path: '/socios/:id/editar',
    name: 'socios-edit',
    component: () => import('@/views/socios/SociosEditPage.vue')
  }
]

export default socios_routes
