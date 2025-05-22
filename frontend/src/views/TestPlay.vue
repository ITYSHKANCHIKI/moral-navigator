<!-- src/views/TestPlay.vue -->
<template>
  <div class="min-h-screen bg-beige flex flex-col items-center pt-24 px-4 text-black">
    <!-- Заголовок теста -->
    <h1 class="text-4xl font-serif mb-8 text-center">
      {{ testTitle }}
    </h1>

    <!-- Карточка с текстом дилеммы и кнопками -->
    <div
      v-if="currentDilemma"
      class="w-full max-w-2xl bg-white p-6 rounded-lg shadow mb-8"
    >
      <!-- Текст дилеммы -->
      <p class="text-lg leading-relaxed mb-6">
        {{ currentDilemma.question }}
      </p>

      <!-- Кнопки с опциями -->
      <div class="flex flex-col md:flex-row gap-4">
        <button
          v-for="opt in currentDilemma.options"
          :key="opt.id"
          @click="choose(opt.id)"
          class="flex-1 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
        >
          {{ opt.text }}
        </button>
      </div>
    </div>

    <!-- Пока дилеммы нет (загрузка или ошибка) -->
    <p v-else class="text-gray-500">Загрузка дилеммы...</p>

    <!-- Навигационные кнопки -->
    <div class="mt-auto mb-8 flex gap-4">
      <button
        @click="router.back()"
        class="px-4 py-2 bg-blue-400 text-white rounded hover:bg-blue-500 transition"
      >
        ← Назад
      </button>
      <button
        @click="router.push('/')"
        class="px-4 py-2 bg-blue-400 text-white rounded hover:bg-blue-500 transition"
      >
        Домой
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTestsStore } from '@/store/tests'

// стор
const testsStore = useTestsStore()

// роутер и params
const route  = useRoute()
const router = useRouter()
const testId = Number(route.params.id)

// Загружаем сначала тесты (для названия), потом дилеммы
onMounted(async () => {
  await testsStore.fetchTests()
  await testsStore.fetchDilemmas(testId)
})

// текущая дилемма
const currentDilemma = computed(() => {
  return testsStore.dilemmas[testsStore.currentIndex] || null
})

// название теста
const testTitle = computed(() => {
  const t = testsStore.tests.find(x => x.id === testId)
  return t ? t.title : 'Тест'
})

async function choose(optionId) {
  if (!currentDilemma.value) return

  // сохраняем ответ
  testsStore.saveAnswer(
    currentDilemma.value.id,
    optionId
  )

  // если остались дилеммы — переключаемся
  if (testsStore.currentIndex + 1 < testsStore.dilemmas.length) {
    testsStore.currentIndex++
    return
  }

  // завершаем тест, записываем историю и уходим на отчёт
  await testsStore.submitHistory(testId)
  await testsStore.fetchHistory()
  router.push(`/history/${testId}`)
}
</script>

<style scoped>
.bg-beige { background-color: #f1ece2; }
</style>
