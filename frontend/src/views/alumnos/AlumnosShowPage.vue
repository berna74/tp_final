<template>
  <AlumnosShow :alumno-id="alumnoId" @close="volver" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AlumnosShow from '@/components/alumnos/AlumnosShow.vue'

const route = useRoute()
const router = useRouter()
const alumnoId = computed(() => Number(route.params.id))

function volver() {
  router.push({ name: 'alumnos' })
}
</script>
