<template>
  <div class="bg-white border border-gray-100 p-6 mb-6 antialiased">
    <div class="flex justify-between items-end mb-8">
      <div>
        <h2 class="text-[11px] font-bold text-gray-400 uppercase tracking-[0.2em] mb-2">
          AI Diagnostic Tool
        </h2>
        <h1 class="text-3xl text-bold text-gray-900 tracking-tighter">Analisa Daun Tembakau</h1>
      </div>
    </div>

    <div
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      :class="[
        'relative border border-dashed p-12 transition-all duration-300 text-center rounded-sm',
        isDragging
          ? 'border-green-500 bg-blue-50/50 scale-[0.99]'
          : 'border-gray-200 hover:border-gray-400',
      ]"
    >
      <input
        type="file"
        @change="onFileChange"
        accept="image/*"
        class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        id="fileInput"
      />

      <div v-if="!previewUrl" class="space-y-4">
        <div class="text-gray-300 flex justify-center">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-12 w-12"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
        </div>
        <p class="text-gray-500 text-sm tracking-normal font-medium">
          Tarik gambar ke sini atau <span class="text-blue-600 font-bold">Pilih File</span>
        </p>
        <p class="text-[11px] text-gray-400 uppercase tracking-widest">RAW, JPG, PNG up to 10MB</p>
      </div>

      <div v-else class="flex flex-col items-center gap-6">
        <div class="relative group">
          <img
            :src="previewUrl"
            class="h-48 w-48 object-cover rounded-sm border border-gray-100 shadow-xl"
          />
          <div
            class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center rounded-sm"
          >
            <p class="text-white text-[10px] font-bold uppercase tracking-widest">Ganti Gambar</p>
          </div>
        </div>
        <div class="text-center">
          <p class="text-sm font-bold text-gray-800 font-mono tracking-tighter">
            {{ formatFileName(selectedFile?.name) }}
          </p>
          <button
            @click.stop="clearSelection"
            class="mt-2 text-red-500 text-[10px] font-bold uppercase tracking-[0.2em] hover:text-red-700 transition-colors"
          >
            Discard Image
          </button>
        </div>
      </div>
    </div>

    <div v-if="isPredicting" class="mt-8 space-y-2">
      <div class="flex justify-between items-end mb-1">
        <span class="text-[10px] font-bold text-blue-600 uppercase tracking-widest italic"
          >Running Neural Engine...</span
        >
        <span class="text-[10px] font-mono text-gray-400">Please wait</span>
      </div>
      <div class="w-full bg-gray-50 h-[2px] overflow-hidden">
        <div class="bg-blue-600 h-full animate-progress-strip"></div>
      </div>
    </div>

    <button
      v-else
      @click="handlePredict"
      :disabled="!selectedFile"
      class="w-full mt-8 bg-gray-900 text-white py-4 rounded-sm text-xs font-bold uppercase tracking-[0.3em] hover:bg-black disabled:bg-gray-100 disabled:text-gray-400 transition-all border border-gray-900"
    >
      Execute Analysis
    </button>

    <LoadingOverlay :show="isPredicting" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'
import LoadingOverlay from '@/components/LoadingOverlay.vue'

const emit = defineEmits(['success'])
const selectedFile = ref(null)
const previewUrl = ref(null)
const isPredicting = ref(false)
const isDragging = ref(false)
const lastAnalysisId = ref(null) // Menyimpan ID untuk download report

const formatFileName = (name) => {
  if (!name) return ''

  // Ambil ekstensi (misal: .jpg, .png)
  const extension = name.substring(name.lastIndexOf('.'))
  // Ambil nama tanpa ekstensi
  const baseName = name.substring(0, name.lastIndexOf('.'))
  if (baseName.length <= 7) {
    return name
  }
  // Ambil 10 karakter pertama + ... + ekstensi
  return baseName.substring(0, 7) + '...' + extension
}
const onFileChange = (e) => {
  const file = e.target.files[0]
  if (file) setupPreview(file)
}

const handleDrop = (e) => {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file && file.type.startsWith('image/')) setupPreview(file)
}

const setupPreview = (file) => {
  selectedFile.value = file
  previewUrl.value = URL.createObjectURL(file)
}

const clearSelection = () => {
  selectedFile.value = null
  previewUrl.value = null
}

const handlePredict = async () => {
  if (!selectedFile.value) return
  isPredicting.value = true

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    const res = await api.post('/model/predict', formData)
    lastAnalysisId.value = res.data.id // Asumsi API mengembalikan ID hasil
    emit('success')
    clearSelection()
  } catch (err) {
    console.error('Analysis failed')
  } finally {
    isPredicting.value = false
  }
}
</script>

<style scoped>
@keyframes progress-strip {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
.animate-progress-strip {
  width: 50%;
  animation: progress-strip 1.5s infinite linear;
}
</style>
