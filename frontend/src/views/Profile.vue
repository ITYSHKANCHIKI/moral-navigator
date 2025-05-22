<script setup>
import { ref, onMounted } from 'vue'
import { useRouter }      from 'vue-router'
import { useUserStore }   from '@/store/user'
import { useTestsStore }  from '@/store/tests'
import Modal from '../components/Modal.vue'

const router     = useRouter()
const userStore  = useUserStore()
const testsStore = useTestsStore()

const showHistory = ref(false)

onMounted(async () => {
  await testsStore.fetchTests()
  await testsStore.fetchHistory()        // ← подгружаем историю для модалки
})

function goPlay (id) {
  router.push(`/tests/${id}`)
}
function openReport (histId) {
  showHistory.value = false
  router.push(`/history/${histId}`)
}
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center text-white">

    <!-- приветствие -->
    <h1 class="text-4xl md:text-5xl font-bold mb-10 text-center">
      Добро пожаловать,&nbsp;{{ userStore.me?.username || '...' }}!
    </h1>

    <!-- панель действий -->
    <div class="flex gap-4 mb-12">
      <button
        @click="userStore.logout(); router.push('/login')"
        class="px-3 py-1 bg-black rounded hover:bg-neutral-800"
      >
        Выйти
      </button>

      <button
        @click="showHistory = true"
        class="px-3 py-1 border border-blue-500 rounded hover:bg-blue-600/10"
      >
        История
      </button>
    </div>

    <!-- список доступных тестов -->
    <h2 class="text-xl font-semibold mb-4">Доступные тесты</h2>

    <ul v-if="testsStore.tests.length" class="space-y-3">
      <li
        v-for="t in testsStore.tests"
        :key="t.id"
        class="flex items-center gap-4 border-b border-neutral-600 pb-2"
      >
        <span>{{ t.title }}</span>
        <button
          @click="goPlay(t.id)"
          class="px-3 py-1 border border-blue-400 rounded hover:bg-blue-600/10"
        >
          Начать
        </button>
      </li>
    </ul>
    <p v-else class="opacity-60">Тестов пока нет</p>
  </div>

  <!-- Модальное окно история -->
  <Teleport to="body">
    <Modal :show="showHistory" @close="showHistory = false">
      <!-- заголовок -->
      <template #header>
        <h3 class="text-lg font-semibold">История прохождений</h3>
      </template>

      <!-- содержимое -->
      <template #default>
        <ul v-if="testsStore.history.length" class="space-y-2 max-h-[60vh] overflow-auto">
          <li
            v-for="h in testsStore.history"
            :key="h.id"
          >
            <button
              class="w-full flex justify-between items-center px-4 py-2 rounded bg-white text-black hover:bg-blue-50"
              @click="openReport(h.id)"
            >
              <span class="font-medium">
                {{ testsStore.tests.find(t => t.id === h.test_id)?.title || 'Тест' }}
              </span>
              <span class="text-sm opacity-60">
                {{ new Date(h.date).toLocaleDateString() }}
              </span>
            </button>
          </li>
        </ul>

        <p v-else class="opacity-70">История пока пуста.</p>
      </template>
    </Modal>
  </Teleport>
</template>
