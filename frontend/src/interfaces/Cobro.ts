export interface Cobro {
  id: number
  socio: number
  socio_nombre: string
  anio: number
  mes: number
  monto_cuota: number | string
  monto_pagado: number | string
  saldo_mes: number | string
  estado: 'Pendiente' | 'Parcial' | 'Pagado' | 'Sin registro'
  fecha_registro_pago: string | null
  metodo_pago: string
  observaciones: string
}

export interface CobroResumenMensual {
  mes: number
  monto_cuota: number
  monto_pagado: number
  saldo_mes: number
  estado: 'Pendiente' | 'Parcial' | 'Pagado' | 'Sin registro'
  fecha_registro_pago: string | null
}

export interface CobroResumenSocio {
  socio_id: number
  socio_nombre: string
  registra_deuda: boolean
  deuda_total: number
  resumen_mensual: CobroResumenMensual[]
}

export interface CobroResumenAnual {
  anio: number
  meses: number[]
  socios: CobroResumenSocio[]
  totales: {
    deuda_global: number
    cantidad_socios_con_deuda: number
  }
}
