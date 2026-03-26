<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import OrderCreate from './OrderCreate.vue'
import { listOrders } from '../services'
import type { Order } from '../types/order'

const loading = ref(false)
const errorMessage = ref('')
const orders = ref<Order[]>([])
const activeView = ref<'list' | 'create'>('list')
const currentPage = ref(1)
const pageSize = 5
const hasNextPage = ref(false)
const hasPreviousPage = computed(() => currentPage.value > 1)

async function loadOrders() {
  loading.value = true
  errorMessage.value = ''

  try {
    const skip = (currentPage.value - 1) * pageSize
    const results = await listOrders({ skip, limit: pageSize + 1 })
    hasNextPage.value = results.length > pageSize
    orders.value = hasNextPage.value ? results.slice(0, pageSize) : results
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Erro ao carregar pedidos'
    hasNextPage.value = false
  } finally {
    loading.value = false
  }
}

async function goToNextPage() {
  if (!hasNextPage.value || loading.value) {
    return
  }

  currentPage.value += 1
  await loadOrders()
}

async function goToPreviousPage() {
  if (!hasPreviousPage.value || loading.value) {
    return
  }

  currentPage.value -= 1
  await loadOrders()
}

async function refreshOrders() {
  await loadOrders()
}

async function handleOrderCreated() {
  activeView.value = 'list'
  currentPage.value = 1
  await loadOrders()
}

onMounted(loadOrders)
</script>

<template>
  <v-container fluid class="pa-0">
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>Pedidos (MFE)</span>
        <div class="d-flex ga-2">
          <v-btn variant="outlined" @click="refreshOrders">Atualizar</v-btn>
          <v-btn color="primary" @click="activeView = activeView === 'list' ? 'create' : 'list'">
            {{ activeView === 'list' ? 'Novo pedido' : 'Ver pedidos' }}
          </v-btn>
        </div>
      </v-card-title>

      <v-card-text>
        <OrderCreate v-if="activeView === 'create'" @created="handleOrderCreated" />

        <div v-else-if="loading" class="loading-state">
          <v-progress-circular indeterminate color="primary" />
          <span>Carregando pedidos...</span>
        </div>

        <v-alert v-else-if="errorMessage" type="error" variant="tonal">
          {{ errorMessage }}
        </v-alert>

        <template v-else>
          <v-row>
            <v-col v-for="order in orders" :key="order.id" cols="12">
              <v-card variant="outlined">
                <v-card-text>
                  <div><strong>Cliente:</strong> {{ order.customer_name }}</div>
                  <div><strong>Status:</strong> {{ order.status }}</div>
                  <div>
                    <strong>Itens:</strong>
                    <ul class="items-list">
                      <li v-for="(item, index) in order.items" :key="index">
                        {{ item.product_name }} - Quantidade: {{ item.quantity }} - Preço unitário: R$ {{ item.unit_price.toFixed(2) }}
                      </li>
                    </ul>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <v-alert v-if="orders.length === 0" type="info" variant="tonal">
            Nenhum pedido encontrado.
          </v-alert>

          <div class="pagination">
            <v-btn variant="outlined" :disabled="!hasPreviousPage" @click="goToPreviousPage">
              Anterior
            </v-btn>
            <span>Página {{ currentPage }}</span>
            <v-btn color="primary" :disabled="!hasNextPage" @click="goToNextPage">
              Próxima
            </v-btn>
          </div>
        </template>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<style scoped>
.loading-state {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.pagination {
  margin-top: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.items-list {
  margin: 0.5rem 0 0;
  padding-left: 1rem;
}
</style>
