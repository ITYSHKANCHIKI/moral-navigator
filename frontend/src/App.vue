<template>
  <TornPaperLayout>
    <router-view />
  </TornPaperLayout>
</template>

<script setup>
import TornPaperLayout from './components/TornPaperLayout.vue'
</script>

<style>
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  background: none;
}
</style>
