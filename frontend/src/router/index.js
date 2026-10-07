import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', component: () => import('../views/Login.vue') },
    { path: '/register', component: () => import('../views/Register.vue') },
    { path: '/dashboard', component: () => import('../views/Dashboard.vue') },
    { path: '/users', component: () => import('../views/UserManagement.vue') },
    { path: '/profile', component: () => import('../views/Profile.vue') },
    { path: '/', redirect: '/login' },
  ],
})

const publicPaths = ['/login', '/register']

router.beforeEach((to) => {
  const token = localStorage.getItem('token')
  if (!token && !publicPaths.includes(to.path)) return '/login'
  if (token && publicPaths.includes(to.path)) return '/dashboard'
  if (to.path === '/users' && localStorage.getItem('user_role') !== 'admin') return '/dashboard'
})

export default router
