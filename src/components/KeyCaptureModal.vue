<template>
  <!-- 按鍵輸入模態框 -->
  <div
    v-if="modelValue"
    class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
    @click="$emit('update:modelValue', false)"
  >
    <div
      class="bg-slate-800 rounded-2xl p-6 max-w-md w-full mx-4 border border-white/10"
      @click.stop
    >
      <h3 class="text-xl font-bold text-white mb-4">按下你想要的鍵</h3>
      <div class="p-4 bg-black/30 rounded-lg border border-white/10 mb-4">
        <p class="text-gray-400 text-sm mb-2">請按下任意鍵...</p>
        <p class="text-white text-lg font-mono">{{ capturedKey || '等待輸入...' }}</p>
      </div>
      <div class="flex gap-3">
        <button
          @click="$emit('confirm')"
          :disabled="!capturedKey"
          class="flex-1 px-4 py-2 bg-green-500 hover:bg-green-600 disabled:bg-gray-500 disabled:opacity-50 text-white rounded-lg transition-all"
        >
          確認
        </button>
        <button
          @click="$emit('cancel')"
          class="px-4 py-2 bg-gray-500/20 hover:bg-gray-500/30 text-gray-400 rounded-lg transition-all"
        >
          取消
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  modelValue: boolean;
  capturedKey: string;
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void;
  (e: 'confirm'): void;
  (e: 'cancel'): void;
}

defineProps<Props>();
defineEmits<Emits>();
</script>
