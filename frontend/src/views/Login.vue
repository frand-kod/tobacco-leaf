<template>
  <div class="min-h-screen flex bg-white selection:bg-blue-100 antialiased">
    <LoadingOverlay :show="isLoading" />

    <div class="w-full lg:w-[45%] flex items-center justify-center p-8 md:p-16">
      <div class="max-w-sm w-full">
        <div class="mb-10 text-center lg:text-left">
          <div
            class="w-10 h-10 bg-blue-600 rounded-sm mb-6 mx-auto lg:mx-0 flex items-center justify-center text-white font-bold"
          >
            T
          </div>
          <h2 class="text-3xl font-bold text-gray-900 tracking-tighter mb-2">Welcome Back</h2>
          <p class="text-[13px] text-gray-500 uppercase tracking-widest font-medium">
            Masuk untuk memulai analisa AI
          </p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <BaseInput
            v-model="form.email"
            label="Email Registry"
            type="email"
            placeholder="name@tobacco.ai"
            required
            class="text-sm"
          />

          <div class="space-y-1">
            <BaseInput
              v-model="form.password"
              label="Secure Password"
              type="password"
              placeholder="••••••••"
              required
            />
            <div class="flex justify-end">
              <a
                href="#"
                class="text-[11px] font-bold text-blue-600 uppercase tracking-tighter hover:underline"
                >Forgot?</a
              >
            </div>
          </div>

          <div class="pt-4">
            <button
              :disabled="isLoading"
              class="w-full bg-gray-900 text-white py-3.5 rounded-sm text-xs font-bold uppercase tracking-[0.3em] hover:bg-black transition-all border border-gray-900 disabled:opacity-50"
            >
              Authorize Access
            </button>
          </div>
        </form>

        <p
          class="mt-12 text-center lg:text-left text-xs text-gray-400 uppercase tracking-widest font-bold"
        >
          New Explorer?
          <router-link to="/register" class="text-blue-600 hover:text-black transition-colors ml-2">
            Create Registry
          </router-link>
        </p>
      </div>
    </div>

    <div
      class="hidden lg:flex w-[55%] bg-[#0a0a0a] relative overflow-hidden items-center justify-center border-l border-gray-800"
    >
      <div class="absolute inset-0 opacity-20 pointer-events-none">
        <div
          class="absolute top-0 left-0 w-full h-full bg-[radial-gradient(#1e1e1e_1px,transparent_1px)] [background-size:20px_20px]"
        ></div>
      </div>

      <div class="relative z-10 p-16 max-w-2xl text-center">
        <h3 class="text-4xl font-extrabold text-white tracking-tighter mb-6 leading-tight">
          Smarter Analysis for <br />
          <span class="text-blue-500">Premium Tobacco Quality</span>
        </h3>

        <div class="flex justify-center gap-4 mb-8">
          <div
            class="px-3 py-1 border border-gray-700 rounded-sm text-[10px] text-gray-400 font-mono tracking-widest uppercase bg-gray-900/50"
          >
            AI Engine v1.0.4
          </div>
          <div
            class="px-3 py-1 border border-blue-900 rounded-sm text-[10px] text-blue-400 font-mono tracking-widest uppercase bg-blue-900/20"
          >
            Edge Computing
          </div>
        </div>

        <div class="bg-gray-900/50 border border-gray-800 p-6 rounded-md text-left font-mono">
          <p class="text-emerald-400 text-sm mb-2 font-bold">// Quality Validation Result</p>
          <p class="text-gray-400 text-xs leading-relaxed">
            "Sistem AI Tobacco secara signifikan mempercepat waktu inspeksi kualitas daun sebesar
            85% dengan akurasi klasifikasi mencapai 98.4%."
          </p>
          <div class="mt-4 flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-gray-700"></div>
            <div>
              <p class="text-white text-[11px] font-bold">Research Labs</p>
              <p class="text-gray-500 text-[10px]">Technical Review 2026</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import BaseInput from '../components/BaseInput.vue'
import BaseButton from '../components/BaseButton.vue'
import LoadingOverlay from '@/components/LoadingOverlay.vue'

const router = useRouter()
const isLoading = ref(false)

const form = ref({
  email: '',
  password: '',
})

const handleLogin = async () => {
  isLoading.value = true
  try {
    const res = await api.post('/auth/login', form.value)

    // Menyimpan data autentikasi
    localStorage.setItem('token', res.data.access_token)
    localStorage.setItem('user_id', res.data.user.id)
    localStorage.setItem('user_role', res.data.user.role)

    // Opsional: Gunakan toast alih-alih alert agar UX lebih smooth
    router.push('/dashboard')
  } catch (err) {
    // Menangkap pesan error spesifik dari backend jika ada
    const errorMsg = err.response?.data?.detail || 'Login gagal: Periksa email/password'
    alert(errorMsg)
    console.error('Error detail:', err.response?.data)
  } finally {
    // Beri sedikit delay agar transisi overlay terasa halus
    setTimeout(() => {
      isLoading.value = false
    }, 300)
  }
}
</script>
