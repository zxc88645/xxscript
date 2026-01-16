/**
 * 腳本管理 Composable
 * 處理腳本的 CRUD 操作
 */
import { ref, onMounted } from 'vue';
import { scriptApi } from '../services/api';
import type { Script, ScriptCreate, ScriptUpdate } from '../types';
import { useToast } from './useToast';
import { useConfirm } from './useConfirm';

export function useScripts() {
  const scripts = ref<Script[]>([]);
  const selectedScript = ref<Script | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const toast = useToast();
  const { confirm } = useConfirm();

  /**
   * 載入所有腳本
   */
  const loadScripts = async () => {
    try {
      loading.value = true;
      error.value = null;
      const response = await scriptApi.getScripts();
      scripts.value = response.data;
    } catch (err) {
      error.value = '載入腳本失敗';
      toast.error('載入腳本失敗');
      console.error('載入腳本失敗:', err);
    } finally {
      loading.value = false;
    }
  };

  /**
   * 選擇腳本
   */
  const selectScript = (script: Script) => {
    selectedScript.value = { ...script };
  };

  /**
   * 創建新腳本
   */
  const createScript = async (data?: ScriptCreate) => {
    try {
      const scriptData = data || {
        name: '新腳本',
        content: '# 在此輸入腳本內容\n',
        hotkey: '',
      };
      const response = await scriptApi.createScript(scriptData);
      await loadScripts();
      selectedScript.value = response.data;
    } catch (err) {
      error.value = '建立腳本失敗';
      toast.error('建立腳本失敗');
      console.error('建立腳本失敗:', err);
    }
  };

  /**
   * 更新腳本
   */
  const updateScript = async (id: string, data: ScriptUpdate) => {
    try {
      await scriptApi.updateScript(id, data);
      await loadScripts();
    } catch (err) {
      error.value = '更新腳本失敗';
      toast.error('更新腳本失敗');
      console.error('更新腳本失敗:', err);
    }
  };

  /**
   * 儲存當前選中的腳本
   */
  const saveCurrentScript = async () => {
    if (!selectedScript.value) return;

    try {
      await scriptApi.updateScript(selectedScript.value.id, {
        name: selectedScript.value.name,
        content: selectedScript.value.content,
        hotkey: selectedScript.value.hotkey,
        enabled: selectedScript.value.enabled,
      });
      await loadScripts();
    } catch (err) {
      error.value = '儲存腳本失敗';
      toast.error('儲存腳本失敗');
      console.error('儲存腳本失敗:', err);
    }
  };

  /**
   * 刪除腳本
   */
  const deleteScript = async (id: string) => {
    const isConfirmed = await confirm({
      title: '刪除腳本',
      message: '確定要刪除此腳本嗎? 此動作無法復原。',
      confirmText: '刪除',
      type: 'danger',
    });
    if (!isConfirmed) return;

    try {
      await scriptApi.deleteScript(id);
      if (selectedScript.value?.id === id) {
        selectedScript.value = null;
      }
      await loadScripts();
    } catch (err) {
      error.value = '刪除腳本失敗';
      toast.error('刪除腳本失敗');
      console.error('刪除腳本失敗:', err);
    }
  };

  /**
   * 切換腳本啟用狀態
   */
  const toggleScriptEnabled = async (script: Script) => {
    try {
      script.enabled = !script.enabled;
      await scriptApi.updateScript(script.id, { enabled: script.enabled });
      await loadScripts();
    } catch (err) {
      error.value = '切換腳本狀態失敗';
      toast.error('切換腳本狀態失敗');
      console.error('切換腳本狀態失敗:', err);
      // 失敗時回滾
      script.enabled = !script.enabled;
    }
  };

  /**
   * 執行腳本
   */
  const executeScript = async (id: string) => {
    try {
      const response = await scriptApi.executeScript(id);
      toast.success(`執行完成: ${response.data.message}`);
    } catch (err) {
      error.value = '執行腳本失敗';
      console.error('執行腳本失敗:', err);
      toast.error('執行腳本失敗');
    }
  };

  // 初始化時載入腳本
  onMounted(() => {
    loadScripts();
  });

  return {
    scripts,
    selectedScript,
    loading,
    error,
    loadScripts,
    selectScript,
    createScript,
    updateScript,
    saveCurrentScript,
    deleteScript,
    toggleScriptEnabled,
    executeScript,
  };
}
