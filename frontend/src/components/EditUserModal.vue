<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
    <div
      class="bg-white rounded-2xl max-w-md w-full shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200"
    >
      <div class="p-6 border-b border-gray-100 flex justify-between items-center">
        <h3 class="text-xl font-bold text-gray-800">Edit User Profile</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">&times;</button>
      </div>

      <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
        <BaseInput v-model="localUser.name" label="Full Name" required />
        <BaseInput v-model="localUser.email" label="Email Address" type="email" required />

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Role</label>
          <select
            v-model="localUser.role"
            class="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
          >
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <div class="flex gap-3 pt-4">
          <BaseButton
            type="button"
            variant="secondary"
            @click="$emit('close')"
            class="bg-gray-100 text-gray-700 hover:bg-gray-200"
          >
            Cancel
          </BaseButton>
          <BaseButton :loading="loading">Update User</BaseButton>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import api from '../api'
import BaseInput from './BaseInput.vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  user: { type: Object, required: true },
})

const emit = defineEmits(['close', 'updated'])

const loading = ref(false)
// Gunakan ref lokal agar tidak mengubah data di parent sebelum disave (reactive copy)
const localUser = ref({ ...props.user })

const handleSubmit = async () => {
  loading.value = true
  try {
    await api.put(`/user/${localUser.value.id}`, {
      name: localUser.value.name,
      email: localUser.value.email,
      role: localUser.value.role,
    })
    emit('updated') // Beritahu parent untuk refresh data
    emit('close') // Tutup modal
  } catch (err) {
    alert('Update failed: ' + (err.response?.data?.detail || 'Unknown error'))
  } finally {
    loading.value = false
  }
}
</script>
