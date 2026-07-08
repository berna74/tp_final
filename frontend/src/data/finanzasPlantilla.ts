export type TipoFinanzas = 'ingreso' | 'gasto'

export interface GrupoRubros {
  grupo: string
  rubros: string[]
}

export const configuracionRubros: Record<TipoFinanzas, GrupoRubros[]> = {
  ingreso: [
    { grupo: 'Cuotas y cancha', rubros: ['Abonos y turnos', 'Otro'] },
    { grupo: 'Ventas operativas', rubros: ['Pelotitas', 'Bebidas interno', 'Otro'] },
    { grupo: 'Eventos y torneos', rubros: ['Torneo patagonico', 'Otro'] },
    { grupo: 'Indumentaria', rubros: ['Remeras, buzos y rompevientos', 'Otro'] },
  ],
  gasto: [
    { grupo: 'Operacion y mantenimiento', rubros: ['Limpieza', 'Gas', 'Luz', 'Arreglo techos', 'Art. limpieza y art. bano', 'Art. bano/vestuario', 'Plomero/Gasista', 'Pintura y demas', 'Cortinas', 'Internet/chromecast', 'Otro'] },
    { grupo: 'Pelotitas y stock', rubros: ['Pelotitas + flete', 'Otro'] },
    { grupo: 'Honorarios y canones', rubros: ['Profesor', 'Canon Veteranos/Federacion RN', 'Otro'] },
    { grupo: 'Eventos y torneos', rubros: ['Gastos torneo Patagonico', 'Vajilla torneo', 'Premios interno', 'Remeras torneo', 'Otro'] },
    { grupo: 'Indumentaria', rubros: ['Rompevientos y buzos', 'Otro'] },
    { grupo: 'Administracion', rubros: ['Impresiones', 'Otro'] },
  ],
}

export const sugerenciasCarga: Record<TipoFinanzas, string[]> = {
  ingreso: [
    'Use Cuotas y cancha para abonos y alquileres que hoy nacen en pagos/cobros.',
    'Registre ventas de pelotitas e indumentaria como ingresos separados para medir margen.',
    'Cargue eventos extraordinarios con concepto detallado para luego resumir por torneo o interno.',
  ],
  gasto: [
    'Separe operacion diaria de gastos extraordinarios para que el resumen mensual sea legible.',
    'Relacione pelotitas + flete con las compras del modulo de pelotitas para controlar stock y costo.',
    'Use Eventos y torneos para premios, vajilla, remeras y otros gastos puntuales de competencia.',
  ],
}

export const obtenerRubrosDeGrupo = (tipo: TipoFinanzas, grupo: string) =>
  configuracionRubros[tipo].find((item) => item.grupo === grupo)?.rubros ?? []

export const formatearMoneda = (valor: number) =>
  new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    maximumFractionDigits: 0,
  }).format(valor)

export const formatearFecha = (valor: string) =>
  new Date(`${valor}T00:00:00`).toLocaleDateString('es-AR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
