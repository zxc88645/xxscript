/**
 * 錄製功能 Composable
 * 處理腳本錄製相關邏輯
 */
import { ref } from 'vue';
import { scriptApi } from '../services/api';
import type { Script } from '../types';

export function useRecorder(selectedScript: { value: Script | null }) {
  const isRecording = ref(false);

  /**
   * 開始錄製
   */
  const startRecording = async () => {
    try {
      await scriptApi.startRecording();
      isRecording.value = true;
    } catch (err) {
      console.error('開始錄製失敗:', err);
      alert('開始錄製失敗');
    }
  };

  /**
   * 停止錄製
   */
  const stopRecording = async () => {
    try {
      const response = await scriptApi.stopRecording();
      isRecording.value = false;

      // 將錄製的腳本內容填入當前選中的腳本
      if (selectedScript.value && response.data.script) {
        selectedScript.value.content = response.data.script;
      }
    } catch (err) {
      console.error('停止錄製失敗:', err);
      alert('停止錄製失敗');
      isRecording.value = false;
    }
  };

  return {
    isRecording,
    startRecording,
    stopRecording,
  };
}
