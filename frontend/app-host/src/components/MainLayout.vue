<template>
  <v-app-bar color="primary" density="comfortable">
    <v-app-bar-title>E-cCC</v-app-bar-title>
    <v-btn variant="text" :to="{ name: 'home' }">Home</v-btn>
    <v-btn variant="text" :to="{ name: 'users' }">Usuários</v-btn>
    <v-btn variant="text" :to="{ name: 'orders' }">Orders</v-btn>
    <v-spacer />
    <v-btn flat color="white" @click="logout" title="Logout" icon="mdi-logout"/>
  </v-app-bar>

  <v-main class="ma-3">
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
</style>
