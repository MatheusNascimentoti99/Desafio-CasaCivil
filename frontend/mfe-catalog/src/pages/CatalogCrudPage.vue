<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import {
  createCatalogProduct,
  deleteCatalogProduct,
  listCatalogProducts,
  updateCatalogProduct,
} from '../services'
import type { CatalogProduct, CatalogProductPayload } from '../types/catalog'

const loading = ref(false)
const saving = ref(false)
const deletingEan = ref<string | null>(null)
const errorMessage = ref('')
const successMessage = ref('')
const products = ref<CatalogProduct[]>([])
const editingOriginalEan = ref<string | null>(null)

const form = reactive<CatalogProductPayload>({
  ean: '',
  name: '',
  unit_price: 0,
})

const formTitle = computed(() => (editingOriginalEan.value ? 'Editar produto' : 'Novo produto'))
const submitLabel = computed(() => (editingOriginalEan.value ? 'Salvar alterações' : 'Cadastrar produto'))

function resetForm() {
  form.ean = ''
  form.name = ''
  form.unit_price = 0
  editingOriginalEan.value = null
}

function toPayload(): CatalogProductPayload {
  return {
    ean: form.ean.trim(),
    name: form.name.trim(),
    unit_price: Number(form.unit_price),
  }
}

async function loadProducts() {
  loading.value = true
  errorMessage.value = ''

  try {
    products.value = await listCatalogProducts()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Erro ao carregar catálogo'
  } finally {
    loading.value = false
  }
}

async function submitProduct() {
  errorMessage.value = ''
  successMessage.value = ''

  const payload = toPayload()
  if (!payload.ean || !payload.name || payload.unit_price <= 0) {
    errorMessage.value = 'Preencha EAN, nome e preço válido.'
    return
  }

  saving.value = true

  try {
    if (editingOriginalEan.value) {
      await updateCatalogProduct(editingOriginalEan.value, payload)
      successMessage.value = 'Produto atualizado com sucesso.'
    } else {
      await createCatalogProduct(payload)
      successMessage.value = 'Produto criado com sucesso.'
    }

    await loadProducts()
    resetForm()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Erro ao salvar produto'
  } finally {
    saving.value = false
  }
}

function startEdit(product: CatalogProduct) {
  editingOriginalEan.value = product.ean
  form.ean = product.ean
  form.name = product.name
  form.unit_price = Number(product.unit_price)
}

async function removeProduct(product: CatalogProduct) {
  deletingEan.value = product.ean
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await deleteCatalogProduct(product.ean)
    successMessage.value = 'Produto removido com sucesso.'
    await loadProducts()

    if (editingOriginalEan.value === product.ean) {
      resetForm()
    }
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Erro ao remover produto'
  } finally {
    deletingEan.value = null
  }
}

onMounted(loadProducts)
</script>

<template>
  <v-container fluid class="pa-0 catalog-page">
    <v-row>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>{{ formTitle }}</v-card-title>
          <v-card-text>
            <v-form class="catalog-form" @submit.prevent="submitProduct">
              <v-text-field
                v-model="form.ean"
                label="EAN"
                maxlength="14"
                placeholder="Ex: 7894900011517"
                required
                variant="outlined"
              />

              <v-text-field
                v-model="form.name"
                label="Nome"
                maxlength="255"
                required
                variant="outlined"
              />

              <v-text-field
                v-model.number="form.unit_price"
                label="Preço unitário"
                type="number"
                min="0.01"
                step="0.01"
                required
                variant="outlined"
                prefix="R$"
              />

              <div class="form-actions">
                <v-btn color="primary" type="submit" :loading="saving">
                  {{ submitLabel }}
                </v-btn>
                <v-btn v-if="editingOriginalEan" variant="text" @click="resetForm">Cancelar</v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="8">
        <v-card>
          <v-card-title class="d-flex align-center justify-space-between">
            <span>Catálogo de produtos</span>
            <v-btn variant="outlined" prepend-icon="mdi-refresh" :loading="loading" @click="loadProducts">
              Atualizar
            </v-btn>
          </v-card-title>

          <v-card-text>
            <v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-3">
              {{ errorMessage }}
            </v-alert>
            <v-alert v-if="successMessage" type="success" variant="tonal" class="mb-3">
              {{ successMessage }}
            </v-alert>

            <v-table density="comfortable" hover>
              <thead>
                <tr>
                  <th>EAN</th>
                  <th>Produto</th>
                  <th class="text-right">Preço</th>
                  <th class="text-right">Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="loading">
                  <td colspan="4" class="text-center py-4">Carregando...</td>
                </tr>
                <tr v-else-if="products.length === 0">
                  <td colspan="4" class="text-center py-4">Nenhum produto cadastrado.</td>
                </tr>
                <tr v-for="product in products" :key="product.ean">
                  <td>{{ product.ean }}</td>
                  <td>{{ product.name }}</td>
                  <td class="text-right">R$ {{ Number(product.unit_price).toFixed(2) }}</td>
                  <td class="text-right">
                    <v-btn size="small" variant="text" color="primary" @click="startEdit(product)">
                      Editar
                    </v-btn>
                    <v-btn
                      size="small"
                      variant="text"
                      color="error"
                      :loading="deletingEan === product.ean"
                      @click="removeProduct(product)"
                    >
                      Excluir
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.catalog-form {
  display: grid;
  gap: 0.75rem;
}

.form-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
