<template>
  <div class="pelotitas-view">
    <PelotitasCreate
      v-if="showCreatePanel"
      @close="showCreatePanel = false"
      @saved="handleSaved"
    />
    <PelotitasList
      @showCreate="showCreatePanel = true"
      @showEdit="handleEdit"
      @showView="handleView"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PelotitasList from '@/components/pelotitas/PelotitasList.vue'
import PelotitasCreate from '@/components/pelotitas/PelotitasCreate.vue'
import { usePelotitasStore } from '@/stores/pelotitas'

const pelotitasStore = usePelotitasStore()
const showCreatePanel = ref(false)
const router = useRouter()

const handleEdit = (id: number) => {
  router.push({ name: 'pelotitas-edit', params: { id } })
}

const handleView = (id: number) => {
  router.push({ name: 'pelotitas-show', params: { id } })
}

const handleSaved = async () => {
  await pelotitasStore.fetchPelotitas()
  await pelotitasStore.fetchResumen()
}

const handleUpdated = async () => {
  await pelotitasStore.fetchPelotitas()
  await pelotitasStore.fetchResumen()
}
</script>

<style scoped>
.pelotitas-view {
  background: #f5f7fa;
}
</style>
