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

onMounted(loadUser)
</script>

<template>
  <v-container class="home-page" fluid>
    <v-card class="home-card" elevation="6">
      <v-card-title class="text-h5">Plataforma de Pedidos</v-card-title>
      <v-card-text>
        <p v-if="loading">Carregando dados do usuário...</p>
        <v-alert v-else-if="errorMessage" type="error" variant="tonal">{{ errorMessage }}</v-alert>

        <div v-else-if="user">
          <p><strong>Usuário:</strong> {{ user.full_name }}</p>
          <p><strong>E-mail:</strong> {{ user.email }}</p>
        </div>

        <div class="home-actions">
          <v-btn color="primary" :to="{ name: 'orders' }">Abrir módulo de pedidos</v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
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
  padding: 0.5rem;
}

.home-actions {
  margin-top: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

</style>
