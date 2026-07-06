<template>
  <PelotitasUpdate :pelotita-id="pelotitaId" @close="volver" @updated="volver" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PelotitasUpdate from '@/components/pelotitas/PelotitasUpdate.vue'

const route = useRoute()
const router = useRouter()
const pelotitaId = computed(() => Number(route.params.id))

function volver() {
  router.push({ name: 'pelotitas' })
}
</script>
