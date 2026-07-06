<template>
  <div class="pagos-registro-view">
    <PagosCreate
      v-if="showCreate"
      @close="showCreate = false"
      @created="handleCreated"
    />

    <PagosList
      @create="showCreate = true"
      @edit="handleEdit"
      @show="handleShow"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PagosList from '@/components/pagos/PagosList.vue'
import PagosCreate from '@/components/pagos/PagosCreate.vue'

const showCreate = ref(false)
const router = useRouter()

function handleCreated() {
  showCreate.value = false
}

function handleEdit(id: number) {
  router.push({ name: 'pagos-edit', params: { id } })
}

function handleShow(id: number) {
  router.push({ name: 'pagos-show', params: { id } })
}
</script>

<style scoped>
.pagos-registro-view {
  width: 100%;
}
</style>
