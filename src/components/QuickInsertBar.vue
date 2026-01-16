<template>
  <div
    class="flex flex-wrap items-center gap-1.5 p-1 bg-bg-main rounded-xl border border-border-base"
  >
    <button
      v-for="item in INSERT_ITEMS"
      :key="item.label"
      @click="$emit('insert', item.code)"
      class="px-3 py-1.5 text-xs font-medium text-text-muted hover:text-primary hover:bg-bg-surface rounded-lg transition-all border border-transparent hover:border-border-base flex items-center gap-1.5"
      :title="item.label"
    >
      <span>{{ item.icon }}</span>
      {{ item.label }}
    </button>
    <div class="w-[1px] h-4 bg-border-base mx-1"></div>
    <button
      @click="$emit('insert-click')"
      class="px-3 py-1.5 text-xs font-medium text-text-muted hover:text-primary hover:bg-bg-surface rounded-lg transition-all border border-transparent hover:border-border-base flex items-center gap-1.5"
      title="插入點擊"
    >
      <span>🖱️</span> 點擊
    </button>
    <button
      @click="$emit('insert-key')"
      class="px-3 py-1.5 text-xs font-medium text-text-muted hover:text-primary hover:bg-bg-surface rounded-lg transition-all border border-transparent hover:border-border-base flex items-center gap-1.5"
      title="插入按鍵"
    >
      <span>⌨️</span> 按鍵
    </button>
    <button
      @click="$emit('capture-position')"
      class="px-3 py-1.5 text-xs font-medium text-primary bg-primary/5 hover:bg-primary/10 rounded-lg transition-all border border-primary/10 flex items-center gap-1.5"
      title="座標擷取"
    >
      <span>🎯</span> 擷取座標 (F2)
    </button>
  </div>
</template>

<script setup lang="ts">
const INSERT_ITEMS = [
  { label: '延遲', icon: '⏱️', code: 'sleep(1.0)\n' },
  { label: '滾動', icon: '↕️', code: 'scroll(0, -10)\n' },
  { label: '提示', icon: '💡', code: 'print("Hello world")\n' },
];

defineEmits<{
  (e: 'insert', code: string): void;
  (e: 'insert-click'): void;
  (e: 'insert-key'): void;
  (e: 'capture-position'): void;
}>();
</script>
