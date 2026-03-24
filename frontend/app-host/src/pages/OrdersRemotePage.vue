<script setup lang="ts">
import { defineAsyncComponent } from 'vue'

const OrdersApp = defineAsyncComponent(() => import('orders/OrdersApp'))
</script>

<template>
  <section class="orders-mfe-page">
    <h1>Pedidos</h1>
    <OrdersApp />
  </section>
</template>

<style scoped>
.orders-mfe-page {
  padding: 1.5rem;
}
</style>
