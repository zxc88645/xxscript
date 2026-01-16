<template>
  <!-- 點擊按鈕選擇模態框 -->
  <div
    v-if="modelValue"
    class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
    @click="$emit('update:modelValue', false)"
  >
    <div
      class="bg-slate-800 rounded-2xl p-6 max-w-md w-full mx-4 border border-white/10"
      @click.stop
    >
      <h3 class="text-xl font-bold text-white mb-4">選擇滑鼠操作</h3>
      <div class="grid grid-cols-3 gap-3">
        <button
          @click="$emit('select', 'left')"
          class="px-4 py-3 bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 border border-blue-500 rounded-lg transition-all"
        >
          🖘️ 左鍵點擊
        </button>
        <button
          @click="$emit('select', 'right')"
          class="px-4 py-3 bg-purple-500/20 hover:bg-purple-500/30 text-purple-400 border border-purple-500 rounded-lg transition-all"
        >
          🖘️ 右鍵點擊
        </button>
        <button
          @click="$emit('select', 'middle')"
          class="px-4 py-3 bg-green-500/20 hover:bg-green-500/30 text-green-400 border border-green-500 rounded-lg transition-all"
        >
          🖘️ 中鍵點擊
        </button>
      </div>
      <button
        @click="$emit('update:modelValue', false)"
        class="mt-4 w-full px-4 py-2 bg-gray-500/20 hover:bg-gray-500/30 text-gray-400 rounded-lg transition-all"
      >
        取消
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  modelValue: boolean;
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void;
  (e: 'select', type: string): void;
}

defineProps<Props>();
defineEmits<Emits>();
</script>
