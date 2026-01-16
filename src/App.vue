<template>
  <div class="flex min-h-screen bg-bg-main">
    <AppSidebar />
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <RouterView />
    </div>
  </div>
</template>

<script setup lang="ts">
import AppSidebar from './components/AppSidebar.vue';
</script>
