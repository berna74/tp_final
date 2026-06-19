<template>
  <MenuPrincipal v-if="!hideMenu" />
  <main>
    <RouterView />
  </main>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import MenuPrincipal from '@/components/MenuPrincipal.vue'

const route = useRoute()
const hideMenu = computed(() => Boolean(route.meta.hideMenu))
</script>

<style>
main {
  min-height: calc(100vh - 4rem);
}

@media (max-width: 768px) {
  main {
    min-height: calc(100vh - 3.5rem);
  }
}

@media (max-width: 480px) {
  main {
    min-height: calc(100vh - 3rem);
  }
}
</style>