<template>
  <div
    class="min-h-screen flex flex-col lg:flex-row-reverse bg-white selection:bg-blue-100 antialiased"
  >
    <LoadingOverlay :show="isLoading" />

    <div
      class="w-full lg:w-[45%] flex items-center justify-center p-8 md:p-16 border-l border-gray-100"
    >
      <div class="max-w-sm w-full">
        <div class="mb-10 text-center lg:text-left">
          <div
            class="w-10 h-10 bg-blue-600 rounded-sm mb-6 mx-auto lg:mx-0 flex items-center justify-center text-white font-bold"
          >
            T
          </div>
          <h2 class="text-3xl font-extrabold text-gray-900 tracking-tighter mb-2">
            Create Registry
          </h2>
          <p class="text-[13px] text-gray-500 uppercase tracking-widest font-medium">
            Daftar untuk akses diagnosa AI
          </p>
        </div>

        <form @submit.prevent="handleRegister" class="space-y-5">
          <BaseInput v-model="form.name" label="Full Name" placeholder="Nama Lengkap" required />
          <BaseInput
            v-model="form.email"
            label="Email Address"
            type="email"
            placeholder="name@tobacco.ai"
            required
          />
          <BaseInput
            v-model="form.password"
            label="Password"
            type="password"
            placeholder="••••••••"
            required
          />

          <div class="pt-4">
            <button
              class="w-full bg-gray-900 text-white py-3.5 rounded-sm text-xs font-bold uppercase tracking-[0.3em] hover:bg-black transition-all border border-gray-900"
            >
              Complete Registration
            </button>
          </div>
        </form>

        <p
          class="mt-12 text-center lg:text-left text-xs text-gray-400 uppercase tracking-widest font-bold"
        >
          Sudah punya akun?
          <router-link to="/login" class="text-blue-600 hover:text-black transition-colors ml-2"
            >Authorize Access</router-link
          >
        </p>
      </div>
    </div>

    <div
      class="hidden lg:flex w-[55%] bg-[#0a0a0a] relative overflow-hidden items-center justify-center"
    >
      <div class="absolute inset-0 opacity-20 pointer-events-none">
        <div
          class="absolute top-0 left-0 w-full h-full bg-[radial-gradient(#1e1e1e_1px,transparent_1px)] [background-size:20px_20px]"
        ></div>
      </div>

      <div class="relative z-10 p-16 max-w-2xl text-center">
        <h3 class="text-4xl font-extrabold text-white tracking-tighter mb-6 leading-tight">
          Join the Global <br />
          <span class="text-blue-500">Tobacco Intelligence</span>
        </h3>
        <p class="text-gray-400 font-mono text-sm tracking-tight mb-8">
          // Connecting farmers with neural networks for optimal crop selection.
        </p>
        <div class="flex justify-center gap-2">
          <div class="w-2 h-2 rounded-full bg-blue-600"></div>
          <div class="w-2 h-2 rounded-full bg-gray-800"></div>
          <div class="w-2 h-2 rounded-full bg-gray-800"></div>
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
import LoadingOverlay from '@/components/LoadingOverlay.vue'

const router = useRouter()
const isLoading = ref(false)
const form = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: '', // Tambahkan untuk konfirmasi password
})

const handleRegister = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    alert('Password dan konfirmasi password tidak cocok!')
    return
  }

  isLoading.value = true
  try {
    await api.post('/auth/register', {
      name: form.value.name,
      email: form.value.email,
      password: form.value.password,
    })
    alert('Registrasi berhasil! Silakan login.')
    router.push('/login')
  } catch (err) {
    const errorMsg = err.response?.data?.detail || 'Registrasi gagal. Coba lagi.'
    alert(errorMsg)
    console.error('Error detail:', err.response?.data)
  } finally {
    setTimeout(() => {
      isLoading.value = false
    }, 300)
  }
}
</script>
