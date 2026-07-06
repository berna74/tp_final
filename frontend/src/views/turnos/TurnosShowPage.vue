<template>
  <TurnosShow :id="turnoId" @close="volver" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import TurnosShow from '@/components/turnos/TurnosShow.vue'

const route = useRoute()
const router = useRouter()
const turnoId = computed(() => Number(route.params.id))

function volver() {
  router.push({ name: 'turnos' })
}
</script>
