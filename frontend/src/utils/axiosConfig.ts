import axios from 'axios'
import { BACKEND_URL } from './api'

// Criar instância do axios
export const apiClient = axios.create({
  baseURL: BACKEND_URL,
})

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')

  console.log('TOKEN ENVIADO:', token)

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

// Interceptor para adicionar token em todas as requisições
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor de resposta para tratar erros 401
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn('Token inválido ou expirado')
      // NÃO remove automaticamente
    }
    return Promise.reject(error)
  }
)

export default apiClient
