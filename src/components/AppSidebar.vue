<template>
  <aside
    class="w-64 flex-shrink-0 border-r border-border-base bg-bg-surface flex flex-col h-screen sticky top-0"
  >
    <!-- Logo 區域 -->
    <div class="p-6 flex items-center gap-3">
      <div
        class="w-10 h-10 bg-gradient-to-br from-primary to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-primary/20"
      >
        <span class="text-white font-bold text-xl">XX</span>
      </div>
      <h1 class="text-xl font-bold tracking-tight">XXScript</h1>
    </div>

    <!-- 導航區域 -->
    <nav class="flex-1 px-4 py-4 space-y-1">
      <a
        href="#"
        class="flex items-center gap-3 px-4 py-3 rounded-xl bg-primary/10 text-primary font-medium"
      >
        <span class="text-xl">📊</span>
        儀表板
      </a>
      <!-- 這裡之後可以加入更多導航項 -->
    </nav>

    <!-- 底部設置 -->
    <div class="p-4 border-t border-border-base">
      <button
        @click="themeStore.toggleTheme"
        class="w-full flex items-center justify-between px-4 py-3 rounded-xl hover:bg-bg-main transition-colors group"
      >
        <div class="flex items-center gap-3">
          <span class="text-xl">{{ themeStore.isDarkMode ? '🌙' : '☀️' }}</span>
          <span class="font-medium text-text-muted group-hover:text-text-base">
            {{ themeStore.isDarkMode ? '深色模式' : '淺色模式' }}
          </span>
        </div>
        <div
          class="w-10 h-5 bg-border-base rounded-full relative p-1 transition-colors"
          :class="{ 'bg-primary': themeStore.isDarkMode }"
        >
          <div
            class="w-3 h-3 bg-white rounded-full shadow transition-transform duration-300"
            :class="{ 'translate-x-5': themeStore.isDarkMode }"
          ></div>
        </div>
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { useThemeStore } from '../stores/theme';

const themeStore = useThemeStore();
</script>
