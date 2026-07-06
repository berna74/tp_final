<template>
  <ProfesoresUpdate :id="profesorId" @close="volver" @updated="volver" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ProfesoresUpdate from '@/components/profesores/ProfesoresUpdate.vue'

const route = useRoute()
const router = useRouter()
const profesorId = computed(() => Number(route.params.id))

function volver() {
  router.push({ name: 'profesores' })
}
</script>
