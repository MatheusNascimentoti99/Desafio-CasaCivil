<script setup lang="ts">
import { onMounted, ref } from 'vue'
import OrderCreate from './OrderCreate.vue'
import { listOrders } from '../services'
import type { Order } from '../types/order'

const loading = ref(false)
const errorMessage = ref('')
const orders = ref<Order[]>([])
const activeView = ref<'list' | 'create'>('list')

async function loadOrders() {
  loading.value = true
  errorMessage.value = ''

  try {
    orders.value = await listOrders()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Erro ao carregar pedidos'
  } finally {
    loading.value = false
  }
}

async function handleOrderCreated() {
  activeView.value = 'list'
  await loadOrders()
}

onMounted(loadOrders)
</script>

<template>
  <div class="orders-app">
    <header class="orders-header">
      <h2>Pedidos (MFE)</h2>
      <div class="actions">
        <button class="refresh-btn" type="button" @click="loadOrders">Atualizar</button>
        <button
          class="create-btn"
          type="button"
          @click="activeView = activeView === 'list' ? 'create' : 'list'"
        >
          {{ activeView === 'list' ? 'Novo pedido' : 'Ver pedidos' }}
        </button>
      </div>
    </header>

    <OrderCreate v-if="activeView === 'create'" @created="handleOrderCreated" />

    <p v-else-if="loading">Carregando pedidos...</p>
    <p v-else-if="errorMessage" class="error">{{ errorMessage }}</p>

    <ul v-else class="orders-list">
      <li v-for="order in orders" :key="order.id" class="order-card">
        <div><strong>Cliente:</strong> {{ order.customer_name }}</div>
        <div><strong>Status:</strong> {{ order.status }}</div>
        <div><strong>Itens:</strong>
          <ul class="items-list">
            <li v-for="(item, index) in order.items" :key="index">
              {{ item.product_name }} - Quantidade: {{ item.quantity }} - Preço unitário: R$ {{ item.unit_price.toFixed(2) }}
            </li>
          </ul>
        </div>
      </li>
      <li v-if="orders.length === 0" class="empty">Nenhum pedido encontrado.</li>
    </ul>
  </div>
</template>

<style scoped>
.orders-app {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1rem;
  background: #fff;
}

.orders-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.refresh-btn {
  border: 1px solid #c7c7c7;
  background: #f5f5f5;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  cursor: pointer;
}

.create-btn {
  border: 1px solid #0c6cf2;
  background: #0c6cf2;
  color: #fff;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  cursor: pointer;
}

.orders-list {
  list-style: none;
  padding: 0;
  margin: 1rem 0 0;
  display: grid;
  gap: 0.75rem;
}

.order-card {
  border: 1px solid #ececec;
  border-radius: 8px;
  padding: 0.75rem;
}

.error {
  color: #b00020;
}

.empty {
  color: #666;
}
</style>
