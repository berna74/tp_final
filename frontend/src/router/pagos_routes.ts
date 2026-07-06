import type { RouteRecordRaw } from 'vue-router'

const pagosRoutes: RouteRecordRaw[] = [
  {
    path: '/pagos',
    name: 'pagos',
    component: () => import('@/views/PagosView.vue'),
    children: [
      {
        path: '',
        redirect: { name: 'pagos-deudas' },
      },
      {
        path: 'registro',
        name: 'pagos-registro',
        component: () => import('@/views/pagos/PagosRegistroView.vue'),
      },
      {
        path: 'cobros',
        name: 'pagos-cobros',
        component: () => import('@/views/pagos/PagosCobrosView.vue'),
      },
      {
        path: 'deudas',
        name: 'pagos-deudas',
        component: () => import('@/views/pagos/PagosDeudasView.vue'),
      },
      {
        path: 'ultimos-12-meses',
        name: 'pagos-ultimos-12',
        component: () => import('@/views/pagos/PagosUltimos12MesesView.vue'),
      },
      {
        path: 'detalle/:id',
        name: 'pagos-show',
        component: () => import('@/views/pagos/PagosShowPage.vue'),
      },
      {
        path: 'editar/:id',
        name: 'pagos-edit',
        component: () => import('@/views/pagos/PagosEditPage.vue'),
      },
    ],
  },
]

export default pagosRoutes
