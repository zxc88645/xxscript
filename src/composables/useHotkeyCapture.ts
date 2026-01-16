/**
 * 熱鍵捕捉 Composable
 * 處理熱鍵輸入捕捉邏輯
 */
import { ref } from 'vue';
import type { Script } from '../types';

export function useHotkeyCapture(
  selectedScript: { value: Script | null },
  saveScript: () => Promise<void>,
) {
  const capturingHotkey = ref(false);

  /**
   * 捕捉熱鍵 (支援組合鍵)
   */
  const captureHotkey = (event: KeyboardEvent) => {
    event.preventDefault();
    if (!selectedScript.value) return;

    const modifiers: string[] = [];
    if (event.ctrlKey) modifiers.push('ctrl');
    if (event.shiftKey) modifiers.push('shift');
    if (event.altKey) modifiers.push('alt');

    // 取得主鍵
    let mainKey = '';
    if (event.key && !['Control', 'Shift', 'Alt'].includes(event.key)) {
      mainKey = event.key.toLowerCase();
    }

    // 組合熱鍵字串
    const hotkey = [...modifiers, mainKey].filter(Boolean).join('+');

    if (hotkey) {
      selectedScript.value.hotkey = hotkey;
      capturingHotkey.value = false;
      saveScript();
    }
  };

  /**
   * 開始捕捉熱鍵
   */
  const startCapture = () => {
    capturingHotkey.value = true;
  };

  /**
   * 停止捕捉熱鍵
   */
  const stopCapture = () => {
    capturingHotkey.value = false;
  };

  return {
    capturingHotkey,
    captureHotkey,
    startCapture,
    stopCapture,
  };
}
