import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { ScriptCheckIssue } from '../types';

export interface LogEntry {
  id: string;
  timestamp: Date;
  type: 'info' | 'success' | 'warning' | 'error';
  message: string;
  source?: string;
}

export const useConsoleStore = defineStore('console', () => {
  // 終端機日誌
  const logs = ref<LogEntry[]>([]);
  // 代碼問題
  const problems = ref<ScriptCheckIssue[]>([]);
  // 當前標籤頁 'terminal' | 'problems'
  const activeTab = ref<'terminal' | 'problems'>('terminal');

  // 計算屬性
  const problemCount = computed(() => problems.value.length);
  const errorCount = computed(() => problems.value.filter((p) => p.severity === 'error').length);
  const warningCount = computed(
    () => problems.value.filter((p) => p.severity === 'warning').length,
  );

  // 添加日誌
  function addLog(message: string, type: LogEntry['type'] = 'info', source: string = 'System') {
    logs.value.push({
      id: Math.random().toString(36).substring(2, 9),
      timestamp: new Date(),
      type,
      message,
      source,
    });

    // 限制日誌數量，保留最近 1000 條
    if (logs.value.length > 1000) {
      logs.value.shift();
    }

    // 如果有新日誌且不在 terminal 標籤，可能需要提示 (這裡先簡單切換如果有錯誤)
    if (type === 'error' && activeTab.value !== 'terminal') {
      // optional: auto switch or show badge
    }
  }

  // 清除日誌
  function clearLogs() {
    logs.value = [];
  }

  // 設定問題列表
  function setProblems(issues: ScriptCheckIssue[]) {
    problems.value = issues;
    // 如果有問題且當前無日誌或用戶不在操作，可以考慮切換標籤，但自動切換可能會打斷用戶，這裡僅更新數據
  }

  // 清除問題
  function clearProblems() {
    problems.value = [];
  }

  return {
    logs,
    problems,
    activeTab,
    problemCount,
    errorCount,
    warningCount,
    addLog,
    clearLogs,
    setProblems,
    clearProblems,
    info: (msg: string, src?: string) => addLog(msg, 'info', src),
    success: (msg: string, src?: string) => addLog(msg, 'success', src),
    warn: (msg: string, src?: string) => addLog(msg, 'warning', src),
    error: (msg: string, src?: string) => addLog(msg, 'error', src),
  };
});
