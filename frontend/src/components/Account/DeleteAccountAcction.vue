<template>
  <div class="space-y-8">
    <h3 class="text-[11px] font-bold text-red-500 uppercase tracking-[0.2em]">Danger Management</h3>

    <div
      class="flex flex-col md:flex-row md:items-start justify-between gap-8 pb-8 border-b border-gray-100"
    >
      <div class="max-w-md">
        <p class="text-[15px] font-bold text-gray-900 mb-2">Delete Account Registry</p>
        <p class="text-[14px] text-gray-500 leading-relaxed font-normal">
          Tindakan ini akan menghapus seluruh data klasifikasi tembakau dan preferensi akun Anda
          dari basis data kami secara permanen.
        </p>
      </div>
      <button
        @click="confirmDelete"
        class="w-full md:w-auto px-6 py-2 border border-red-200 text-red-600 text-[11px] font-bold uppercase tracking-widest rounded-sm hover:bg-red-50 transition-all"
      >
        Execute Delete
      </button>
    </div>
  </div>
</template>

<script setup>
import api from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()

const confirmDelete = async () => {
  if (confirm('Apakah Anda yakin ingin menghapus akun? Semua data akan hilang selamanya.')) {
    try {
      const userId = localStorage.getItem('user_id')
      await api.delete(`/user/${userId}`)

      // Cleanup
      localStorage.clear()
      alert('Akun telah dihapus.')
      router.push('/login')
    } catch (err) {
      alert('Gagal menghapus akun. Silakan coba lagi.')
    }
  }
}
</script>
