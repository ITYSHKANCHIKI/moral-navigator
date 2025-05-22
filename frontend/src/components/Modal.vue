<template>
  <!-- v-if создаёт элемент только когда show === true -->
  <div v-if="show" class="backdrop" @click.self="$emit('close')">
    <div class="window">
      <header class="head">
        <slot name="header"/>
        <button class="close" @click="$emit('close')">✕</button>
      </header>
      <div class="body">
        <slot/>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ show: Boolean })
</script>

<style scoped>
.backdrop{
  position:fixed; inset:0; z-index:1000;
  display:flex; justify-content:center; align-items:center;
  background:rgba(0,0,0,.45);
}
.window{
  width:100%; max-width:600px;
  background:#fff; border-radius:.75rem;
  box-shadow:0 8px 24px rgb(0 0 0 /.18);
  overflow:hidden;
}
.head{
  display:flex; justify-content:space-between; align-items:center;
  padding:1rem 1.25rem; background:#ebe7df;
  font-weight:600;
}
.close{
  background:none; border:none; font-size:1.25rem; cursor:pointer;
}
.body{ padding:1.25rem; max-height:60vh; overflow:auto }
</style>
