<template>
  <div class="flex gap-2">
    <button
      @click="$emit('insert-click')"
      class="px-3 py-1 text-xs bg-blue-500/20 hover:bg-blue-500/30 text-blue-400 border border-blue-500/50 rounded transition-all"
      title="插入滑鼠點擊"
    >
      🖱️ 點擊
    </button>
    <button
      @click="$emit('capture-position')"
      class="px-3 py-1 text-xs bg-purple-500/20 hover:bg-purple-500/30 text-purple-400 border border-purple-500/50 rounded transition-all"
      title="捕捉滑鼠位置"
    >
      ↗️ 移動
    </button>
    <button
      @click="$emit('insert', 'type_text(\'文字\')')"
      class="px-3 py-1 text-xs bg-green-500/20 hover:bg-green-500/30 text-green-400 border border-green-500/50 rounded transition-all"
      title="插入文字輸入"
    >
      ⌨️ 輸入
    </button>
    <button
      @click="$emit('insert-key')"
      class="px-3 py-1 text-xs bg-yellow-500/20 hover:bg-yellow-500/30 text-yellow-400 border border-yellow-500/50 rounded transition-all"
      title="插入按鍵"
    >
      ⏎ 按鍵
    </button>
    <button
      @click="$emit('insert', 'sleep(1.0)')"
      class="px-3 py-1 text-xs bg-orange-500/20 hover:bg-orange-500/30 text-orange-400 border border-orange-500/50 rounded transition-all"
      title="插入延遲"
    >
      ⏱️ 延遲
    </button>
  </div>
</template>

<script setup lang="ts">
interface Emits {
  (e: 'insert', code: string): void;
  (e: 'insert-click'): void;
  (e: 'insert-key'): void;
  (e: 'capture-position'): void;
}

defineEmits<Emits>();
</script>
