<template>
  <button
    :disabled="loading"
    class="w-full bg-slate-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center"
  >
    <span v-if="loading" class="animate-spin mr-2">◌</span>
    <slot />
  </button>
</template>

<script setup>
defineProps({ loading: Boolean })
</script>
