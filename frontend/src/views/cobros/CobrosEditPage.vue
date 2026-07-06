<template>
  <CobrosUpdate :cobro-id="cobroId" @close="volver" @updated="volver" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CobrosUpdate from '@/components/cobros/CobrosUpdate.vue'

const route = useRoute()
const router = useRouter()
const cobroId = computed(() => Number(route.params.id))

function volver() {
  router.push({ name: 'cobros' })
}
</script>
