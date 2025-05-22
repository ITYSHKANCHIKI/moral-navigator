// src/utils/api.js
import axios from 'axios'
import { useUserStore } from '../store/user'

// можно вынести адрес в .env: VITE_API_URL
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// JWT токен в каждом запросе
api.interceptors.request.use(
  config => {
    const userStore = useUserStore()
    if (userStore.token) {
      // ОБРАТИТЕ ВНИМАНИЕ на обратные кавычки!
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  error => Promise.reject(error)
)

export default api
