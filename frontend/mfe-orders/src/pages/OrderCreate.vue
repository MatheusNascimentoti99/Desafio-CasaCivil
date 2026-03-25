<script setup lang="ts">
import { reactive, ref } from 'vue'
import type { CreateOrderPayload } from '../types/order'
import { createOrder } from '../services'

const emit = defineEmits<{
  created: []
}>()

const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const form = reactive<CreateOrderPayload>({
  customer_name: '',
  items: [
    {
      product_name: '',
      quantity: 1,
      unit_price: 0,
    },
  ],
})

function addItem() {
  form.items.push({
    product_name: '',
    quantity: 1,
    unit_price: 0,
  })
}

function removeItem(index: number) {
  if (form.items.length === 1) {
    return
  }

  form.items.splice(index, 1)
}

function resetForm() {
  form.customer_name = ''
  form.items = [
    {
      product_name: '',
      quantity: 1,
      unit_price: 0,
    },
  ]
}

async function submitOrder() {
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const payload: CreateOrderPayload = {
      customer_name: form.customer_name.trim(),
      items: form.items.map((item) => ({
        product_name: item.product_name.trim(),
        quantity: Number(item.quantity),
        unit_price: Number(item.unit_price),
      })),
    }

    await createOrder(payload)
    successMessage.value = 'Pedido criado com sucesso.'
    resetForm()
    emit('created')
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Erro ao criar pedido'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="order-create">
    <h3>Criar pedido</h3>

    <form class="order-form" @submit.prevent="submitOrder">
      <label class="field">
        <span>Nome do cliente</span>
        <input
          v-model="form.customer_name"
          type="text"
          minlength="2"
          maxlength="255"
          required
          placeholder="Ex: Maria Silva"
        >
      </label>

      <div class="items-header">
        <h4>Itens</h4>
        <button type="button" class="secondary-btn" @click="addItem">Adicionar item</button>
      </div>

      <div v-for="(item, index) in form.items" :key="index" class="item-row">
        <label class="field grow">
          <span>Produto</span>
          <input
            v-model="item.product_name"
            type="text"
            minlength="2"
            maxlength="255"
            required
            placeholder="Nome do produto"
          >
        </label>

        <label class="field small">
          <span>Qtd.</span>
          <input
            v-model.number="item.quantity"
            type="number"
            min="1"
            step="1"
            required
          >
        </label>

        <label class="field medium">
          <span>Valor unit.</span>
          <input
            v-model.number="item.unit_price"
            type="number"
            min="0"
            step="0.01"
            required
          >
        </label>

        <button
          type="button"
          class="danger-btn"
          :disabled="form.items.length === 1"
          @click="removeItem(index)"
        >
          Remover
        </button>
      </div>

      <button class="primary-btn" type="submit" :disabled="loading">
        {{ loading ? 'Criando...' : 'Criar pedido' }}
      </button>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </form>
  </section>
</template>

<style scoped>
.order-create {
  border: 1px solid #ececec;
  border-radius: 12px;
  padding: 1rem;
  background: #fff;
}

.order-form {
  display: grid;
  gap: 0.75rem;
}

.items-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.item-row {
  display: grid;
  grid-template-columns: 1fr 90px 140px auto;
  gap: 0.5rem;
  align-items: end;
}

.field {
  display: grid;
  gap: 0.25rem;
}

.field input {
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 0.5rem;
}

.primary-btn,
.secondary-btn,
.danger-btn {
  border: 1px solid transparent;
  border-radius: 6px;
  padding: 0.45rem 0.8rem;
  cursor: pointer;
}

.primary-btn {
  background: #0c6cf2;
  color: #fff;
}

.secondary-btn {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.danger-btn {
  background: #fff5f5;
  border-color: #fecaca;
  color: #b91c1c;
}

.error {
  color: #b00020;
}

.success {
  color: #0f7b0f;
}

@media (max-width: 900px) {
  .item-row {
    grid-template-columns: 1fr;
  }
}
</style>
