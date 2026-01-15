<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
    <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex items-center gap-5">
      <div class="h-12 w-12 rounded-xl bg-blue-50 flex items-center justify-center text-blue-600">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
      </div>
      <div>
        <p class="text-sm text-gray-400 font-medium uppercase tracking-wider">Total Analysis</p>
        <h3 class="text-2xl font-semibold text-gray-800 tracking-tight">{{ total }}</h3>
      </div>
    </div>

    <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex items-center gap-5">
      <div
        class="h-12 w-12 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-600"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M13 10V3L4 14h7v7l9-11h-7z"
          />
        </svg>
      </div>
      <div>
        <p class="text-sm text-gray-400 font-medium uppercase tracking-wider">Latest Status</p>
        <h3 class="text-xl font-semibold text-gray-800 truncate max-w-[150px]">
          {{ latest || 'No Data' }}
        </h3>
      </div>
    </div>

    <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex items-center gap-5">
      <div
        class="h-12 w-12 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </div>
      <div>
        <p class="text-sm text-gray-400 font-medium uppercase tracking-wider">Avg. Confidence</p>
        <h3 class="text-2xl font-semibold text-gray-800 tracking-tight">{{ average }}%</h3>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  reports: {
    type: Array,
    required: true,
  },
})

const total = computed(() => props.reports.length)

const latest = computed(() => {
  return props.reports.length > 0 ? props.reports[0].label : null
})

const average = computed(() => {
  if (props.reports.length === 0) return 0
  const sum = props.reports.reduce((acc, curr) => acc + curr.confidence, 0)
  return (sum / props.reports.length).toFixed(1)
})
</script>
