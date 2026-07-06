<template>
  <TurnosUpdate :id="turnoId" @close="volver" @updated="volver" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import TurnosUpdate from '@/components/turnos/TurnosUpdate.vue'

const route = useRoute()
const router = useRouter()
const turnoId = computed(() => Number(route.params.id))

function volver() {
  router.push({ name: 'turnos' })
}
</script>
