import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../utils/api'
import { getStrategy } from '../logic/strategy'

export const useTestsStore = defineStore('tests', () => {
  const tests        = ref([])
  const dilemmas     = ref([])
  const currentIndex = ref(0)
  const answers      = ref([])

  const history    = ref([])
  const lastResult = ref(null)

  // 1) список всех тестов
  async function fetchTests() {
    const { data } = await api.get('/tests')
    tests.value = data
  }

  // 2) подгрузка дилемм для конкретного теста
  async function fetchDilemmas(testId) {
    const { data } = await api.get(`/tests/${testId}/dilemmas`)
    dilemmas.value     = data
    currentIndex.value = 0
    answers.value      = []
  }

  // 3) сохранить один ответ
  function saveAnswer(dilemmaId, optionId) {
    answers.value.push({ dilemma_id: dilemmaId, option_id: optionId })
  }

  // 4) отправить историю и сразу посчитать локальный результат
  async function submitHistory(testId) {
    // а) POST /history
    await api.post('/history', { test_id: testId, answers: answers.value })

    // б) вычисляем финальный результат на клиенте
    const test     = tests.value.find(t => t.id === testId)
    const strategy = getStrategy(test.evaluation)
    // из каждой записи answers вытаскиваем score из опции
    const enriched = answers.value.map(a => {
      const opt = dilemmas.value
        .flatMap(d => d.options)
        .find(o => o.id === a.option_id)
      return { ...a, score: opt?.score ?? 0 }
    })
    lastResult.value = strategy.calculate(enriched)

    // в) кладём в локальный стор новую запись
    history.value.unshift({
      id: Date.now(),
      test_id: testId,
      date: new Date().toISOString(),
      result_text: lastResult.value.text
    })
  }

  // 5) GET /history
  async function fetchHistory() {
    if (history.value.length) return
    const { data } = await api.get('/history')
    history.value = data
  }

  return {
    tests,
    dilemmas,
    currentIndex,
    answers,
    history,
    lastResult,

    fetchTests,
    fetchDilemmas,
    saveAnswer,
    submitHistory,
    fetchHistory,
  }
})
