<template>
  <div class="social-links">
    <a href="https://www.facebook.com/paletasoldemayo" target="_blank" rel="noopener noreferrer" title="Facebook">
      <Icon icon="mdi:facebook" width="24" height="24" />
    </a>
    <a href="https://www.instagram.com/paletasoldemayo" target="_blank" rel="noopener noreferrer" title="Instagram">
      <Icon icon="mdi:instagram" width="24" height="24" />
    </a>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
</script>

<style scoped>
.social-links {
  display: flex;
  gap: 1rem;
}

.social-links a {
  color: #ffffff;
  transition: color 0.3s ease;
}

.social-links a:hover {
  color: #00cdff;
}
</style>