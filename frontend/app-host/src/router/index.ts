import { createRouter, createWebHistory } from 'vue-router'
import AuthLayout from '@/components/AuthLayout.vue'
import HomePage from '@/pages/HomePage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import RegisterPage from '@/pages/RegisterPage.vue'
import UsersPage from '@/pages/UsersPage.vue'
import MainLayout from '@/components/MainLayout.vue'
import { defineAsyncComponent } from 'vue'
import { getSession } from '@/services/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: MainLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '/home',
          alias: '',
          name: 'home',
          component: HomePage,
          meta: { requiresAuth: true },
        },
        {
          path: '/users',
          name: 'users',
          component: UsersPage,
          meta: { requiresAuth: true },
        },
        {
          path: '/orders',
          name: 'orders',
          component: defineAsyncComponent(() => import('orders/OrdersList')),
          meta: { requiresAuth: true },
        },
        {
          path: '/orders/create',
          name: 'order-create',
          component: defineAsyncComponent(() => import('orders/OrderCreate')),
          meta: { requiresAuth: true },
        }
      ]
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
    // Redirect any unknown route to home
    {
      path: '/:pathMatch(.*)*',
      redirect: { name: 'home' }
    }
  ],
})

router.beforeEach(async (to) => {
  if (!to.meta.requiresAuth && !to.meta.guestOnly) {
    return true
  }

  let hasSession = false

  try {
    await getSession()
    hasSession = true
  } catch {
    hasSession = false
  }

  if (to.meta.requiresAuth && !hasSession) {
    return { name: 'login' }
  }

  if (to.meta.guestOnly && hasSession) {
    return { name: 'home' }
  }

  return true
})

export default router
