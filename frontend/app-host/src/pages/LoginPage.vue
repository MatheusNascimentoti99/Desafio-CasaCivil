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
  <main class="auth-page">
    <section class="auth-card">
      <h1>Entrar</h1>
      <p class="auth-subtitle">Acesse a plataforma de pedidos</p>

      <form class="auth-form" @submit.prevent="handleSubmit">
        <BrInput
          v-model="form.email"
          label="E-mail"
          name="email"
          placeholder="voce@empresa.com"
          type="email"
        />

        <BrInput
          v-model="form.password"
          label="Senha"
          name="password"
          placeholder="Mínimo 8 caracteres"
          type="password"
        />

        <p v-if="errorMessage" class="auth-error">{{ errorMessage }}</p>

        <BrButton type="submit" :disabled="loading">
          {{ loading ? 'Entrando...' : 'Entrar' }}
        </BrButton>
      </form>

      <p class="auth-footer">
        Ainda não tem conta?
        <RouterLink to="/register">Criar cadastro</RouterLink>
      </p>
    </section>
  </main>
</template>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 1.5rem;
}

.auth-card {
  width: min(100%, 420px);
  border: 1px solid var(--gray-20, #d9d9d9);
  border-radius: 12px;
  padding: 1.5rem;
  background: #fff;
}

.auth-subtitle {
  margin-top: 0.25rem;
  color: #555;
}

.auth-form {
  margin-top: 1rem;
  display: grid;
  gap: 0.75rem;
}

.auth-error {
  color: #b00020;
  font-size: 0.9rem;
}

.auth-footer {
  margin-top: 1rem;
}
</style>
