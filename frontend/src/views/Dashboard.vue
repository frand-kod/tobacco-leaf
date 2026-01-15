<template>
  <div class="wrapper min-h-screen bg-[#fafafa]">
    <TheNavbar />

    <main class="pt-24 pb-10 px-4 lg:px-8 max-w-[1600px] mx-auto">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <aside class="lg:col-span-4 xl:col-span-3 lg:sticky lg:top-24">
          <div class="space-y-6">
            <Predictor @success="fetchReports" />
          </div>
        </aside>

        <section class="lg:col-span-8 xl:col-span-9 space-y-6">
          <div>
            <StatsOverview :reports="reports" />
          </div>

          <div class="bg-white border border-gray-100 p-1 lg:p-6 rounded-sm">
            <HistoryTable :reports="reports" @refresh="fetchReports" />
          </div>
        </section>
      </div>
    </main>

    <TheFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import TheNavbar from '@/components/TheNavbar.vue'
import Predictor from '@/components/Predictor.vue'
import HistoryTable from '@/components/HistoryTable.vue'
import StatsOverview from '@/components/StatsOverview.vue'
import TheFooter from '@/components/TheFooter.vue'

const reports = ref([])

const fetchReports = async () => {
  try {
    const res = await api.get('/reports')
    reports.value = res.data
  } catch (err) {
    console.error('Failed to load reports')
  }
}

onMounted(fetchReports)
</script>
