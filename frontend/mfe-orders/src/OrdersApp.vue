<script setup lang="ts">
import { onMounted, ref } from 'vue'

interface OrderItem {
  product_name: string
  quantity: number
  unit_price: number
}

interface Order {
  id: string
  customer_name: string
  status: string
  total_amount?: number
  items?: OrderItem[]
}

const loading = ref(false)
const errorMessage = ref('')
const orders = ref<Order[]>([])

async function loadOrders() {
  loading.value = true
  errorMessage.value = ''

  try {
    const baseUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8080'
    const token = localStorage.getItem('auth_token')

    const response = await fetch(`${baseUrl}/api/orders/`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })

    if (!response.ok) {
      const body = await response.json().catch(() => ({}))
      throw new Error(body?.detail ?? 'Não foi possível carregar pedidos')
    }

    orders.value = (await response.json()) as Order[]
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Erro ao carregar pedidos'
  } finally {
    loading.value = false
  }
}

onMounted(loadOrders)
</script>

<template>
  <div class="orders-app">
    <header class="orders-header">
      <h2>Pedidos (MFE)</h2>
      <button class="refresh-btn" type="button" @click="loadOrders">Atualizar</button>
    </header>

    <p v-if="loading">Carregando pedidos...</p>
    <p v-else-if="errorMessage" class="error">{{ errorMessage }}</p>

    <ul v-else class="orders-list">
      <li v-for="order in orders" :key="order.id" class="order-card">
        <div><strong>Cliente:</strong> {{ order.customer_name }}</div>
        <div><strong>Status:</strong> {{ order.status }}</div>
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

.refresh-btn {
  border: 1px solid #c7c7c7;
  background: #f5f5f5;
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
