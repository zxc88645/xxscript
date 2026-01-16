/**
 * 代碼插入 Composable
 * 處理快速插入代碼、位置捕捉、按鍵捕捉等功能
 */
import { ref, watch } from 'vue';
import type { Script } from '../types';
import type { editor } from 'monaco-editor';

export function useCodeInsertion(
  selectedScript: { value: Script | null },
  saveScript: () => Promise<void>,
  editorInstance?: { value: editor.IStandaloneCodeEditor | null },
) {
  const showClickModal = ref(false);
  const showKeyModal = ref(false);
  const capturingPosition = ref(false);
  const capturedKey = ref('');

  /**
   * 插入代碼到當前腳本
   */
  const insertCode = (code: string) => {
    if (editorInstance?.value) {
      const editor = editorInstance.value;
      const position = editor.getPosition();
      const selection = editor.getSelection();

      if (!position) return;

      // 如果有選取範圍則替換，否則在游標處插入
      const range = selection || {
        startLineNumber: position.lineNumber,
        startColumn: position.column,
        endLineNumber: position.lineNumber,
        endColumn: position.column,
      };

      const op = {
        range: range,
        text: code,
        forceMoveMarkers: true,
      };

      editor.executeEdits('insert-code', [op]);
      editor.pushUndoStop(); // 添加 Undo 斷點
      editor.focus();

      // 更新 selectedScript content 並儲存
      // 雖然 v-model 會更新，但確保狀態同步
      if (selectedScript.value) {
        selectedScript.value.content = editor.getValue();
        saveScript();
      }
    } else {
      // Fallback: 附加到最後
      if (!selectedScript.value) return;
      const currentContent = selectedScript.value.content || '';
      const newContent = currentContent + (currentContent ? '\n' : '') + code;
      selectedScript.value.content = newContent;
      saveScript();
    }
  };

  /**
   * 插入點擊代碼
   */
  const insertClickCode = (type: string) => {
    const button = type === 'middle' ? 'middle' : type === 'right' ? 'right' : 'left';

    // 完整的點擊流程: 按下 -> 延遲 -> 釋放
    const code = `mouse_down('${button}')\nsleep(0.05)\nmouse_release('${button}')`;

    insertCode(code);
    showClickModal.value = false;
  };

  /**
   * 捕捉滑鼠位置 (透過後端 WebSocket)
   */
  const captureMousePosition = () => {
    capturingPosition.value = true;

    // 建立 WebSocket 連線
    const wsUrl = `ws://${window.location.hostname}:8000/ws/system`;
    const socket = new WebSocket(wsUrl);

    const cleanup = () => {
      capturingPosition.value = false;
      if (socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
      window.removeEventListener('keydown', handleEscape);
    };

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        cleanup();
      }
    };

    socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        if (message.type === 'coordinate') {
          const { x, y } = message.data;
          insertCode(`move(${x}, ${y})`);
          cleanup(); // 成功獲取後自動關閉
        }
      } catch (err) {
        console.error('解析 WebSocket 訊息失敗:', err);
      }
    };

    socket.onclose = () => {
      capturingPosition.value = false;
    };

    socket.onerror = (err) => {
      console.error('WebSocket 錯誤:', err);
      capturingPosition.value = false;
    };

    window.addEventListener('keydown', handleEscape);
  };

  /**
   * 設置按鍵捕捉
   */
  const setupKeyCapture = () => {
    const handleKeyDown = (e: KeyboardEvent) => {
      e.preventDefault();
      capturedKey.value = e.key;
    };

    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  };

  let keyCleanup: (() => void) | null = null;

  // 監聽 showKeyModal 變化
  watch(showKeyModal, (newVal) => {
    if (newVal) {
      capturedKey.value = '';
      keyCleanup = setupKeyCapture();
    } else if (keyCleanup) {
      keyCleanup();
      keyCleanup = null;
    }
  });

  /**
   * 確認按鍵
   */
  const confirmKey = () => {
    if (capturedKey.value) {
      const key = capturedKey.value.toLowerCase();
      // 完整的按鍵流程: 按下 -> 延遲 -> 釋放
      const code = `key_down('${key}')\nsleep(0.05)\nkey_release('${key}')`;
      insertCode(code);
      showKeyModal.value = false;
    }
  };

  /**
   * 取消按鍵捕捉
   */
  const cancelKeyCapture = () => {
    showKeyModal.value = false;
  };

  return {
    showClickModal,
    showKeyModal,
    capturingPosition,
    capturedKey,
    insertCode,
    insertClickCode,
    captureMousePosition,
    confirmKey,
    cancelKeyCapture,
  };
}
