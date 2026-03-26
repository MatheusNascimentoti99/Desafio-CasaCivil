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

const currencyFormatter = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

function formatCurrency(value: number | undefined) {
  return currencyFormatter.format(value ?? 0)
}

function statusColor(status: string) {
  const normalized = status.toLowerCase()

  if (normalized === 'completed' || normalized === 'paid') {
    return 'success'
  }

  if (normalized === 'pending') {
    return 'warning'
  }

  if (normalized === 'cancelled' || normalized === 'canceled') {
    return 'error'
  }

  return 'info'
}

function orderTotal(order: Order) {
  if (typeof order.total === 'number') {
    return order.total
  }

  return order.items.reduce((sum, item) => sum + item.quantity * item.unit_price, 0)
}

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
        <div class="d-flex align-center ga-2">
          <v-icon icon="mdi-package-variant-closed" color="primary" />
          <span>Pedidos (MFE)</span>
        </div>
        <div class="d-flex ga-2">
          <v-btn variant="outlined" prepend-icon="mdi-refresh" @click="refreshOrders">Atualizar</v-btn>
          <v-btn color="primary" @click="activeView = activeView === 'list' ? 'create' : 'list'">
            <v-icon start :icon="activeView === 'list' ? 'mdi-plus-circle-outline' : 'mdi-format-list-bulleted'" />
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
              <v-card variant="outlined" class="order-card">
                <v-card-title class="d-flex justify-space-between align-center pb-1">
                  <div class="d-flex align-center ga-2">
                    <v-icon icon="mdi-account-circle-outline" color="primary" />
                    <span>{{ order.customer_name }}</span>
                  </div>
                  <v-chip size="small" :color="statusColor(order.status)" variant="tonal">
                    <v-icon start icon="mdi-progress-clock" />
                    {{ order.status }}
                  </v-chip>
                </v-card-title>

                <v-card-text>
                  <div class="d-flex align-center ga-2 mb-3 text-medium-emphasis">
                    <v-icon icon="mdi-cash-multiple" size="18" />
                    <span>Total: <strong>{{ formatCurrency(orderTotal(order)) }}</strong></span>
                  </div>

                  <div class="d-flex align-center ga-2 mb-2">
                    <v-icon icon="mdi-format-list-bulleted-square" size="18" color="primary" />
                    <strong>Itens</strong>
                  </div>

                  <v-list class="py-0" density="compact" bg-color="transparent">
                    <v-list-item
                      v-for="(item, index) in order.items"
                      :key="index"
                      class="item-row"
                      rounded="lg"
                    >
                      <template #prepend>
                        <v-icon icon="mdi-cube-outline" size="18" class="mr-2" />
                      </template>

                      <v-list-item-title class="item-title">{{ item.product_name }}</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-icon icon="mdi-counter" size="14" class="mr-1" />
                        {{ item.quantity }}
                        <span class="mx-1">•</span>
                        <v-icon icon="mdi-currency-brl" size="14" class="mr-1" />
                        {{ formatCurrency(item.unit_price) }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <v-alert v-if="orders.length === 0" type="info" variant="tonal">
            Nenhum pedido encontrado.
          </v-alert>

          <div class="pagination">
            <v-btn variant="outlined" prepend-icon="mdi-chevron-left" :disabled="!hasPreviousPage" @click="goToPreviousPage">
              Anterior
            </v-btn>
            <span>Página {{ currentPage }}</span>
            <v-btn color="primary" append-icon="mdi-chevron-right" :disabled="!hasNextPage" @click="goToNextPage">
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

.order-card {
  border-left: 4px solid rgb(var(--v-theme-primary));
}

.item-row {
  border: 1px solid rgba(0, 0, 0, 0.08);
  margin-bottom: 0.4rem;
}

.item-title {
  font-weight: 500;
}
</style>
