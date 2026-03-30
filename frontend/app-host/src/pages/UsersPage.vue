<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { listUsers } from '@/services/auth'
import type { UserResponse } from '@/types/auth'

const router = useRouter()
const users = ref<UserResponse[]>([])
const loading = ref(false)
const errorMessage = ref('')
const search = ref('')
const filterActive = ref<string | null>(null)

const headers = [
  { title: 'Nome', key: 'full_name', sortable: true },
  { title: 'E-mail', key: 'email', sortable: true },
  { title: 'Status', key: 'is_active', sortable: true },
  { title: 'Criado em', key: 'created_at', sortable: true },
]

async function load() {
  loading.value = true
  errorMessage.value = ''

  try {
    users.value = await listUsers()
  } catch (err) {
    errorMessage.value = err instanceof Error ? err.message : 'Falha ao carregar usuários'
    router.push({ name: 'login' })
  } finally {
    loading.value = false
  }
}

const filteredUsers = computed(() => {
  let result = users.value

  if (filterActive.value !== null) {
    const isActive = filterActive.value === 'active'
    result = result.filter((u) => u.is_active === isActive)
  }

  if (search.value.trim()) {
    const q = search.value.toLowerCase()
    result = result.filter(
      (u) =>
        u.full_name.toLowerCase().includes(q) ||
        u.email.toLowerCase().includes(q),
    )
  }

  return result
})

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(load)
</script>

<template>
  <v-container fluid class="users-page dsgov-shell">
    <div class="page-header mb-6">
      <div>
        <h1 class="dsgov-page-title">Usuários</h1>
        <p class="dsgov-page-subtitle">
          Gerencie todos os usuários cadastrados na plataforma
        </p>
      </div>
      <v-chip class="users-count" color="primary" variant="tonal" size="small" rounded="pill">
        {{ filteredUsers.length }} {{ filteredUsers.length === 1 ? 'usuário' : 'usuários' }}
      </v-chip>
    </div>

    <v-card class="mb-4 dsgov-card">
      <v-card-text class="pa-3">
        <v-row align="center" no-gutters>
          <v-col cols="12" sm="7" class="pe-sm-3 mb-3 mb-sm-0">
            <v-text-field
              v-model="search"
              prepend-inner-icon="mdi-magnify"
              placeholder="Buscar por nome ou e-mail..."
              variant="outlined"
              density="compact"
              hide-details
              clearable
              rounded="lg"
            />
          </v-col>
          <v-col cols="12" sm="5">
            <v-btn-toggle
              v-model="filterActive"
              color="primary"
              variant="outlined"
              divided
              density="compact"
              rounded="lg"
              class="w-100"
            >
              <v-btn :value="null" class="flex-1-1">Todos</v-btn>
              <v-btn value="active" class="flex-1-1">Ativos</v-btn>
              <v-btn value="inactive" class="flex-1-1">Inativos</v-btn>
            </v-btn-toggle>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-4" rounded="lg">
      {{ errorMessage }}
    </v-alert>

    <v-card class="dsgov-card">
      <v-data-table
        :headers="headers"
        :items="filteredUsers"
        :loading="loading"
        loading-text="Carregando usuários..."
        no-data-text="Nenhum usuário encontrado"
        hover
        class="users-table"
      >
        <template #item.full_name="{ item }">
          <div class="d-flex align-center gap-3 py-1">
            <v-avatar color="primary" size="36" variant="tonal">
              <span>
                {{ item.full_name.charAt(0) }}
              </span>
            </v-avatar>
            <span class="font-weight-medium ml-2">{{ item.full_name }}</span>
          </div>
        </template>

        <template #item.is_active="{ item }">
          <v-chip
            :color="item.is_active ? 'success' : 'error'"
            variant="tonal"
            size="small"
            :prepend-icon="item.is_active ? 'mdi-check-circle' : 'mdi-close-circle'"
          >
            {{ item.is_active ? 'Ativo' : 'Inativo' }}
          </v-chip>
        </template>

        <template #item.created_at="{ item }">
          <span class="text-medium-emphasis text-body-2">{{ formatDate(item.created_at) }}</span>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<style scoped>
.users-page {
  max-width: 1100px;
  margin: 0 auto;
  padding-top: 0.5rem;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.users-count {
  margin-top: 4px;
}

.users-table :deep(thead th) {
  background: #f0f4fa;
  color: #1351b4;
  font-weight: 700;
}

.users-table :deep(tbody tr:hover) {
  background: #f8fbff;
}

@media (max-width: 700px) {
  .page-header {
    flex-direction: column;
    gap: 0.65rem;
  }
}

</style>
