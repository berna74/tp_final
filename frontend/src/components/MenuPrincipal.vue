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
      <RouterLink :to="{ name: 'profesores' }" @click="cerrarMenu">Profesores</RouterLink>
      <RouterLink :to="{ name: 'pagos-deudas' }" @click="cerrarMenu">Pagos</RouterLink>
      <RouterLink :to="{ name: 'cobros' }" @click="cerrarMenu">Cobros</RouterLink>
      <RouterLink :to="{ name: 'pelotitas' }" @click="cerrarMenu">Pelotitas</RouterLink>
      <RouterLink :to="{ name: 'ingresos-gastos' }" @click="cerrarMenu">Ingresos/Gastos</RouterLink>
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
  height: 100%;
  line-height: 0;
  z-index: 1001;
}

.logo {
  width: 15rem;
  height: auto;
  margin: 0;
  display: block;
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
    padding: 0.35rem 0.25rem 0.5rem;
    height: auto;
    min-height: 5.4rem;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.3rem;
  }

  .logo-link {
    width: 95vw;
    max-width: 95vw;
    justify-content: center;
    padding: 0;
    height: auto;
    margin-top: 0.35rem;
  }

  .logo {
    width: 100%;
    height: auto;
    max-height: none;
    object-fit: initial;
  }

  .menu-toggle {
    display: block;
    position: static;
    transform: none;
    width: 3rem;
    height: 3rem;
    align-items: center;
    justify-content: center;
    background: rgba(2, 47, 157, 0.92);
    border-radius: 0.5rem;
  }

  .nav-links {
    position: fixed;
    top: 5.4rem;
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
  nav {
    padding: 0.25rem 0.2rem;
    min-height: 5rem;
  }

  .logo-link {
    width: 95vw;
    max-width: 95vw;
    padding: 0;
    margin-top: 0.25rem;
  }

  .nav-links {
    top: 5rem;
  }

  .menu-toggle {
    width: 2.8rem;
    height: 2.8rem;
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
