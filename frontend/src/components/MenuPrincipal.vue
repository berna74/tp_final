<template>
  <nav>
    <RouterLink :to="{ name: 'home' }" class="logo-link" @click="cerrarMenu" aria-label="Inicio">
      <img src="/images/logo.svg" alt="Logo" class="logo" />
    </RouterLink>

    <button class="menu-toggle" @click="alternarMenu" :aria-label="menuAbierto ? 'Cerrar menú' : 'Abrir menú'">
      <Icon :icon="menuAbierto ? 'mdi:close' : 'mdi:menu'" width="28" height="28" />
    </button>

    <div class="nav-links" :class="{ 'nav-links-open': menuAbierto }">
      <RouterLink :to="{ name: 'socios' }" @click="cerrarMenu">Socios</RouterLink>
      <RouterLink :to="{ name: 'alumnos' }" @click="cerrarMenu">Alumnos</RouterLink>
      <RouterLink :to="{ name: 'turnos' }" @click="cerrarMenu">Turnos</RouterLink>
      <RouterLink :to="{ name: 'profesores' }" @click="cerrarMenu">Profesores</RouterLink>
      <RouterLink :to="{ name: 'pagos' }" @click="cerrarMenu">Pagos</RouterLink>
      <RouterLink :to="{ name: 'pelotitas' }" @click="cerrarMenu">Pelotitas</RouterLink>
      <EnlacesRedesSociales class="social-links-container" />
      <RouterLink
        v-if="!authStore.estaAutenticado"
        :to="{ name: 'login' }"
        class="login-entry"
        @click="cerrarMenu"
      >
        <Icon icon="mdi:login-variant" width="20" height="20" />
        <span>Ingresar</span>
      </RouterLink>
      <button v-else class="login-entry logout-entry" @click="manejarCierreSesion" type="button">
        <Icon icon="mdi:logout-variant" width="20" height="20" />
        <span>Salir</span>
      </button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Icon } from '@iconify/vue'
import EnlacesRedesSociales from '@/components/EnlacesRedesSociales.vue'
import { useAuthStore } from '@/stores/auth'

const menuAbierto = ref(false)
const router = useRouter()
const authStore = useAuthStore()

const alternarMenu = () => {
  menuAbierto.value = !menuAbierto.value
}

const cerrarMenu = () => {
  menuAbierto.value = false
}

const manejarCierreSesion = async () => {
  authStore.cerrarSesion()
  cerrarMenu()
  await router.push({ name: 'login' })
}
</script>

<style scoped>
nav {
  background: #022f9d;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 4rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  position: relative;
}

.logo-link {
  display: flex;
  align-items: center;
  z-index: 1001;
}

.logo {
  width: 15rem;
  height: auto;
  margin: 0;
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  color: #ffffff;
  cursor: pointer;
  padding: 0.5rem;
  z-index: 1001;
  transition: color 0.3s ease;
}

.menu-toggle:hover {
  color: #00cdff;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
  justify-content: flex-start;
  margin-left: 2rem;
}

.nav-links a {
  color: #ffffff;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
  white-space: nowrap;
}

.nav-links a:hover {
  color: #00cdff;
}

.nav-links a.router-link-exact-active {
  color: #ffcd00;
  font-weight: 600;
}

.social-links-container {
  margin-left: auto;
  display: flex;
}

.login-entry {
  margin-left: 1rem;
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 999px;
  padding: 0.55rem 0.9rem;
  color: #ffffff;
  background: rgba(255, 255, 255, 0.08);
  font-weight: 700;
  transition: all 0.25s ease;
}

.login-entry:hover {
  background: #ffffff;
  color: #022f9d;
  border-color: #ffffff;
}

.logout-entry {
  cursor: pointer;
}

.login-entry :deep(.ov-icon) {
  color: currentColor;
}

@media (max-width: 768px) {
  nav {
    padding: 0.75rem 1rem;
    height: 3.5rem;
  }

  .logo {
    width: 10rem;
  }

  .menu-toggle {
    display: block;
  }

  .nav-links {
    position: fixed;
    top: 3.5rem;
    left: 0;
    right: 0;
    background: #022f9d;
    flex-direction: column;
    align-items: stretch;
    gap: 0;
    margin: 0;
    padding: 1rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    max-height: 0;
    overflow: hidden;
    opacity: 0;
    transition: max-height 0.4s ease, opacity 0.3s ease;
    z-index: 1000;
  }

  .nav-links-open {
    max-height: calc(100vh - 3.5rem);
    opacity: 1;
  }

  .nav-links a {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    text-align: left;
  }

  .nav-links a:last-of-type {
    border-bottom: none;
  }

  .social-links-container {
    margin: 1rem 0 0;
    padding: 1rem 1.5rem 0;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    justify-content: center;
  }

  .login-entry {
    margin: 1rem 1.5rem 0;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .logo {
    width: 8rem;
  }

  nav {
    padding: 0.5rem 1rem;
    height: 3rem;
  }

  .nav-links {
    top: 3rem;
  }

  .menu-toggle {
    padding: 0.25rem;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .logo {
    width: 12rem;
  }

  .nav-links {
    gap: 1rem;
    margin-left: 1rem;
  }

  .nav-links a {
    font-size: 0.9rem;
  }
}
</style>
