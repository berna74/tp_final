<template>
  <MenuPrincipal />
  <main>
    <RouterView />
  </main>
</template>

<script setup lang="ts">
import MenuPrincipal from '@/components/MenuPrincipal.vue'
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