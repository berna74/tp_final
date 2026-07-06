<template>
  <ProfesoresShow :id="profesorId" @close="volver" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ProfesoresShow from '@/components/profesores/ProfesoresShow.vue'

const route = useRoute()
const router = useRouter()
const profesorId = computed(() => Number(route.params.id))

function volver() {
  router.push({ name: 'profesores' })
}
</script>
