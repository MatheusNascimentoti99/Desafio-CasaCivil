<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getCurrentUser } from '@/services/auth'
import type { UserResponse } from '@/types/auth'

const router = useRouter()
const user = ref<UserResponse | null>(null)
const loading = ref(false)
const errorMessage = ref('')

async function loadUser() {
  const token = localStorage.getItem('auth_token')

  if (!token) {
    router.push({ name: 'login' })
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    user.value = await getCurrentUser(token)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Falha ao carregar usuário'
    localStorage.removeItem('auth_token')
    router.push({ name: 'login' })
  } finally {
    loading.value = false
  }
}

function logout() {
  localStorage.removeItem('auth_token')
  router.push({ name: 'login' })
}

onMounted(loadUser)
</script>

<template>
  <main class="home-page">
    <section class="home-card">
      <h1>Plataforma de Pedidos</h1>
      <p v-if="loading">Carregando dados do usuário...</p>
      <p v-else-if="errorMessage" class="home-error">{{ errorMessage }}</p>

      <div v-else-if="user">
        <p><strong>Usuário:</strong> {{ user.full_name }}</p>
        <p><strong>E-mail:</strong> {{ user.email }}</p>
      </div>

      <div class="home-actions">
        <RouterLink class="orders-link" :to="{ name: 'orders' }">Abrir módulo de pedidos</RouterLink>
        <BrButton @click="logout">Sair</BrButton>
      </div>
    </section>
  </main>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 1.5rem;
}

.home-card {
  width: min(100%, 560px);
  border: 1px solid var(--gray-20, #d9d9d9);
  border-radius: 12px;
  padding: 1.5rem;
  background: #fff;
}

.home-actions {
  margin-top: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.orders-link {
  color: #1351b4;
  font-weight: 600;
}

.home-error {
  color: #b00020;
}
</style>
