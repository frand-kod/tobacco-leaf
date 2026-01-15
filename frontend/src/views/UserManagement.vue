<template>
  <div class="wrapper">
    <TheNavbar />

    <div class="pt-20 pb-10 px-4 max-w-6xl mx-auto">
      <div class="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
        <div>
          <h2 class="text-2xl font-bold text-gray-800">User Management</h2>
          <p class="text-gray-500">Manage account access and user profiles</p>
        </div>
        <div
          class="bg-blue-50 text-blue-700 px-4 py-2 rounded-lg font-medium border border-blue-100"
        >
          Total Users: {{ users.length }}
        </div>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead class="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider">
              <tr>
                <th class="px-6 py-4 font-semibold">User Details</th>
                <th class="px-6 py-4 font-semibold">Email Address</th>
                <th class="px-6 py-4 font-semibold">Role</th>
                <th class="px-6 py-4 font-semibold text-center">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50 transition">
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div
                      class="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold"
                    >
                      {{ (user.name || 'U').charAt(0).toUpperCase() }}
                    </div>
                    <span class="font-normal text-gray-900">{{ user.name }}</span>
                  </div>
                </td>
                <td class="px-6 py-4 text-gray-600">
                  {{ user.email }}
                </td>
                <td class="px-6 py-4 text-gray-600">
                  {{ user.role }}
                </td>
                <td class="px-6 py-4">
                  <div class="flex justify-center gap-2">
                    <button
                      @click="openEditModal(user)"
                      class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition"
                      title="Edit User"
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
                          d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                        />
                      </svg>
                    </button>
                    <button
                      @click="handleDelete(user.id)"
                      class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition"
                      title="Delete User"
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
    </div>
    <EditUserModal
      v-if="showModal"
      :user="selectedUser"
      @close="showModal = false"
      @updated="fetchUsers"
    />
  </div>
  <TheFooter />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import TheNavbar from '../components/TheNavbar.vue'
import EditUserModal from '../components/EditUserModal.vue'
import TheFooter from '@/components/TheFooter.vue'
const users = ref([])
const showModal = ref(false)
const selectedUser = ref(null) // Digunakan sebagai props untuk modal

const fetchUsers = async () => {
  try {
    const res = await api.get('/user/list')
    users.value = res.data
  } catch (err) {
    console.error('Failed to fetch users')
  }
}

const openEditModal = (user) => {
  // PERBAIKAN: Isi selectedUser, bukan editForm
  selectedUser.value = { ...user }
  showModal.value = true
}

const handleDelete = async (userId) => {
  if (!confirm('Are you sure you want to delete this user?')) return
  try {
    await api.delete(`/user/${userId}`)
    await fetchUsers()
  } catch (err) {
    alert('Delete failed')
  }
}

// Fungsi updateUser sudah tidak dibutuhkan di sini
// karena logikanya sudah pindah ke dalam komponen EditUserModal.vue

onMounted(fetchUsers)
</script>
