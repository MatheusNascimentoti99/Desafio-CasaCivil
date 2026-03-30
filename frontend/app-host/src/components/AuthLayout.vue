<template>
  <v-main class="auth-main">
    <div class="dsgov-top-strip" />
    <div class="dsgov-government-line">
      <div class="dsgov-shell content">
        <span class="dsgov-government-badge">gov.br</span>
      </div>
    </div>

    <v-container class="auth-page dsgov-shell" fluid>
      <v-card class="auth-card dsgov-card" rounded="lg">
        <div class="auth-card-header">
          <span class="auth-badge">Acesso à plataforma</span>
        </div>
        <div class="logo-wrapper">
          <v-img :src="Logo" alt="E-commerce Casa Civil" class="logo-img" />
        </div>
        <v-card-text>
          <RouterView />
        </v-card-text>
      </v-card>
    </v-container>
  </v-main>
</template>
<script setup lang="ts">
import Logo from '@/assets/logo.png'
</script>
<style scoped>
.auth-main {
  min-height: 100vh;
}

.auth-page {
  min-height: calc(100vh - 40px);
  display: grid;
  place-items: center;
  padding: 1.5rem;
}

.auth-card {
  width: min(100%, 460px);
  padding: 0.2rem 1.5rem 1.5rem;
}

.auth-card-header {
  display: flex;
  align-items: center;
  min-height: 3rem;
}

.auth-badge {
  font-size: 0.74rem;
  font-weight: 700;
  color: #071d41;
  background: #fff2cc;
  border-radius: 999px;
  padding: 0.24rem 0.72rem;
}

.logo-wrapper {
  display: flex;
  justify-content: center;
  padding: 0.35rem 1rem 1rem;
}

.logo-img {
  width: 240px;
  max-width: 100%;
}
</style>
