<template>
  <div class="min-h-screen bg-gray-50 font-sans antialiased tracking-tight text-gray-900">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
// Tidak butuh logika berat di sini karena sudah dihandle oleh Router
</script>

<style>
/* Animasi transisi antar halaman agar lebih smooth */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.6 cubic-bezier(0.2, 0.8, 0.2, 1);
}

.fade-enter-from {
  opacity: 0;
  filter: blur(1px); /* Blur lebih dalam untuk transisi masuk */

  opacity: 0;
  filter: blur(1px);
}
</style>
