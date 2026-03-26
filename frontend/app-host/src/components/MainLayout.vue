<template>
  <v-app-bar color="primary" density="comfortable">
    <v-app-bar-title>E-cCC</v-app-bar-title>
    <v-btn variant="text" :to="{ name: 'home' }">Home</v-btn>
    <v-btn variant="text" :to="{ name: 'orders' }">Orders</v-btn>
    <v-btn flat color="white" @click="logout">Logout</v-btn>
  </v-app-bar>

  <v-main>
    <RouterView />
  </v-main>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';

const router = useRouter();

function logout() {
  localStorage.removeItem('auth_token')
  router.push({ name: 'login' })
}
</script>
