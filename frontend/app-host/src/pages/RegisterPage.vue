<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { registerUser } from '@/services/auth'

const router = useRouter()

const form = reactive({
  full_name: '',
  email: '',
  password: '',
})

const loading = ref(false)
const errorMessage = ref('')

async function handleSubmit() {
  errorMessage.value = ''

  if (!form.full_name || !form.email || !form.password) {
    errorMessage.value = 'Preencha todos os campos.'
    return
  }

  if (form.password.length < 8) {
    errorMessage.value = 'A senha precisa ter no mínimo 8 caracteres.'
    return
  }

  loading.value = true

  try {
    await registerUser(form)
    router.push({ name: 'login' })
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Falha ao registrar usuário'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <h1>Novo registro</h1>
    <p class="auth-subtitle">Crie sua conta para acessar o sistema</p>

    <form class="auth-form" @submit.prevent="handleSubmit">
        <BrInput
          v-model="form.full_name"
          label="Nome completo"
          name="full_name"
          placeholder="Seu nome"
        />

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
          {{ loading ? 'Registrando...' : 'Registrar' }}
        </BrButton>
    </form>

    <p class="auth-footer">
        Já possui conta?
        <RouterLink :to="{ name: 'login' }">Entrar</RouterLink>
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

.auth-error {
  color: #b00020;
  font-size: 0.9rem;
}

.auth-footer {
  margin-top: 1rem;
}
</style>
