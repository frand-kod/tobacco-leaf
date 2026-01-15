<template>
  <div class="bg-[#0f1117] border border-gray-800 rounded-md overflow-hidden my-4 relative group">
    <div class="flex justify-between items-center px-4 py-2 bg-[#161b22] border-b border-gray-800">
      <span class="text-[10px] font-mono text-gray-400 uppercase tracking-widest">{{ label }}</span>
      <button @click="copyCode" class="text-gray-400 hover:text-white transition">
        <svg
          v-if="!copied"
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
          />
        </svg>
        <span v-else class="text-[10px] font-bold text-green-400">COPIED!</span>
      </button>
    </div>
    <div class="p-4 overflow-x-auto">
      <pre class="text-sm font-mono text-blue-300 leading-relaxed"><code>{{ code }}</code></pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps(['code', 'label'])
const copied = ref(false)

const copyCode = () => {
  navigator.clipboard.writeText(props.code)
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}
</script>
