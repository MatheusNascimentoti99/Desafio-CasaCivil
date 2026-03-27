<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { loginUser } from '@/services/auth'

const router = useRouter()

const form = reactive({
  email: '',
  password: '',
})

const loading = ref(false)
const errorMessage = ref('')

async function handleSubmit() {
  errorMessage.value = ''

  if (!form.email || !form.password) {
    errorMessage.value = 'Preencha e-mail e senha.'
    return
  }

  loading.value = true

  try {
    const token = await loginUser(form)
    localStorage.setItem('auth_token', token.access_token)
    router.push({ name: 'home' })
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Falha no login'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <h1 class="text-h4 text-center">Entrar</h1>
    <p class="auth-subtitle">Acesse a plataforma de pedidos</p>

    <v-form class="auth-form" @submit.prevent="handleSubmit">
      <v-text-field
        v-model="form.email"
        label="E-mail"
        name="email"
        placeholder="voce@empresa.com"
        type="email"
        autocomplete="email"
        variant="outlined"
      />

      <v-text-field
        v-model="form.password"
        label="Senha"
        name="password"
        placeholder="Mínimo 8 caracteres"
        type="password"
        autocomplete="current-password"
        variant="outlined"
      />

      <v-alert v-if="errorMessage" type="error" variant="tonal" density="compact">
        {{ errorMessage }}
      </v-alert>

      <v-btn type="submit" :loading="loading" color="primary" block>
        {{ loading ? 'Entrando...' : 'Entrar' }}
      </v-btn>
    </v-form>

    <p class="auth-footer">
      Ainda não tem conta?
      <RouterLink :to="{ name: 'register' }">Criar cadastro</RouterLink>
    </p>
  </div>
</template>

<style scoped>
.auth-subtitle {
  margin-top: 0.25rem;
  color: #555;
}

.auth-form {
  margin-top: 1rem;
  display: grid;
  gap: 0.75rem;
}

.auth-footer {
  margin-top: 1rem;
}
</style>
