import { ref, onMounted, onUnmounted } from 'vue';
import { scriptApi } from '../services/api';
import { useConsoleStore } from '../stores/console';

export type EngineStatus = 'IDLE' | 'RUNNING' | 'PAUSED';

export function useScriptEngine() {
  const status = ref<EngineStatus>('IDLE');
  const currentScriptId = ref<string | null>(null);
  const currentScriptName = ref<string | null>(null);
  const loading = ref(false);

  const consoleStore = useConsoleStore();

  let pollTimer: number | null = null;

  const fetchStatus = async () => {
    try {
      const response = await scriptApi.getEngineStatus();
      status.value = response.data.status;
      currentScriptId.value = response.data.script_id;
      currentScriptName.value = response.data.script_name;
    } catch (e) {
      console.error('Failed to fetch engine status', e);
    }
  };

  const startPolling = () => {
    if (pollTimer) return;
    fetchStatus(); // immediate check
    pollTimer = setInterval(fetchStatus, 1000) as unknown as number;
  };

  const stopPolling = () => {
    if (pollTimer) {
      clearInterval(pollTimer);
      pollTimer = null;
    }
  };

  const executeScript = async (id: string, name: string) => {
    try {
      loading.value = true;
      await scriptApi.executeScript(id);
      consoleStore.info(`開始執行: ${name}`, 'Runtime');
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
    loading,
    executeScript,
    stopEngine,
    pauseEngine,
    resumeEngine,
    refreshStatus: fetchStatus,
  };
}
