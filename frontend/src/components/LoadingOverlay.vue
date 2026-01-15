<template>
  <Transition name="fade">
    <div
      v-if="show"
      class="fixed inset-0 z-[9999] flex flex-col items-center justify-center bg-white/40 backdrop-blur-[1px]"
    >
      <div class="relative flex items-center justify-center">
        <div
          class="h-20 w-20 rounded-full border-4 border-gray-100 border-t-blue-600 animate-spin"
        ></div>
        <div class="absolute h-10 w-10 bg-blue-500 rounded-lg animate-pulse opacity-50"></div>
      </div>

      <div class="mt-6 text-center">
        <h3 class="text-xl font-bold text-gray-800 tracking-tight">Loading</h3>
        <p class="text-gray-500 text-sm mt-1 font-medium italic">Please wait...</p>
      </div>
    </div>
  </Transition>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    default: false,
  },
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
