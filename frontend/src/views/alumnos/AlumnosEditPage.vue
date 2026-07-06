<template>
  <AlumnosUpdate :alumno-id="alumnoId" @close="volver" @updated="volver" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AlumnosUpdate from '@/components/alumnos/AlumnosUpdate.vue'

const route = useRoute()
const router = useRouter()
const alumnoId = computed(() => Number(route.params.id))

function volver() {
  router.push({ name: 'alumnos' })
}
</script>
