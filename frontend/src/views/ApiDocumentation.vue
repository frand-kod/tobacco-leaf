<template>
  <div class="min-h-screen bg-white">
    <TheNavbar />

    <DocSearch :endpoints="allEndpoints" ref="searchRef" />

    <div class="max-w-[1440px] mx-auto flex">
      <aside
        class="w-72 fixed h-[calc(100vh-64px)] top-16 border-r border-gray-100 overflow-y-auto bg-white py-8 px-6 hidden lg:block"
      >
        <button
          @click="openSearchModal"
          class="w-full flex items-center gap-3 px-3 py-2 mb-8 bg-gray-50 border border-gray-200 rounded-md text-gray-400 hover:border-gray-300 transition-all text-sm"
        >
          <svg
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
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
          <span class="flex-1 text-left">Search...</span>
          <span class="text-[10px] font-mono border border-gray-200 px-1 rounded bg-white"
            >Ctrl K</span
          >
        </button>

        <div v-for="section in docStructure" :key="section.title" class="mb-8">
          <h4
            class="text-[11px] font-bold text-gray-900 uppercase tracking-widest mb-4 flex items-center gap-2"
          >
            <span class="w-1 h-1 bg-blue-600 rounded-full"></span>
            {{ section.title }}
          </h4>
          <ul class="space-y-1">
            <li v-for="item in section.items" :key="item.id">
              <a
                :href="'#' + item.id"
                class="text-[13px] text-gray-600 hover:text-blue-600 hover:bg-blue-50/50 px-2 py-1.5 rounded-md block transition-all"
              >
                {{ item.name }}
              </a>
            </li>
          </ul>
        </div>
      </aside>

      <main class="flex-1 lg:ml-72 flex flex-col xl:flex-row min-w-0">
        <div class="flex-1 p-8 lg:p-12 xl:max-w-3xl">
          <div class="mb-16">
            <div class="flex items-center gap-2 text-blue-600 mb-4 text-sm font-medium">
              <span
                class="px-2 py-0.5 bg-blue-50 rounded text-[10px] font-bold uppercase tracking-wider"
                >Docs</span
              >
              <span>/</span>
              <span>API Reference</span>
            </div>
            <h1 class="text-4xl font-bold text-gray-900 tracking-tighter mb-6">API Tembakau</h1>
            <p class="text-gray-600 leading-relaxed text-base">
              Gunakan endpoint kami untuk mengidentifikasi penyakit pada daun tembakau secara
              otomatis. API kami dirancang untuk kecepatan dan akurasi tinggi menggunakan model visi
              komputer terbaru.
            </p>
          </div>

          <section v-for="group in apiGroups" :key="group.id" :id="group.id" class="mb-20">
            <h2 class="text-2xl font-bold text-gray-900 mb-8 border-b border-gray-100 pb-4">
              {{ group.title }}
            </h2>

            <div
              v-for="ep in group.endpoints"
              :key="ep.slug"
              :id="ep.slug"
              class="mb-16 scroll-mt-24"
            >
              <div class="flex items-center gap-3 mb-4">
                <span
                  :class="methodColor(ep.method)"
                  class="px-2 py-0.5 text-[10px] font-bold border rounded uppercase"
                >
                  {{ ep.method }}
                </span>
                <code
                  class="text-sm font-mono font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded"
                  >{{ ep.path }}</code
                >
              </div>
              <h3 class="text-xl font-bold text-gray-900 mb-3">{{ ep.name }}</h3>
              <p class="text-gray-600 text-[14px] leading-relaxed mb-6">{{ ep.details }}</p>

              <div class="xl:hidden space-y-4 mb-8">
                <DocCodeBlock label="Request Body" :code="JSON.stringify(ep.params, null, 2)" />
                <DocCodeBlock label="Response" :code="JSON.stringify(ep.response, null, 2)" />
              </div>
            </div>
          </section>
        </div>

        <div
          class="hidden xl:block w-[400px] border-l border-gray-100 p-8 h-screen sticky top-16 bg-gray-50/30 overflow-y-auto"
        >
          <div v-for="group in apiGroups" :key="'code-' + group.id">
            <div v-for="ep in group.endpoints" :key="'code-' + ep.slug" class="mb-20">
              <h4 class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-4">
                Example Implementation
              </h4>
              <DocCodeBlock label="cURL Request" :code="generateCurl(ep)" />
              <DocCodeBlock label="Success Response" :code="JSON.stringify(ep.response, null, 2)" />
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import TheNavbar from '@/components/TheNavbar.vue'
import DocCodeBlock from '@/components/Documentation/DocCodeBlock.vue'
import DocSearch from '@/components/Documentation/DocSearch.vue'

// Data & Logic (sama seperti sebelumnya, pastikan data sinkron)
const apiGroups = [
  {
    title: 'Model Inference',
    id: 'inference',
    description: 'Endpoint inti untuk pengolahan citra daun.',
    endpoints: [
      {
        slug: 'predict-leaf',
        name: 'Analyze Leaf Condition',
        method: 'POST',
        path: '/model/predict',
        details: 'Mengirimkan gambar daun untuk mendapatkan hasil analisis kesehatan.',
        params: { file: 'binary image file' },
        response: { label: 'Mosaic Virus', confidence: 0.98 },
      },
    ],
  },
]

const docStructure = [
  { title: 'Inference API', items: [{ name: 'Predict Leaf', id: 'predict-leaf' }] },
]

const searchRef = ref(null)
const allEndpoints = computed(() => apiGroups.flatMap((group) => group.endpoints))

const openSearchModal = () => searchRef.value?.openSearch()

const methodColor = (m) => {
  const colors = {
    GET: 'text-blue-600 border-blue-200 bg-blue-50',
    POST: 'text-emerald-600 border-emerald-200 bg-emerald-50',
  }
  return colors[m] || 'text-gray-600 border-gray-200 bg-gray-50'
}

const generateCurl = (ep) => `curl -X ${ep.method} "https://api.tobacco.com${ep.path}"`
</script>
