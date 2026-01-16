<template>
  <!-- 位置捕捉提示 -->
  <div
    v-if="show"
    class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50"
  >
    <div class="bg-slate-800 rounded-2xl p-8 max-w-md w-full mx-4 border border-purple-500">
      <div class="text-center">
        <div class="text-6xl mb-4">🎯</div>
        <h3 class="text-2xl font-bold text-white mb-2">捕捉滑鼠位置</h3>
        <p class="text-gray-300 mb-4">請在你想要移動到的位置點擊滑鼠</p>
        <p class="text-purple-400 text-sm">按 ESC 取消</p>
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
