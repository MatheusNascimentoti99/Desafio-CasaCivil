import { createRouter, createWebHistory } from 'vue-router'
import AuthLayout from '@/components/AuthLayout.vue'
import HomePage from '@/pages/HomePage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import OrdersRemotePage from '@/pages/OrdersRemotePage.vue'
import RegisterPage from '@/pages/RegisterPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
      meta: { requiresAuth: true },
    },
    {
      path: '/orders',
      name: 'orders',
      component: OrdersRemotePage,
      meta: { requiresAuth: true },
    },
    {
      path: '/auth',
      component: AuthLayout,
      meta: { guestOnly: true },
      children: [
        {
          path: 'login',
          alias: '/login',
          name: 'login',
          component: LoginPage,
        },
        {
          path: 'register',
          alias: '/register',
          name: 'register',
          component: RegisterPage,
        },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const token = localStorage.getItem('auth_token')

  if (to.meta.requiresAuth && !token) {
    return { name: 'login' }
  }

  if (to.meta.guestOnly && token) {
    return { name: 'home' }
  }

  return true
})

export default router
