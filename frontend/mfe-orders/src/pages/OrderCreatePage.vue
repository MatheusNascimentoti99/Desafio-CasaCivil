<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { CreateOrderPayload } from '../types/order'
import { createOrder, listCatalogProducts } from '../services'
import type { CatalogProduct } from '../types/catalog'

const router = useRouter()

const emit = defineEmits<{
  created: []
}>()

const loading = ref(false)
const loadingCatalog = ref(false)
const catalogErrorMessage = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const catalogProducts = ref<CatalogProduct[]>([])

const productOptions = computed(() =>
  catalogProducts.value.map((product) => ({
    title: `${product.name} (${product.ean})`,
    value: product.ean,
  })),
)

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

async function loadCatalogProducts() {
  loadingCatalog.value = true
  catalogErrorMessage.value = ''

  try {
    catalogProducts.value = await listCatalogProducts({ limit: 50 })
  } catch (error) {
    catalogErrorMessage.value =
      error instanceof Error ? error.message : 'Falha ao carregar catálogo de produtos'
  } finally {
    loadingCatalog.value = false
  }
}

async function submitOrder() {
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  if (form.items.some((item) => !item.product_ean)) {
    errorMessage.value = 'Selecione um produto para todos os itens.'
    loading.value = false
    return
  }

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

onMounted(loadCatalogProducts)
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

        <v-alert v-if="catalogErrorMessage" type="error" variant="tonal">
          {{ catalogErrorMessage }}
        </v-alert>

        <div v-for="(item, index) in form.items" :key="index" class="item-row">
          <v-autocomplete
            v-model="item.product_ean"
            :items="productOptions"
            :loading="loadingCatalog"
            label="Produto"
            required
            variant="outlined"
            placeholder="Selecione um produto"
            hideDetails="auto"
            clearable
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
