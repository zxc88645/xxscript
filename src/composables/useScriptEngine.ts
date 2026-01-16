import { ref, onMounted, onUnmounted } from 'vue';
import { scriptApi } from '../services/api';
import { useConsoleStore } from '../stores/console';

export type EngineStatus = 'IDLE' | 'RUNNING' | 'PAUSED';

export function useScriptEngine() {
  const status = ref<EngineStatus>('IDLE');
  const currentScriptId = ref<string | null>(null);
  const currentScriptName = ref<string | null>(null);
  const currentLine = ref<number | null>(null);
  const loading = ref(false);

  const consoleStore = useConsoleStore();

  let pollTimeout: number | null = null;
  let isActive = false;

  const fetchStatus = async () => {
    try {
      const response = await scriptApi.getEngineStatus();
      status.value = response.data.status;
      currentScriptId.value = response.data.script_id;
      currentScriptName.value = response.data.script_name;
      currentLine.value = response.data.current_line;
    } catch (e) {
      console.error('Failed to fetch engine status', e);
    }
  };

  const poll = async () => {
    if (!isActive) return;

    await fetchStatus();

    // 如果正在運行，加快輪詢頻率以更新行號
    const interval = status.value === 'RUNNING' ? 200 : 1000;
    pollTimeout = window.setTimeout(poll, interval);
  };

  const startPolling = () => {
    if (isActive) return;
    isActive = true;
    poll();
  };

  const stopPolling = () => {
    isActive = false;
    if (pollTimeout) {
      clearTimeout(pollTimeout);
      pollTimeout = null;
    }
  };

  const executeScript = async (id: string, name: string) => {
    try {
      loading.value = true;
      currentLine.value = 0;
      await scriptApi.executeScript(id);
      consoleStore.info(`開始執行: ${name}`, 'Runtime');
      // 立即更新一次狀態
      await fetchStatus();
    } catch (err) {
      const errorObj = err as Error;
      consoleStore.error(`執行失敗: ${errorObj.message}`, 'Runtime');
      console.error(err);
    } finally {
      loading.value = false;
    }
  };

  const stopEngine = async () => {
    try {
      const response = await scriptApi.stopEngine();
      consoleStore.warn(`停止執行: ${response.data.message}`, 'Runtime');
      await fetchStatus();
    } catch (e) {
      console.error(e);
    }
  };

  const pauseEngine = async () => {
    try {
      const response = await scriptApi.pauseEngine();
      consoleStore.info(`暫停執行: ${response.data.message}`, 'Runtime');
      await fetchStatus();
    } catch (e) {
      console.error(e);
    }
  };

  const resumeEngine = async () => {
    try {
      const response = await scriptApi.resumeEngine();
      consoleStore.info(`繼續執行: ${response.data.message}`, 'Runtime');
      await fetchStatus();
    } catch (e) {
      console.error(e);
    }
  };

  onMounted(() => {
    startPolling();
  });

  onUnmounted(() => {
    stopPolling();
  });

  return {
    status,
    currentScriptId,
    currentScriptName,
    currentLine,
    loading,
    executeScript,
    stopEngine,
    pauseEngine,
    resumeEngine,
    refreshStatus: fetchStatus,
  };
}
