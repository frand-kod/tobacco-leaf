<template>
  <div v-if="isOpen" class="fixed inset-0 z-[10000] flex items-start justify-center pt-[15vh] px-4">
    <div class="absolute inset-0 bg-gray-900/20 backdrop-blur-[2px]" @click="closeSearch"></div>

    <div
      class="relative w-full max-w-xl bg-white shadow-2xl border border-gray-200 rounded-md overflow-hidden"
    >
      <div class="flex items-center px-4 border-b border-gray-100">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        <input
          v-model="query"
          ref="searchInput"
          type="text"
          placeholder="Search documentation..."
          class="w-full p-4 focus:outline-none text-gray-800 text-sm"
          @keydown.esc="closeSearch"
        />
        <span
          class="text-[10px] font-bold text-gray-400 bg-gray-50 px-1.5 py-0.5 border border-gray-200 rounded-sm"
          >ESC</span
        >
      </div>

      <div v-if="filteredResults.length > 0" class="max-h-80 overflow-y-auto p-2">
        <a
          v-for="item in filteredResults"
          :key="item.slug"
          :href="'#' + item.slug"
          @click="closeSearch"
          class="flex items-center justify-between p-3 hover:bg-blue-50 group transition-colors rounded-sm"
        >
          <div class="flex flex-col">
            <span class="text-xs font-bold text-gray-900">{{ item.name }}</span>
            <span class="text-[10px] text-gray-400 font-mono italic">{{ item.path }}</span>
          </div>
          <span
            class="text-[10px] font-bold uppercase text-blue-600 opacity-0 group-hover:opacity-100 transition"
            >Jump to →</span
          >
        </a>
      </div>

      <div v-else-if="query" class="p-8 text-center text-gray-400 text-sm">
        No results found for "{{ query }}"
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps(['endpoints'])
const isOpen = ref(false)
const query = ref('')
const searchInput = ref(null)

const filteredResults = computed(() => {
  if (!query.value) return []
  return props.endpoints.filter(
    (ep) =>
      ep.name.toLowerCase().includes(query.value.toLowerCase()) ||
      ep.path.toLowerCase().includes(query.value.toLowerCase()),
  )
})

const openSearch = () => {
  isOpen.value = true
  nextTick(() => searchInput.value?.focus())
}

const closeSearch = () => {
  isOpen.value = false
  query.value = ''
}

// Shortcut Handler
const handleKeydown = (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault()
    openSearch()
  }
}

onMounted(() => window.addEventListener('keydown', handleKeydown))
onUnmounted(() => window.removeEventListener('keydown', handleKeydown))

defineExpose({ openSearch })
</script>
