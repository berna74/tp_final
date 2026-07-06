<template>
  <PagosUpdate :pago-id="pagoId" @close="volver" @updated="volver" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PagosUpdate from '@/components/pagos/PagosUpdate.vue'

const route = useRoute()
const router = useRouter()
const pagoId = computed(() => Number(route.params.id))

function volver() {
  router.push({ name: 'pagos-registro' })
}
</script>
