<template>
  <main class="auth-page">
    <section class="auth-card">
      <RouterView />
    </section>
  </main>
</template>

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
</style>
