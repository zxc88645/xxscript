<template>
  <div class="flex flex-col h-full bg-bg-surface border-t border-border-base">
    <!-- 工具列 -->
    <div
      class="flex items-center justify-between px-4 h-10 border-b border-border-base bg-bg-main/50"
    >
      <div class="flex items-center gap-1 h-full">
        <button
          @click="store.activeTab = 'terminal'"
          :class="[
            'px-4 h-full text-sm font-medium border-b-2 transition-colors flex items-center gap-2',
            store.activeTab === 'terminal'
              ? 'border-primary text-primary'
              : 'border-transparent text-text-muted hover:text-text-primary',
          ]"
        >
          <span>終端機</span>
          <span
            v-if="store.logs.length > 0"
            class="px-1.5 py-0.5 text-[10px] bg-bg-main rounded-full text-text-muted"
          >
            {{ store.logs.length }}
          </span>
        </button>
        <button
          @click="store.activeTab = 'problems'"
          :class="[
            'px-4 h-full text-sm font-medium border-b-2 transition-colors flex items-center gap-2',
            store.activeTab === 'problems'
              ? 'border-primary text-primary'
              : 'border-transparent text-text-muted hover:text-text-primary',
          ]"
        >
          <span>問題</span>
          <span
            v-if="store.problemCount > 0"
            :class="[
              'px-1.5 py-0.5 text-[10px] rounded-full text-white',
              store.errorCount > 0 ? 'bg-red-500' : 'bg-yellow-500',
            ]"
          >
            {{ store.problemCount }}
          </span>
        </button>
      </div>
      <div class="flex items-center gap-2">
        <button
          @click="clear"
          class="p-1.5 text-text-muted hover:text-text-primary rounded-lg hover:bg-bg-main transition-colors"
          title="清除"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="w-4 h-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- 內容區 -->
    <div class="flex-1 overflow-hidden relative">
      <!-- 終端機 -->
      <div
        v-if="store.activeTab === 'terminal'"
        class="absolute inset-0 overflow-y-auto p-4 font-mono text-sm space-y-1"
        ref="logContainer"
      >
        <div v-if="store.logs.length === 0" class="text-text-muted italic select-none">
          暫無日誌...
        </div>
        <div
          v-for="log in store.logs"
          :key="log.id"
          class="flex gap-3 hover:bg-white/5 px-2 py-0.5 -mx-2 rounded"
        >
          <span class="text-text-muted shrink-0 w-20">
            {{ formatTime(log.timestamp) }}
          </span>
          <span
            :class="{
              'text-blue-400': log.type === 'info',
              'text-green-400': log.type === 'success',
              'text-yellow-400': log.type === 'warning',
              'text-red-400': log.type === 'error',
            }"
            class="shrink-0 w-16 uppercase font-bold text-xs pt-0.5"
          >
            {{ log.type }}
          </span>
          <span class="text-white/80 break-all whitespace-pre-wrap flex-1">{{ log.message }}</span>
        </div>
      </div>

      <!-- 問題列表 -->
      <div v-else class="absolute inset-0 overflow-y-auto">
        <div v-if="store.problems.length === 0" class="p-8 text-center text-text-muted select-none">
          <div class="text-4xl mb-4 opacity-20">✓</div>
          <p>未發現問題</p>
        </div>
        <div v-else class="divide-y divide-border-base">
          <div
            v-for="(issue, index) in store.problems"
            :key="index"
            class="flex items-start gap-3 p-3 hover:bg-white/5 cursor-pointer transition-colors"
            @click="jumpToIssue(issue)"
          >
            <div class="pt-1">
              <!-- Error Icon -->
              <svg
                v-if="issue.severity === 'error'"
                class="w-4 h-4 text-red-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <!-- Warning Icon -->
              <svg
                v-else
                class="w-4 h-4 text-yellow-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-text-primary truncate">
                {{ issue.message }}
              </p>
              <p class="text-xs text-text-muted mt-0.5">
                行 {{ issue.line }}，列 {{ issue.column }}
                <span v-if="issue.code" class="ml-2 px-1.5 py-0.5 bg-white/10 rounded text-[10px]">
                  {{ issue.code }}
                </span>
              </p>
              <p
                v-if="issue.script_context"
                class="mt-1 font-mono text-xs text-text-muted/70 bg-black/20 px-2 py-1 rounded w-fit"
              >
                {{ issue.script_context }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue';
import { useConsoleStore } from '../stores/console';
import type { ScriptCheckIssue } from '../types';

const store = useConsoleStore();
const logContainer = ref<HTMLElement | null>(null);

const emit = defineEmits<{
  (e: 'jump', issue: ScriptCheckIssue): void;
}>();

// 自動滾動到底部
watch(
  () => store.logs.length,
  async () => {
    if (store.activeTab === 'terminal') {
      await nextTick();
      if (logContainer.value) {
        logContainer.value.scrollTop = logContainer.value.scrollHeight;
      }
    }
  },
);

const timeFormatter = new Intl.DateTimeFormat('zh-TW', {
  hour: '2-digit',
  minute: '2-digit',
  second: '2-digit',
  hour12: false,
});

const formatTime = (date: Date) => timeFormatter.format(date);

const clear = () => {
  if (store.activeTab === 'terminal') {
    store.clearLogs();
  } else {
    // 問題只能透過修復代碼清除，這裡不操作，或者可以讓用戶暫時隱藏
  }
};

const jumpToIssue = (issue: ScriptCheckIssue) => {
  emit('jump', issue);
};
</script>
