<template>
  <div v-if="loading" class="page-state">Cargando...</div>
  <div v-else-if="error" class="page-state page-error">{{ error }}</div>
  <SociosShow v-else-if="socio" :socio="socio" @close="volver" />
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import SociosShow from '@/components/socios/SociosShow.vue'
import { useSociosStore } from '@/stores/socios'

const route = useRoute()
const router = useRouter()
const sociosStore = useSociosStore()
const { socio, loading, error } = storeToRefs(sociosStore)
const socioId = computed(() => Number(route.params.id))

onMounted(() => {
  sociosStore.fetchSocio(socioId.value)
})

function volver() {
  router.push({ name: 'socios' })
}
</script>

<style scoped>
.page-state {
  padding: 2rem;
  text-align: center;
}

.page-error {
  color: #b00020;
}
</style>
