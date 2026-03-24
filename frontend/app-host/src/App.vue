<script setup lang="ts">
import { BrButton } from '@govbr-ds/webcomponents-vue';
import { ref } from 'vue'
const name = ref('Lorem ipsum')

components: {
  BrButton
}
</script>

<template>
  <h1>You did it!</h1>
  <p>
    Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read the
    documentation
  </p>
  <div>
    <br-button name="name" placeholder="Seu nome" v-model="name">teste</br-button>
  </div>
</template>

<style>
</style>
