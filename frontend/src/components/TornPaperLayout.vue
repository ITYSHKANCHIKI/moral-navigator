<template>
  <div class="layout-root">
    <header class="header-layer">
      <slot name="header">
        <h1>Моральный навигатор</h1>
      </slot>
    </header>

    <main class="content-layer">
      <slot/>
    </main>

    <footer class="footer-layer">
      <nav class="footer-nav">
        <button @click="$router.back()">← Назад</button>
        <button @click="goHome">Домой</button>
      </nav>
    </footer>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router=useRouter()
const goHome=()=>router.push('/')
</script>

<style scoped>
/* слои */
.layout-root{min-height:100vh;display:flex;flex-direction:column}

.header-layer{
  padding:1.5rem 1rem;
  background:var(--beige-3);
  color:#fff;
  clip-path:polygon(0 0,100% 0,100% 85%,0 100%);
}

.content-layer{
  flex:1 1 auto;
  padding:2rem 1.25rem;
  background:var(--beige-2);
  clip-path:polygon(0 0,100% 0,100% 100%,0 85%);
}

.footer-layer{
  padding:1.25rem 1rem 2.5rem;
  background:var(--beige-1);
  clip-path:polygon(0 15%,100% 0,100% 100%,0 100%);
}

/* чтобы слой не перекрывал клики по кнопкам */
.footer-layer::before{pointer-events:none}
</style>
