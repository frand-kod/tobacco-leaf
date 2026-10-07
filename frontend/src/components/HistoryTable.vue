<template>
  <div class="bg-white border-t border-gray-100 antialiased px-4">
    <div class="py-8 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
      <div>
        <h2 class="text-[12px] font-bold text-gray-400 uppercase tracking-[0.2em] mb-1">
          Database
        </h2>
        <h3 class="text-3xl font-extrabold text-gray-900 tracking-tighter">Prediction History</h3>
      </div>

    </div>

    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr
            class="text-[11px] font-bold text-gray-400 uppercase tracking-widest border-b border-gray-50"
          >
            <th class="pb-5 font-bold">Preview</th>
            <th class="pb-5 font-bold">Result / Confidence</th>
            <th class="pb-5 font-bold">Date</th>
            <th class="pb-5 font-bold text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-50">
          <tr
            v-for="report in reports"
            :key="report.id"
            class="group transition-colors odd:bg-white even:bg-gray-100 hover:bg-blue-100 border-sm mx-2"
          >
            <td class="py-6">
              <div
                class="h-16 w-16 rounded-sm bg-gray-50 overflow-hidden border border-gray-100 group-hover:border-gray-200 transition-all"
              >
                <img
                  :src="report.image_path"
                  class="h-full w-full object-cover grayscale-[30%] group-hover:grayscale-0"
                />
              </div>
            </td>

            <td class="py-6">
              <p class="text-[16px] font-extrabold text-gray-900 mb-2 uppercase tracking-tight">
                {{ report.label }}
              </p>
              <div class="flex items-center gap-4">
                <div class="w-32 bg-gray-100 h-[3px]">
                  <div
                    class="bg-blue-600 h-full transition-all duration-1000"
                    :style="{ width: report.confidence + '%' }"
                  ></div>
                </div>
                <span class="text-[20px] font-mono font-black text-blue-600">
                  {{ report.confidence.toFixed(1) }}%
                </span>
              </div>
            </td>

            <td class="py-6">
              <span class="text-base text-gray-500 font-bold tabular-nums">
                {{ formatDate(report.created_at) }}
              </span>
            </td>

            <td class="py-6">
              <div class="flex justify-end gap-1">
                <button
                  @click="handleDelete(report.id)"
                  class="p-2.5 text-gray-600 hover:text-red-500 hover:bg-red-50 rounded-sm transition-all"
                  title="Delete Record"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import api from '../api'

defineProps({
  reports: { type: Array, default: () => [] },
})
const emit = defineEmits(['refresh'])

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

const handleDelete = async (id) => {
  if (!confirm('Hapus data?')) return
  try {
    await api.delete(`/reports/${id}`)
    emit('refresh')
  } catch (err) {
    alert('Delete failed')
  }
}
</script>
