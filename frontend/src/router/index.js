// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../store/user'

import Login         from '../views/Login.vue'
import Profile       from '../views/Profile.vue'
import TestPlay      from '../views/TestPlay.vue'
import JournalDetail from '../views/JournalDetail.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/tests/:id',
    name: 'TestPlay',
    component: TestPlay,
    meta: { requiresAuth: true },
    props: route => ({ testId: +route.params.id })
  },
  {
    path: '/history/:testId',
    name: 'JournalDetail',
    component: JournalDetail,
    meta: { requiresAuth: true },
    props: route => ({ testId: +route.params.testId })
  },
  // если ни одна страница не подошла — кидаем на логин
  {
    path: '/:catchAll(.*)*',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  // если защищённый маршрут и нет токена — на логин
  if (to.meta.requiresAuth && !userStore.token) {
    return next({ name: 'Login' })
  }
  // если пытаемся на логин, но уже есть токен — на профиль
  if (to.name === 'Login' && userStore.token) {
    return next({ name: 'Profile' })
  }
  next()
})

export default router
