<template>
  <div class="space-y-2">
    <div
      v-for="script in scripts"
      :key="script.id"
      @click="$emit('select', script)"
      :class="[
        'p-4 rounded-xl cursor-pointer transition-all border',
        isSelected(script)
          ? 'bg-gradient-to-r from-purple-500/20 to-pink-500/20 border-purple-500'
          : 'bg-white/5 border-white/10 hover:bg-white/10',
      ]"
    >
      <div class="flex items-center justify-between mb-2">
        <h3 class="font-semibold text-white">{{ script.name }}</h3>
        <!-- 啟用開關 -->
        <div class="flex items-center gap-2" @click.stop>
          <span class="text-xs text-gray-400">
            {{ script.enabled ? '已啟用' : '已停用' }}
          </span>
          <button
            @click="$emit('toggle', script)"
            :class="[
              'relative w-12 h-6 rounded-full transition-all',
              script.enabled ? 'bg-green-500' : 'bg-gray-600',
            ]"
          >
            <div
              :class="[
                'absolute top-1 w-4 h-4 bg-white rounded-full transition-all',
                script.enabled ? 'left-7' : 'left-1',
              ]"
            ></div>
          </button>
        </div>
      </div>
      <div class="flex items-center gap-2 text-sm">
        <span class="text-gray-400">熱鍵:</span>
        <span class="text-purple-400 font-mono">{{ script.hotkey || '未設定' }}</span>
      </div>
    </div>

    <div v-if="scripts.length === 0" class="text-center py-8 text-gray-400">
      尚無腳本,點擊「新增」建立第一個腳本
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Script } from '../types';

interface Props {
  scripts: Script[];
  selectedId?: string | null;
}

interface Emits {
  (e: 'select', script: Script): void;
  (e: 'toggle', script: Script): void;
}

const props = defineProps<Props>();
defineEmits<Emits>();

const isSelected = (script: Script) => {
  return props.selectedId === script.id;
};
</script>
