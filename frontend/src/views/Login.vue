<template>
  <!-- Карточка с тенью -->
  <div class="card login-card">
    <h1 class="text-center">Moral&nbsp;Navigator — Вход</h1>

    <!-- Сеткой располагаем «label + input», а кнопка на всю ширину -->
    <form class="form-wrap" @submit.prevent="submitLogin">
      <label for="login">Логин</label>
      <input
        id="login"
        v-model.trim="credentials.username"
        type="text"
        placeholder="Введите логин"
        autocomplete="username"
      />

      <label for="pass">Пароль</label>
      <input
        id="pass"
        v-model.trim="credentials.password"
        type="password"
        placeholder="Введите пароль"
        autocomplete="current-password"
      />

      <!-- кнопка на всю ширину (grid-column: 1 / -1) -->
      <button :disabled="loading">
        {{ loading ? 'Загрузка…' : 'Войти' }}
      </button>
    </form>

    <p v-if="error" class="text-red-600 text-center mt-4">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'

/* реактивное состояние формы */
const credentials = ref({ username: '', password: '' })
const loading     = ref(false)
const error       = ref('')

const router    = useRouter()
const userStore = useUserStore()

async function submitLogin () {
  loading.value = true
  error.value   = ''

  try {
    await userStore.login(credentials.value)

    if (userStore.error) {
      error.value = userStore.error            // сообщение от бекенда
    } else {
      router.push({ name: 'Profile' })         // успех → профиль
    }
  } catch (e) {
    error.value = 'Не удалось авторизоваться'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* доп-отступы только для этой карточки */
.login-card {
  max-width: 480px;
  margin: 3rem auto;
}
</style>
