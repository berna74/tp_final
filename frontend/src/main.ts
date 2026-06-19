import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { setupAxiosInterceptors } from './plugins/axios'
import { useAuthStore } from './stores/auth'

// Iconify
import { Icon } from '@iconify/vue'
import './plugins/customIcons'

// oh-vue-icons (mantener por compatibilidad)
import { OhVueIcon, addIcons } from "oh-vue-icons";
import { 
  FaDesktop, 
  FaTags, 
  FaTruck, 
  FaFolderOpen,
  FaUsers,
  FaUserGraduate,
  FaClock,
  FaUserCheck,
  FaLayerGroup,
  FaCreditCard
} from 'oh-vue-icons/icons'

addIcons(
  FaDesktop, 
  FaTags, 
  FaTruck, 
  FaFolderOpen,
  FaUsers,
  FaUserGraduate,
  FaClock,
  FaUserCheck,
  FaLayerGroup,
  FaCreditCard
);


const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

setupAxiosInterceptors(pinia, router)

const storeAuth = useAuthStore(pinia)
storeAuth.restaurarSesionSiEsPosible()

app.component("v-icon", OhVueIcon)
app.component("Icon", Icon)

app.mount('#app')
