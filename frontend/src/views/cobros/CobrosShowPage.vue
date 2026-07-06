<template>
  <CobrosShow :cobro-id="cobroId" @close="volver" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CobrosShow from '@/components/cobros/CobrosShow.vue'

const route = useRoute()
const router = useRouter()
const cobroId = computed(() => Number(route.params.id))

function volver() {
  router.push({ name: 'cobros' })
}
</script>
