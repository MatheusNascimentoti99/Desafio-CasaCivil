<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { listOrders, updateOrderStatus } from '../services'
import type { Order, OrderStatus } from '../types/order'

const loading = ref(false)
const updatingOrderId = ref<string | null>(null)
const errorMessage = ref('')
const actionErrorMessage = ref('')
const orders = ref<Order[]>([])
const currentPage = ref(1)
const pageSize = 5
const hasNextPage = ref(false)
const hasPreviousPage = computed(() => currentPage.value > 1)
const selectedStatus = ref<OrderStatus | null>(null)

const statusOptions: Array<{ label: string; value: OrderStatus }> = [
  { label: 'Pendente', value: 'pendente' },
  { label: 'Confirmado', value: 'confirmado' },
  { label: 'Enviado', value: 'enviado' },
  { label: 'Entregue', value: 'entregue' },
  { label: 'Cancelado', value: 'cancelado' },
]

const currencyFormatter = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

function formatCurrency(value: number | undefined) {
  return currencyFormatter.format(value ?? 0)
}

function statusColor(status: OrderStatus) {
  if (status === 'entregue') {
    return 'success'
  }

  if (status === 'pendente') {
    return 'warning'
  }

  if (status === 'cancelado') {
    return 'error'
  }

  return 'info'
}

function nextStatus(status: OrderStatus): OrderStatus | null {
  if (status === 'pendente') {
    return 'confirmado'
  }

  if (status === 'confirmado') {
    return 'enviado'
  }

  if (status === 'enviado') {
    return 'entregue'
  }

  return null
}

function nextStatusLabel(status: OrderStatus): string {
  if (status === 'pendente') {
    return 'Confirmar'
  }

  if (status === 'confirmado') {
    return 'Marcar como enviado'
  }

  if (status === 'enviado') {
    return 'Marcar como entregue'
  }

  return 'Avançar status'
}

function canCancel(status: OrderStatus): boolean {
  return status !== 'entregue' && status !== 'cancelado'
}

async function changeStatus(order: Order, targetStatus: OrderStatus) {
  if (updatingOrderId.value || order.status === 'cancelado') {
    return
  }

  updatingOrderId.value = order.id
  actionErrorMessage.value = ''

  try {
    const updated = await updateOrderStatus(order.id, targetStatus)
    const idx = orders.value.findIndex((item) => item.id === order.id)
    if (idx >= 0) {
      orders.value[idx] = updated
    }
  } catch (error) {
    actionErrorMessage.value = error instanceof Error ? error.message : 'Erro ao atualizar status'
  } finally {
    updatingOrderId.value = null
  }
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
    const results = await listOrders({
      skip,
      limit: pageSize + 1,
      status: selectedStatus.value ?? undefined,
    })
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

async function applyStatusFilter(status: OrderStatus | null) {
  selectedStatus.value = status
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
          <v-select
            :model-value="selectedStatus"
            :items="statusOptions"
            item-title="label"
            item-value="value"
            label="Filtrar por status"
            variant="outlined"
            density="compact"
            clearable
            hide-details
            style="min-width: 220px"
            @update:model-value="applyStatusFilter"
          />
          <v-btn variant="outlined" prepend-icon="mdi-refresh" @click="refreshOrders">Atualizar</v-btn>
          <v-btn color="primary" :to="{ name: 'order-create' }">
            <v-icon start icon="mdi-plus-circle-outline" />
            Novo pedido
          </v-btn>
        </div>
      </v-card-title>

      <v-card-text>
        <div v-if="loading" class="loading-state">
          <v-progress-circular indeterminate color="primary" />
          <span>Carregando pedidos...</span>
        </div>

        <v-alert v-else-if="errorMessage" type="error" variant="tonal">
          {{ errorMessage }}
        </v-alert>

        <template v-else>
          <v-alert v-if="actionErrorMessage" type="error" variant="tonal" class="mb-4">
            {{ actionErrorMessage }}
          </v-alert>
          <v-alert v-if="orders.length === 0" type="info" variant="tonal">
            Nenhum pedido encontrado.
          </v-alert>
          <v-row v-else>
            <v-col v-for="order in orders" :key="order.id" cols="12">
              <v-card class="order-card">
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

                      <v-list-item-title class="item-title">EAN {{ item.product_ean }}</v-list-item-title>
                      <v-list-item-subtitle>
                        <v-icon icon="mdi-counter" size="14" class="mr-1" />
                        {{ item.quantity }}
                        <span class="mx-1">•</span>
                        <v-icon icon="mdi-currency-brl" size="14" class="mr-1" />
                        {{ formatCurrency(item.unit_price) }}
                      </v-list-item-subtitle>
                    </v-list-item>
                  </v-list>

                  <v-divider class="my-3" />

                  <div class="d-flex flex-wrap ga-2">
                    <v-btn
                      v-if="nextStatus(order.status)"
                      color="primary"
                      variant="tonal"
                      size="small"
                      :loading="updatingOrderId === order.id"
                      :disabled="updatingOrderId !== null"
                      @click="changeStatus(order, nextStatus(order.status) as OrderStatus)"
                    >
                      <v-icon start icon="mdi-arrow-right-bold-circle-outline" />
                      {{ nextStatusLabel(order.status) }}
                    </v-btn>

                    <v-btn
                      v-if="canCancel(order.status)"
                      color="error"
                      variant="outlined"
                      size="small"
                      :loading="updatingOrderId === order.id"
                      :disabled="updatingOrderId !== null"
                      @click="changeStatus(order, 'cancelado')"
                    >
                      <v-icon start icon="mdi-cancel" />
                      Cancelar pedido
                    </v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

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
