<template>
  <LoadingOverlay :show="isLoggingOut" />

  <nav
    class="bg-white/80 backdrop-blur-md border-b border-gray-100 fixed w-full z-50 top-0 antialiased selection:bg-blue-50"
  >
    <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
      <div class="flex items-center gap-8">
        <router-link to="/dashboard" class="flex items-center gap-2 group">
          <div
            class="w-8 h-8 bg-blue-600 rounded-sm flex items-center justify-center text-white font-bold group-hover:bg-black transition-colors"
          >
            T
          </div>
          <span class="text-sm font-extrabold tracking-[0.2em] uppercase text-gray-900">
            Tobacco<span class="text-blue-600">AI</span>
          </span>
        </router-link>

        <div class="hidden md:flex items-center gap-1">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            class="px-4 py-2 text-[11px] font-bold uppercase tracking-widest transition-all rounded-sm"
            :class="[
              $route.path === link.path
                ? 'text-blue-600 bg-blue-50/50'
                : 'text-gray-500 hover:text-gray-900 hover:bg-gray-50',
            ]"
          >
            {{ link.name }}
            <span
              v-if="link.badge"
              class="ml-1 text-[9px] px-1 border border-blue-200 text-blue-500 rounded-sm uppercase tracking-tighter"
            >
              {{ link.badge }}
            </span>
          </router-link>
        </div>
      </div>

      <div class="flex items-center gap-6">
        <router-link to="/profile" class="flex items-center gap-3 group">
          <div class="text-right hidden sm:block">
            <p
              class="text-[10px] font-bold text-gray-400 uppercase tracking-widest leading-none mb-1"
            >
              Login As
            </p>
            <p
              class="text-md font-normal text-gray-900 leading-none group-hover:text-blue-600 transition-colors"
            >
              {{ userName }}
            </p>
          </div>
          <div
            class="h-8 w-8 rounded-sm bg-gray-100 flex items-center justify-center text-xs font-bold text-gray-600 border border-gray-200 group-hover:border-blue-400 transition-all"
          >
            {{ userName.charAt(0).toUpperCase() }}
          </div>
        </router-link>

        <button
          @click="handleLogout"
          class="p-2 text-gray-400 hover:text-red-500 transition-colors"
          title="Logout Session"
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
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
            />
          </svg>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import LoadingOverlay from '@/components/LoadingOverlay.vue' // Import overlay Anda

const router = useRouter()
const isLoggingOut = ref(false)
const role = localStorage.getItem('user_role')
const userName = localStorage.getItem('user_role') || 'User'

const navLinks = computed(() => {
  const links = [
    { name: 'Dashboard', path: '/dashboard' },
    { name: 'Docs', path: '/docs', badge: 'API' },
  ]
  if (role === 'admin') {
    links.push({ name: 'User Management', path: '/users' })
  }
  return links
})

const handleLogout = () => {
  isLoggingOut.value = true

  // Memberikan waktu bagi overlay untuk muncul dan transisi halaman terasa smooth
  setTimeout(() => {
    localStorage.clear()
    router.push('/login')
  }, 800)
}
</script>
