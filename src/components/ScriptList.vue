<template>
  <div class="space-y-2">
    <div
      v-for="script in scripts"
      :key="script.id"
      :class="[
        'group flex items-center justify-between p-4 rounded-xl border transition-all cursor-pointer',
        selectedId === script.id
          ? 'bg-primary/5 border-primary shadow-sm'
          : 'bg-bg-main border-border-base hover:border-primary/50 hover:bg-bg-surface',
      ]"
      @click="$emit('select', script)"
    >
      <div class="flex items-center gap-3 min-w-0">
        <div
          :class="[
            'w-2 h-2 rounded-full flex-shrink-0',
            script.enabled ? 'bg-primary' : 'bg-text-muted/30',
          ]"
        ></div>
        <div class="flex flex-col min-w-0">
          <span
            :class="[
              'font-semibold truncate',
              selectedId === script.id ? 'text-primary' : 'text-text-base',
            ]"
          >
            {{ script.name }}
          </span>
          <span class="text-xs text-text-muted font-mono truncate">
            {{ script.hotkey || '無熱鍵' }}
          </span>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <label class="relative inline-flex items-center cursor-pointer" @click.stop>
          <input
            type="checkbox"
            :checked="script.enabled"
            class="sr-only peer"
            @change="$emit('toggle', script)"
          />
          <div
            class="w-9 h-5 bg-border-base peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-primary"
          ></div>
        </label>
      </div>
    </div>

    <!-- 空狀態 -->
    <div v-if="scripts.length === 0" class="py-12 text-center">
      <p class="text-text-muted text-sm italic">尚無腳本</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Script } from '../types';

defineProps<{
  scripts: Script[];
  selectedId?: string;
}>();

defineEmits<{
  (e: 'select', script: Script): void;
  (e: 'toggle', script: Script): void;
}>();
</script>
