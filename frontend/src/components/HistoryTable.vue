<template>
  <div class="bg-white border-t border-gray-100 antialiased px-4">
    <div class="py-8 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
      <div>
        <h2 class="text-[12px] font-bold text-gray-400 uppercase tracking-[0.2em] mb-1">
          Database
        </h2>
        <h3 class="text-3xl font-extrabold text-gray-900 tracking-tighter">Prediction History</h3>
      </div>

      <div class="flex items-center gap-3">
        <Transition name="fade">
          <button
            v-if="selectedIds.length > 0"
            @click="handleBatchDownload"
            class="px-5 py-2.5 bg-blue-600 text-white text-[12px] font-bold uppercase tracking-widest rounded-sm hover:bg-black transition-all flex items-center gap-2 shadow-lg shadow-blue-100"
          >
            Download ({{ selectedIds.length }}) Selected
          </button>
        </Transition>

        <button
          @click="$emit('refresh')"
          class="p-2.5 text-gray-400 hover:text-blue-600 hover:rotate-180 transition-all duration-700"
        ></button>
      </div>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr
            class="text-[11px] font-bold text-gray-400 uppercase tracking-widest border-b border-gray-50"
          >
            <th class="pb-5 w-10">
              <input
                type="checkbox"
                @change="toggleSelectAll"
                :checked="isAllSelected"
                class="w-4 h-4 rounded-sm border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
              />
            </th>
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
            :class="{ 'bg-blue-50/50': selectedIds.includes(report.id) }"
          >
            <td class="py-6 px-2">
              <input
                type="checkbox"
                v-model="selectedIds"
                :value="report.id"
                class="w-4 h-4 rounded-sm border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
              />
            </td>

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
              <div class="flex justify-end gap-2">
                <td class="py-6">
                  <div class="flex justify-end gap-1">
                    <button
                      @click="handleDownload(report.id)"
                      class="p-2.5 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-sm transition-all group/btn"
                      title="Download PDF Report"
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
                          d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                        />
                      </svg>
                    </button>

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
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import api from '../api'

const props = defineProps({
  reports: { type: Array, default: () => [] },
})
const emit = defineEmits(['refresh'])

const selectedIds = ref([])

// Checkbox Logic
const isAllSelected = computed(() => {
  return props.reports.length > 0 && selectedIds.value.length === props.reports.length
})

const toggleSelectAll = (e) => {
  if (e.target.checked) {
    selectedIds.value = props.reports.map((r) => r.id)
  } else {
    selectedIds.value = []
  }
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

// Download Individual
const handleDownload = async (id) => {
  try {
    const response = await api.get(`/reports/${id}/download`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `report-${id}.pdf`)
    link.click()
  } catch (err) {
    alert('Download failed')
  }
}

// BATCH DOWNLOAD LOGIC
const handleBatchDownload = async () => {
  if (selectedIds.value.length === 0) return

  try {
    // Biasanya backend akan menerima list ID dan mengembalikan file .zip
    const response = await api.post(
      '/reports/batch-download',
      { ids: selectedIds.value },
      { responseType: 'blob' },
    )

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `tobacco-reports-batch.zip`)
    link.click()

    // Clear selection after success
    selectedIds.value = []
  } catch (err) {
    alert('Batch download failed. Make sure backend supports ZIP generation.')
  }
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

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
