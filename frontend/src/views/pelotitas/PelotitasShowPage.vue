<template>
  <PelotitasShow :pelotita-id="pelotitaId" @close="volver" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PelotitasShow from '@/components/pelotitas/PelotitasShow.vue'

const route = useRoute()
const router = useRouter()
const pelotitaId = computed(() => Number(route.params.id))

function volver() {
  router.push({ name: 'pelotitas' })
}
</script>
