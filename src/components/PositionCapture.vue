<template>
  <!-- 位置捕捉提示 -->
  <div
    v-if="show"
    class="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-[100]"
  >
    <div
      class="bg-bg-surface rounded-3xl p-10 max-w-sm w-full mx-4 border border-border-base shadow-2xl flex flex-col items-center"
    >
      <div
        class="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mb-6 animate-pulse"
      >
        <span class="text-4xl text-primary">🎯</span>
      </div>
      <h3 class="text-2xl font-bold mb-4">捕捉全域座標</h3>
      <div class="space-y-4 text-center">
        <p class="text-text-muted">請將滑鼠移動到目標位置，然後按下</p>
        <div
          class="inline-flex items-center gap-2 px-4 py-2 bg-primary text-white font-mono rounded-xl shadow-lg shadow-primary/30"
        >
          <span class="text-lg font-bold">F2</span>
        </div>
        <p class="text-text-muted mt-4">座標將自動插入到編輯器中。</p>
        <div class="pt-6">
          <p class="text-xs text-text-muted/50">
            按
            <kbd class="px-2 py-1 bg-bg-main border border-border-base rounded">ESC</kbd> 取消操作
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  show: boolean;
}

defineProps<Props>();
</script>
