<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { CreateOrderPayload } from '../types/order'
import { createOrder } from '../services'

const router = useRouter()

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
      product_ean: '',
      quantity: 1,
    },
  ],
})

function addItem() {
  form.items.push({
    product_ean: '',
    quantity: 1,
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
      product_ean: '',
      quantity: 1,
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
        product_ean: item.product_ean.trim(),
        quantity: Number(item.quantity),
      })),
    }

    await createOrder(payload)
    successMessage.value = 'Pedido criado com sucesso.'
    resetForm()
    emit('created')
    await router.push({ name: 'orders' })
  } catch (error) {
    errorMessage.value = "Erro ao criar pedido. Verifique os dados e tente novamente."
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-card>
    <v-card-title class="d-flex align-center ga-2">
      <v-btn icon="mdi-arrow-left" variant="text" @click="router.push({ name: 'orders' })" />
      <span>Criar pedido</span>
    </v-card-title>
    <v-card-text>
      <v-form class="order-form" @submit.prevent="submitOrder">
        <v-text-field
          v-model="form.customer_name"
          label="Nome do cliente"
          maxlength="255"
          required
          variant="outlined"
          placeholder="Ex: Maria Silva"
        />

        <div class="items-header">
          <h4>Itens</h4>
          <v-btn variant="outlined" @click="addItem">Adicionar item</v-btn>
        </div>

        <div v-for="(item, index) in form.items" :key="index" class="item-row">
          <v-text-field
            v-model="item.product_ean"
            label="EAN do produto"
            maxlength="14"
            required
            variant="outlined"
            placeholder="Ex: 7894900011517"
            hideDetails="auto"
          />

          <v-text-field
            v-model.number="item.quantity"
            label="Qtd."
            type="number"
            min="1"
            step="1"
            required
            variant="outlined"
            hideDetails="auto"
          />

          <v-btn
            color="error"
            variant="text"
            :disabled="form.items.length === 1"
            @click="removeItem(index)"
          >
            Remover
          </v-btn>
        </div>

        <v-btn color="primary" type="submit" :loading="loading">
          {{ loading ? 'Criando...' : 'Criar pedido' }}
        </v-btn>

        <v-alert v-if="errorMessage" type="error" variant="tonal">{{ errorMessage }}</v-alert>
        <v-alert v-if="successMessage" type="success" variant="tonal">{{ successMessage }}</v-alert>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<style scoped>
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
  grid-template-columns: minmax(0, 1fr) 120px auto;
  gap: 0.5rem;
  align-items: center;
}

@media (max-width: 900px) {
  .item-row {
    grid-template-columns: 1fr;
  }
}
</style>
