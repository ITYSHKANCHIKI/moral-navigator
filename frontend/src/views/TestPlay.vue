<!-- frontend/src/views/TestPlay.vue -->
<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTestsStore } from '@/store/tests'

const testsStore = useTestsStore()
const router     = useRouter()
const route      = useRoute()
const testId     = +route.params.id

/** текущее дилемма по индексу */
const current = computed(() =>
  testsStore.dilemmas[testsStore.currentIndex] ?? null
)

onMounted(() => testsStore.fetchDilemmas(testId))

/** обработчик выбора варианта */
async function choose (optionId) {
  testsStore.saveAnswer(current.value.id, optionId)

  if (testsStore.currentIndex + 1 < testsStore.dilemmas.length) {
    testsStore.currentIndex++
    return
  }

  await testsStore.submitHistory(testId)
  await testsStore.fetchHistory()
  router.push(`/history/${testId}`)
}
</script>

<template>
  <div class="min-h-screen flex flex-col items-center pt-6">
    <!-- заголовок дилеммы -->
    <h1 class="text-4xl font-bold mb-4 text-center">
      {{ current?.title || 'Тест' }}
    </h1>

    <!-- собственно текст дилеммы -->
    <p
      v-if="current"
      class="max-w-3xl mb-8 text-lg leading-relaxed whitespace-pre-line text-center"
    >
      {{ current.text }}
    </p>

    <!-- варианты ответа -->
    <div v-if="current" class="flex flex-wrap gap-4 mb-8 justify-center">
      <button
        v-for="opt in current.options"
        :key="opt.id"
        @click="choose(opt.id)"
        class="px-4 py-2 rounded bg-blue-600 hover:bg-blue-700 text-white"
      >
        {{ opt.text }}
      </button>
    </div>

    <!-- кнопки навигации -->
    <div class="flex gap-4">
      <button @click="router.back()" class="px-4 py-2 rounded bg-blue-600 text-white">← Назад</button>
      <button @click="router.push('/')" class="px-4 py-2 rounded bg-blue-600 text-white">Домой</button>
    </div>
  </div>
</template>
