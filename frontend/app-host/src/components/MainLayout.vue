<template>
  <header class="dsgov-header">
    <div class="dsgov-top-strip" />
    <div class="dsgov-government-line">
      <div class="dsgov-shell content">
        <span class="dsgov-government-badge">gov.br</span>
      </div>
    </div>

    <div class="dsgov-header-main">
      <div class="dsgov-shell header-content">
        <div class="brand">
          <p class="brand-title">Plataforma de Pedidos</p>
          <p class="brand-subtitle">Casa Civil</p>
        </div>

        <nav class="nav-links" aria-label="Navegação principal">
          <v-btn variant="text" :to="{ name: 'home' }">Início</v-btn>
          <v-btn variant="text" :to="{ name: 'users' }">Usuários</v-btn>
          <v-btn variant="text" :to="{ name: 'orders' }">Pedidos</v-btn>
          <v-btn variant="text" :to="{ name: 'catalog' }">Catálogo</v-btn>
        </nav>

        <v-spacer />
        <v-btn color="primary" prepend-icon="mdi-logout" @click="logout">Sair</v-btn>
      </div>
    </div>
  </header>

  <v-main class="dsgov-main">
    <RouterView />
  </v-main>
</template>

<script lang="ts" setup>
import { logoutUser } from '@/services/auth'
import { useRouter } from 'vue-router'

const router = useRouter()

async function logout() {
  await logoutUser()
  router.push({ name: 'login' })
}
</script>
<style scoped>
.dsgov-header-main {
  background: #fff;
  border-bottom: 1px solid #d9d9d9;
}

.dsgov-main {
  padding: 1rem;
}

.brand {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.brand-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: #071d41;
}

.brand-subtitle {
  margin: 0;
  font-size: 0.84rem;
  color: #495057;
}

.header-content {
  min-height: 78px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.2rem;
  margin-left: 1.2rem;
}

.nav-links :deep(.v-btn) {
  color: #1351b4;
  font-weight: 600;
}

@media (max-width: 980px) {
  .brand-subtitle {
    display: none;
  }

  .nav-links {
    margin-left: 0.2rem;
    gap: 0.1rem;
  }
}

@media (max-width: 760px) {
  .nav-links {
    display: none;
  }
}
</style>
