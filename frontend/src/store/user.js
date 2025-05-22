// src/store/user.js
import { defineStore } from 'pinia'
import api from '../utils/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    me:    null,
    error: ''
  }),

  actions: {
    async login(creds /* { username, password } */) {
      this.error = ''

      try {
        // ① гарантируем чистый plain-object
        const payload = {
          username: creds.username,
          password: creds.password
        }

        // ② JSON-запрос
        const { data } = await api.post('/auth/login-json', payload)

        // ③ сохраняем токен
        this.token = data.access_token
        localStorage.setItem('token', this.token)
        api.defaults.headers.common.Authorization = `Bearer ${this.token}`

        // ④ подтягиваем информацию о себе
        const me = await api.get('/auth/me')
        this.me = me.data
      } catch (err) {
        this.error =
          err?.response?.data?.detail ||
          err.message ||
          'Не удалось войти'
      }
    },

    logout() {
      this.token = ''
      this.me    = null
      localStorage.removeItem('token')
      delete api.defaults.headers.common.Authorization
    }
  }
})
