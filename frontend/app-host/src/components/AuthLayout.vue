<template>
  <v-main>
    <v-container class="auth-page" fluid>
      <v-card class="auth-card" elevation="8">
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
.auth-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 1.5rem;
  background:
    radial-gradient(circle at top right, rgba(0, 135, 90, 0.08), transparent 45%),
    radial-gradient(circle at bottom left, rgba(0, 67, 180, 0.08), transparent 40%),
    #f8f8f8;
}

.auth-card {
  width: min(100%, 460px);
  border: 1px solid var(--gray-20, #d9d9d9);
  border-radius: 12px;
  padding: 1.5rem;
  background: #fff;
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.06);
}

.logo-wrapper {
  display: flex;
  justify-content: center;
  padding: 1.5rem 1rem 0.75rem;
}

.logo-img {
  width: 240px;
  max-width: 100%;
}
</style>
