<template>
  <div class="min-h-screen bg-white font-sans selection:bg-blue-500">
    <TheNavbar />

    <main class="pt-32 pb-20 px-6 max-w-5xl mx-auto antialiased tracking-tight">
      <section
        class="flex flex-col md:flex-row items-center gap-10 mb-12 pb-12 border-b border-gray-300"
      >
        <div
          class="h-28 w-28 rounded-md bg-gray-100 flex items-center justify-center text-3xl font-bold text-blue-600 border border-gray-100"
        >
          {{ (user.name || 'U').charAt(0).toUpperCase() }}
        </div>

        <div class="text-center md:text-left flex-1">
          <div class="flex flex-col md:flex-row md:items-center gap-3 mb-1">
            <h1 class="text-4xl text-gray-900 tracking-tighter">
              {{ user.name }}
            </h1>
            <span
              class="w-fit mx-auto md:mx-0 px-2 py-0.5 rounded-sm text-[10px] font-bold uppercase tracking-[0.2em] border border-blue-100 bg-blue-50/50 text-blue-600"
            >
              {{ user.role }}
            </span>
          </div>
          <p class="text-lg text-gray-500 font-normal">{{ user.email }}</p>
        </div>

        <div class="flex gap-3">
          <button
            @click="showEditModal = true"
            class="px-6 py-2 rounded-sm bg-gray-900 text-white text-xs font-bold uppercase tracking-widest hover:bg-black transition-all border border-gray-900"
          >
            Update Profile
          </button>
        </div>
      </section>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
        <aside class="lg:col-span-3 space-y-10">
          <div class="pb-10 border-b lg:border-b-0 border-gray-300">
            <h4 class="text-[11px] font-bold text-gray-400 uppercase tracking-[0.2em] mb-6">
              Account Overview
            </h4>
            <div class="space-y-6">
              <div>
                <span class="text-[11px] uppercase text-gray-400 font-bold block mb-1"
                  >Total Analysis</span
                >
                <span class="text-2xl font-bold font-mono text-gray-900 tracking-tighter">
                  {{ stats.totalPredictions.toString().padStart(2, '0') }}
                </span>
              </div>
              <div>
                <span class="text-[11px] uppercase text-gray-400 font-bold block mb-1"
                  >Joined Since</span
                >
                <span class="text-base font-semibold text-gray-800 tracking-tight">
                  {{ formatDate(user.created_at) }}
                </span>
              </div>
            </div>
          </div>
        </aside>

        <div class="lg:col-span-9 lg:pl-12 lg:border-l lg:border-gray-300 space-y-16">
          <section>
            <h3 class="text-[11px] font-bold text-gray-400 uppercase tracking-[0.2em] mb-8">
              System & Security
            </h3>
            <div class="flex items-start gap-6 group">
              <div class="mt-1 h-5 w-5 text-emerald-500 shrink-0">
                <svg fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                  />
                </svg>
              </div>
              <div class="pb-8 border-b border-gray-100 w-full">
                <p class="text-[15px] font-bold text-gray-900 mb-1">Verified Session Access</p>
                <p class="text-[14px] text-gray-500 leading-relaxed max-w-md">
                  Sesi Anda saat ini diamankan dengan enkripsi end-to-end dan validasi token JWT
                  yang aktif.
                </p>
              </div>
            </div>
          </section>

          <section>
            <DeleteAccountAction />
          </section>
        </div>
      </div>
    </main>

    <EditUserModal
      v-if="showEditModal"
      :user="user"
      @close="showEditModal = false"
      @updated="fetchProfile"
    />
    <TheFooter />
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import TheNavbar from '@/components/TheNavbar.vue'
import TheFooter from '@/components/TheFooter.vue'
import EditUserModal from '@/components/EditUserModal.vue'
import DeleteAccountAction from '@/components/Account/DeleteAccountAcction.vue' // Impor komponen hapus

const user = ref({ name: '', email: '', role: '', created_at: '' })
const stats = ref({ totalPredictions: 0 })
const showEditModal = ref(false)

const fetchProfile = async () => {
  const userId = localStorage.getItem('user_id')
  try {
    const [userRes, reportsRes] = await Promise.all([
      api.get(`/user/${userId}`),
      api.get('/reports'), // Ambil total laporan untuk statistik
    ])
    user.value = userRes.data
    stats.value.totalPredictions = reportsRes.data.length
  } catch (err) {
    console.error('Gagal mengambil data profil')
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'Desember 2023' // Fallback
  const options = { year: 'numeric', month: 'long' }
  return new Date(dateString).toLocaleDateString('id-ID', options)
}

onMounted(fetchProfile)
</script>
