/**
 * 按鍵監聽器 Composable
 * 處理全局按鍵監聽器的啟動和停止
 */
import { ref, onMounted } from 'vue';
import { scriptApi } from '../services/api';
import { useToast } from './useToast';

export function useKeyListener() {
  const listenerRunning = ref(false);
  const loading = ref(false);
  const toast = useToast();

  /**
   * 檢查監聽器狀態
   */
  const checkStatus = async () => {
    try {
      const response = await scriptApi.getStatus();
      listenerRunning.value = response.data.listener_running;
    } catch (err) {
      console.error('檢查狀態失敗:', err);
    }
  };

  /**
   * 切換監聽器狀態
   */
  const toggleListener = async () => {
    try {
      loading.value = true;
      if (listenerRunning.value) {
        await scriptApi.stopListener();
      } else {
        await scriptApi.startListener();
      }
      await checkStatus();
    } catch (err) {
      console.error('切換監聽器失敗:', err);
      toast.error('切換監聽器失敗');
    } finally {
      loading.value = false;
    }
  };

  // 初始化時檢查狀態
  onMounted(() => {
    checkStatus();
  });

  return {
    listenerRunning,
    loading,
    toggleListener,
    checkStatus,
  };
}
