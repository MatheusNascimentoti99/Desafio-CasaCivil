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
    <h1 class="text-h4 text-center">Novo registro</h1>
    <p class="auth-subtitle">Crie sua conta para acessar o sistema</p>

    <v-form class="auth-form" @submit.prevent="handleSubmit">
      <v-text-field
        v-model="form.full_name"
        label="Nome completo"
        name="full_name"
        placeholder="Seu nome"
        variant="outlined"
      />

      <v-text-field
        v-model="form.email"
        label="E-mail"
        name="email"
        placeholder="voce@empresa.com"
        type="email"
        variant="outlined"
      />

      <v-text-field
        v-model="form.password"
        label="Senha"
        name="password"
        placeholder="Mínimo 8 caracteres"
        type="password"
        variant="outlined"
      />

      <v-alert v-if="errorMessage" type="error" variant="tonal" density="compact">
        {{ errorMessage }}
      </v-alert>

      <v-btn type="submit" :loading="loading" color="primary" block>
        {{ loading ? 'Registrando...' : 'Registrar' }}
      </v-btn>
    </v-form>

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

.auth-footer {
  margin-top: 1rem;
}
</style>
