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
  loading.value = true
  errorMessage.value = ''

  try {
    user.value = await getCurrentUser()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Falha ao carregar usuário'
    router.push({ name: 'login' })
  } finally {
    loading.value = false
  }
}

onMounted(loadUser)
</script>

<template>
  <v-container class="home-page dsgov-shell" fluid>
    <v-card class="home-card dsgov-card">
      <v-card-title class="pb-2">
        <h1 class="dsgov-toolbar-title">Plataforma de Pedidos</h1>
        <p class="dsgov-toolbar-subtitle">Painel de operação integrado para usuários, catálogo e pedidos</p>
      </v-card-title>
      <v-card-text>
        <p v-if="loading">Carregando dados do usuário...</p>
        <v-alert v-else-if="errorMessage" type="error" variant="tonal">{{ errorMessage }}</v-alert>

        <div v-else-if="user" class="profile-grid">
          <div>
            <p class="label">Usuário</p>
            <p class="value">{{ user.full_name }}</p>
          </div>
          <div>
            <p class="label">E-mail</p>
            <p class="value">{{ user.email }}</p>
          </div>
        </div>

        <div class="home-actions">
          <v-btn color="primary" :to="{ name: 'orders' }">Ir para pedidos</v-btn>
          <v-btn variant="outlined" color="primary" :to="{ name: 'catalog' }">Abrir catálogo</v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<style scoped>
.home-page {
  min-height: calc(100vh - 84px);
  display: grid;
  align-items: start;
  padding: 1.5rem;
}

.home-card {
  width: min(100%, 680px);
  padding: 0.4rem;
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
  border: 1px solid #d9d9d9;
  border-radius: 12px;
  padding: 1rem;
  background: #f8f8f8;
}

.label {
  margin: 0;
  color: #495057;
  font-size: 0.86rem;
}

.value {
  margin: 0.18rem 0 0;
  font-size: 1rem;
  font-weight: 700;
}

.home-actions {
  margin-top: 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

@media (max-width: 700px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }

  .home-actions {
    flex-direction: column;
    align-items: stretch;
  }
}

</style>
