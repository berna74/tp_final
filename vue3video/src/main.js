import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import  {createVuetify} from 'vuetify'  

import App from './App.vue'
import router from './router'

const app = createApp(App)
const vuetify = createVuetify()

app.use(vuetify)

app.use(createPinia())
app.use(router)

app.mount('#app')
