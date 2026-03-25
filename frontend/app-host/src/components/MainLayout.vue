<template>
  <div class="main-layout">
    <nav class="navbar">
      <div class="nav-container">
        <h1 class="logo">E-cCC</h1>
        <ul class="nav-links">
          <li><router-link :to="{ name: 'home' }">Home</router-link></li>
          <li><router-link :to="{ name: 'orders' }">Orders</router-link></li>
          <button @click="logout" class="br-button inverted mt-3 mt-sm-0 ml-sm-3">Logout</button>
        </ul>
      </div>
    </nav>
    <RouterView />
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';

const router = useRouter();

function logout() {
  localStorage.removeItem('auth_token')
  router.push({ name: 'login' })
}
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

.navbar{
  background-color: #333;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  color: white;
  margin: 0;
  font-size: 1.5rem;
}

.nav-links {
  list-style: none;
  display: flex;
  align-items: center;
  gap: 2rem;
  margin: 0;
  padding: 0;
}

.nav-links a {
  color: white;
  text-decoration: none;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #007bff;
}

</style>
