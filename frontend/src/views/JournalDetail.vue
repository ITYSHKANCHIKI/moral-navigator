<template>
  <div class="p-6">
    <h1 class="text-2xl mb-4">Отчёт по тесту</h1>
    <div v-if="!history.length">Загрузка…</div>
    <ul v-else>
      <li
        v-for="h in history"
        :key="h.id"
        class="mb-2 border-b pb-2"
      >
        <p><strong>Дилемма:</strong> {{ h.dilemma_text }}</p>
        <p><strong>Выбор:</strong> {{ h.option_text }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted } from "vue"
import { useRoute } from "vue-router"
import { useTestsStore } from "../store/tests"

const route = useRoute()
const testsStore = useTestsStore()
const testId = Number(route.params.id)

onMounted(async () => {
  await testsStore.fetchHistory()
})

const history = computed(() => testsStore.history[testId] || [])
</script>
