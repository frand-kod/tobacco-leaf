import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', component: () => import('../views/Login.vue') },
    { path: '/register', component: () => import('../views/Register.vue') },
    { path: '/dashboard', component: () => import('../views/Dashboard.vue') },
    { path: '/users', component: () => import('../views/UserManagement.vue') },
    { path: '/profile', component: () => import('../views/Profile.vue') },
    { path: '/docs', component: () => import('../views/ApiDocumentation.vue') },
    { path: '/', redirect: '/login' },
  ],
})

export default router
