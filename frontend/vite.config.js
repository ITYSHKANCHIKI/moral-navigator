// vite.config.js
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      // Проксируем все запросы, начинающиеся на /api, на ваш FastAPI
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        // не переписываем, оставляем /api/v1/… на бэке
        // rewrite здесь не обязателен, но можно:
        // rewrite: path => path.replace(/^\/api/, '/api'),
      }
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
