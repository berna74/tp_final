import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios'
import type { Router } from 'vue-router'
import type { Pinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'

const instance = axios.create({
    baseURL: '/api/',
    timeout: 10000,
})

type RetryableRequestConfig = InternalAxiosRequestConfig & {
    _retry?: boolean
}

let solicitudRefresh: Promise<string> | null = null

function esEndpointDeAuth(url?: string) {
    return Boolean(url && (url.includes('/auth/login/') || url.includes('/auth/refresh/')))
}

function redirigirALogin(router: Router) {
    if (router.currentRoute.value.name !== 'login') {
        router.push({ name: 'login' })
    }
}

export function setupAxiosInterceptors(pinia: Pinia, router: Router) {
    instance.interceptors.request.use((config) => {
        const authStore = useAuthStore(pinia)
        if (authStore.tokenAcceso) {
            config.headers.Authorization = `Bearer ${authStore.tokenAcceso}`
        }
        return config
    })

    instance.interceptors.response.use(
        (response) => response,
        async (error: AxiosError) => {
            const authStore = useAuthStore(pinia)
            const solicitudOriginal = error.config as RetryableRequestConfig | undefined

            if (!solicitudOriginal || error.response?.status !== 401 || solicitudOriginal._retry || esEndpointDeAuth(solicitudOriginal.url)) {
                return Promise.reject(error)
            }

            if (!authStore.tokenRefresh) {
                authStore.cerrarSesion()
                redirigirALogin(router)
                return Promise.reject(error)
            }

            solicitudOriginal._retry = true

            try {
                if (!solicitudRefresh) {
                    solicitudRefresh = authStore.refrescarTokenDeAcceso().finally(() => {
                        solicitudRefresh = null
                    })
                }

                const nuevoTokenAcceso = await solicitudRefresh
                solicitudOriginal.headers.Authorization = `Bearer ${nuevoTokenAcceso}`
                return instance(solicitudOriginal)
            } catch (errorRefresh) {
                authStore.cerrarSesion()
                redirigirALogin(router)
                return Promise.reject(errorRefresh)
            }
        },
    )
}

export { instance }