<template>
  <div class="login-page">
    <section class="login-wrapper">
      <div class="login-card">
        <div class="login-header">
          <div>
            <h2>Ingresar</h2>
            <p>Ingresa tus credenciales para acceder al sistema.</p>
          </div>
        </div>

        <form class="login-form" @submit.prevent="enviarFormulario">
          <label for="username">Usuario</label>
          <input
            id="username"
            v-model="username"
            type="text"
            autocomplete="username"
            required
            :disabled="loading"
          />

          <label for="password">Contrasena</label>
          <input
            id="password"
            v-model="password"
            type="password"
            autocomplete="current-password"
            required
            :disabled="loading"
          />

          <p v-if="mensajeError" class="error" role="alert">{{ mensajeError }}</p>

          <button type="submit" :disabled="loading">
            {{ loading ? 'Ingresando...' : 'Ingresar' }}
          </button>

          <button type="button" class="secondary-button" @click="mostrarAyudaRegistro = !mostrarAyudaRegistro">
            Registrarse
          </button>

          <p v-if="mostrarAyudaRegistro" class="register-hint" role="status">
            Para registrarte, solicitá el alta con un administrador del club.
          </p>
        </form>
      </div>
    </section>

    <footer class="login-footer">
      <img src="/images/logo-club.png" alt="Logo Club Sol de Mayo" class="footer-logo">
      <p class="footer-address">Club Sol de Mayo - Av. Francisco de Viedma 1057, Viedma, Río Negro.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')
const loading = ref(false)
const mensajeError = ref('')
const mostrarAyudaRegistro = ref(false)

async function enviarFormulario() {
  loading.value = true
  mensajeError.value = ''

  try {
    await authStore.iniciarSesion(username.value, password.value)
    const destinoRedireccion = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
    await router.push(destinoRedireccion)
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      mensajeError.value = 'Usuario o contrasena incorrectos.'
    } else {
      mensajeError.value = 'No se pudo iniciar sesion. Intenta nuevamente.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 4rem);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 2rem;
  padding: 2rem 1rem 1.5rem;
  box-sizing: border-box;
}

.login-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.login-card {
  width: 100%;
  max-width: 100%;
  width: min(560px, 100%);
  box-sizing: border-box;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(2, 47, 157, 0.16);
  padding: 2rem;
}

.login-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.25rem;
}

h2 {
  margin: 0;
  color: #022f9d;
}

p {
  margin-top: 0.5rem;
  margin-bottom: 1.5rem;
  color: #4b4b4b;
}

.login-form {
  display: grid;
  gap: 0.75rem;
}

label {
  font-weight: 600;
  color: #022f9d;
}

input {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 0.7rem 0.8rem;
  font-size: 1rem;
}

input:focus {
  border-color: #022f9d;
  outline: 2px solid rgba(2, 47, 157, 0.2);
}

button {
  width: 100%;
  margin-top: 0.5rem;
  border: none;
  border-radius: 8px;
  background: #022f9d;
  color: #ffffff;
  font-weight: 600;
  padding: 0.8rem 1rem;
  cursor: pointer;
}

button:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.error {
  margin: 0.25rem 0;
  color: #b91c1c;
  font-size: 0.95rem;
}

.secondary-button {
  margin-top: 0;
  background: transparent;
  color: #022f9d;
  border: 1px solid #022f9d;
}

.secondary-button:hover {
  background: rgba(2, 47, 157, 0.06);
}

.register-hint {
  margin: 0.25rem 0 0;
  color: #4b4b4b;
  font-size: 0.92rem;
}

.login-footer {
  border-top: 1px solid #e0e0e0;
  text-align: center;
  padding-top: 1.25rem;
}

.footer-logo {
  max-width: 84px;
  height: auto;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}

.footer-address {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

@media (max-width: 768px) {
  .login-page {
    min-height: calc(100vh - 3.5rem);
  }

  .login-card {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .login-page {
    min-height: calc(100vh - 3rem);
    padding: 1.25rem 0.75rem 1rem;
  }

  .login-card {
    padding: 1.25rem;
  }
}
</style>
