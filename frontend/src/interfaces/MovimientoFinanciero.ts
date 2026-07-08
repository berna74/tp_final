export type TipoMovimientoFinanciero = 'ingreso' | 'gasto'

export interface MovimientoFinanciero {
  id?: number
  tipo: TipoMovimientoFinanciero
  fecha: string
  mes?: number
  anio?: number
  grupo: string
  rubro: string
  concepto: string
  monto: number
  metodo: string
  observaciones: string
}