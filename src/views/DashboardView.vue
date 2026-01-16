<template>
  <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
    <!-- 頂部 Navbar -->
    <header
      class="h-16 border-b border-border-base bg-bg-surface flex items-center justify-between px-8"
    >
      <div class="flex items-center gap-4">
        <h2 class="text-lg font-semibold">儀表板</h2>
        <div class="h-4 w-[1px] bg-border-base"></div>
        <div class="flex items-center gap-2">
          <div
            :class="[
              'w-2 h-2 rounded-full',
              listenerRunning ? 'bg-green-500 shadow-sm shadow-green-500/50' : 'bg-red-500',
            ]"
          ></div>
          <span class="text-sm font-medium text-text-muted">
            狀態：{{ listenerRunning ? '監聽中 (全自動)' : '已停止' }}
          </span>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <!-- 監聽按鈕已移除，改為全自動管理 -->
      </div>
    </header>

    <!-- 滾動內容區 -->
    <main class="flex-1 overflow-y-auto p-8">
      <div class="max-w-[1600px] mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <!-- 左側:腳本列表 -->
          <div class="lg:col-span-4 flex flex-col gap-6">
            <div class="bg-bg-surface rounded-2xl border border-border-base p-6 shadow-sm">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-bold">腳本列表</h2>
                <button
                  @click="createScript"
                  class="p-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
                  title="新增腳本"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="w-5 h-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 4v16m8-8H4"
                    />
                  </svg>
                </button>
              </div>

              <ScriptList
                :scripts="scripts"
                :selected-id="selectedScript?.id"
                @select="selectScript"
                @toggle="toggleScriptEnabled"
              />
            </div>
          </div>

          <!-- 右側:編輯器 -->
          <div class="lg:col-span-8">
            <div
              v-if="selectedScript"
              class="bg-bg-surface rounded-2xl border border-border-base p-8 shadow-sm"
            >
              <!-- 腳本資訊 -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div>
                  <label class="block text-sm font-medium text-text-muted mb-2 text-indent-1"
                    >腳本名稱</label
                  >
                  <input
                    v-model="selectedScript.name"
                    @blur="saveCurrentScript"
                    class="w-full px-4 py-2.5 bg-bg-main border border-border-base rounded-xl text-lg font-semibold focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all"
                    placeholder="腳本名稱"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-text-muted mb-2 text-indent-1"
                    >觸發熱鍵</label
                  >
                  <div class="relative group">
                    <input
                      v-model="selectedScript.hotkey"
                      @keydown="captureHotkey"
                      @focus="startCapture"
                      @blur="stopCapture"
                      class="w-full px-4 py-2.5 bg-bg-main border border-border-base rounded-xl font-mono text-primary focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all cursor-pointer"
                      placeholder="點擊以擷取熱鍵"
                      readonly
                    />
                    <div
                      class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-text-muted opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      自動記錄組合鍵
                    </div>
                  </div>
                </div>
              </div>

              <!-- 控制欄 -->
              <div
                class="flex flex-wrap items-center justify-between gap-4 mb-6 p-4 bg-bg-main/50 rounded-2xl border border-border-base border-dashed"
              >
                <div class="flex items-center gap-2">
                  <button
                    v-if="!isRecording"
                    @click="startRecording"
                    class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-xl font-medium transition-all flex items-center gap-2 group"
                  >
                    <span class="w-2 h-2 bg-white rounded-full group-hover:animate-ping"></span>
                    開始錄製
                  </button>
                  <button
                    v-else
                    @click="stopRecording"
                    class="px-4 py-2 bg-gray-600 text-white rounded-xl font-medium transition-all flex items-center gap-2 animate-pulse"
                  >
                    <span>⏹️</span>
                    停止錄製
                  </button>
                </div>

                <!-- 執行控制區 -->
                <div class="flex items-center gap-2">
                  <!-- 閒置狀態 -->
                  <button
                    v-if="engineStatus === 'IDLE'"
                    @click="handleExecute"
                    class="px-4 py-2 bg-primary/10 text-primary border border-primary/20 hover:bg-primary/20 rounded-xl font-medium transition-all flex items-center gap-2"
                    :disabled="engineLoading"
                  >
                    <span v-if="engineLoading" class="animate-spin">⌛</span>
                    <span v-else>▶️</span>
                    運行一次
                  </button>

                  <!-- 執行中狀態 -->
                  <template v-if="engineStatus === 'RUNNING'">
                    <button
                      @click="pauseEngine"
                      class="px-4 py-2 bg-yellow-500/10 text-yellow-600 border border-yellow-500/20 hover:bg-yellow-500/20 rounded-xl font-medium transition-all flex items-center gap-2"
                    >
                      <span>⏸️</span> 暫停
                    </button>
                    <button
                      @click="stopEngine"
                      class="px-4 py-2 bg-red-500/10 text-red-600 border border-red-500/20 hover:bg-red-500/20 rounded-xl font-medium transition-all flex items-center gap-2"
                    >
                      <span>⏹️</span> 停止
                    </button>
                  </template>

                  <!-- 暫停狀態 -->
                  <template v-if="engineStatus === 'PAUSED'">
                    <button
                      @click="resumeEngine"
                      class="px-4 py-2 bg-green-500/10 text-green-600 border border-green-500/20 hover:bg-green-500/20 rounded-xl font-medium transition-all flex items-center gap-2"
                    >
                      <span>▶️</span> 繼續
                    </button>
                    <button
                      @click="stopEngine"
                      class="px-4 py-2 bg-red-500/10 text-red-600 border border-red-500/20 hover:bg-red-500/20 rounded-xl font-medium transition-all flex items-center gap-2"
                    >
                      <span>⏹️</span> 停止
                    </button>
                  </template>

                  <div class="h-6 w-[1px] bg-border-base mx-2"></div>

                  <button
                    @click="deleteScript(selectedScript.id)"
                    class="p-2 text-red-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                    title="刪除"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="w-5 h-5"
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

              <!-- 編輯器區域 -->
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <QuickInsertBar
                    @insert="insertCode"
                    @insert-click="showClickModal = true"
                    @insert-key="showKeyModal = true"
                    @capture-position="captureMousePosition"
                  />
                </div>
                <div class="border border-border-base rounded-2xl overflow-hidden bg-bg-main p-1">
                  <div style="height: 450px" class="rounded-xl overflow-hidden shadow-inner">
                    <vue-monaco-editor
                      v-model:value="selectedScript.content"
                      language="python"
                      :theme="themeStore.isDarkMode ? 'vs-dark' : 'vs'"
                      :options="MONACO_EDITOR_OPTIONS"
                      @mount="handleMount"
                      @change="handleChange"
                    />
                  </div>
                </div>
              </div>

              <!-- 控制台面板 -->
              <div
                class="h-48 mt-4 border border-border-base rounded-2xl overflow-hidden shadow-sm"
              >
                <ConsolePanel @jump="handleJumpToIssue" />
              </div>
            </div>

            <!-- 未選擇狀態 -->
            <div
              v-else
              class="h-full min-h-[500px] flex flex-col items-center justify-center bg-bg-surface rounded-2xl border border-border-base border-dashed p-12 text-center"
            >
              <div
                class="w-20 h-20 bg-primary/5 rounded-full flex items-center justify-center mb-6"
              >
                <span class="text-4xl text-primary/40">📝</span>
              </div>
              <h3 class="text-2xl font-bold mb-2">啟動您的第一個腳本</h3>
              <p class="text-text-muted max-w-sm">
                從左側列表選擇現有腳本，或點擊「+」號建立新自動化任務。
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 全域模態框 -->
    <ClickModal v-model="showClickModal" @select="insertClickCode" />
    <KeyCaptureModal
      v-model="showKeyModal"
      :captured-key="capturedKey"
      @confirm="confirmKey"
      @cancel="cancelKeyCapture"
    />
    <PositionCapture :show="capturingPosition" />
    <ToastContainer />
    <ConfirmModal />
  </div>
</template>

<script setup lang="ts">
import { nextTick, shallowRef, watch } from 'vue';
import * as monaco from 'monaco-editor';
import type { editor } from 'monaco-editor';
import { useMonaco } from '@guolao/vue-monaco-editor';
import ScriptList from '../components/ScriptList.vue';
import QuickInsertBar from '../components/QuickInsertBar.vue';
import ClickModal from '../components/ClickModal.vue';
import KeyCaptureModal from '../components/KeyCaptureModal.vue';
import PositionCapture from '../components/PositionCapture.vue';
import ToastContainer from '../components/common/ToastContainer.vue';
import ConfirmModal from '../components/common/ConfirmModal.vue';
import ConsolePanel from '../components/ConsolePanel.vue';

// Stores
import { useThemeStore } from '../stores/theme';
const themeStore = useThemeStore();

// Composables
import { useScripts } from '../composables/useScripts';
import { useKeyListener } from '../composables/useKeyListener';
import { useRecorder } from '../composables/useRecorder';
import { useCodeInsertion } from '../composables/useCodeInsertion';
import { useHotkeyCapture } from '../composables/useHotkeyCapture';
import { useScriptEngine } from '../composables/useScriptEngine';
import { useScriptLinting } from '../composables/useScriptLinting';

// Monaco Editor 配置
const MONACO_EDITOR_OPTIONS = {
  automaticLayout: true,
  minimap: { enabled: false },
  fontSize: 14,
  wordWrap: 'on',
  tabSize: 4,
  formatOnPaste: true,
  quickSuggestions: true,
  parameterHints: { enabled: true },
};

const editorRef = shallowRef<editor.IStandaloneCodeEditor | null>(null);
let decorationsCollection: editor.IEditorDecorationsCollection | null = null; // Store decorations

const handleMount = (editor: editor.IStandaloneCodeEditor) => {
  editorRef.value = editor;
  decorationsCollection = editor.createDecorationsCollection([]);
};

// 使用 Composables
const {
  scripts,
  selectedScript,
  selectScript,
  createScript,
  saveCurrentScript,
  deleteScript,
  toggleScriptEnabled,
  checkCurrentScript,
} = useScripts();

const {
  status: engineStatus,
  loading: engineLoading,
  executeScript: runScriptEngine,
  stopEngine,
  pauseEngine,
  resumeEngine,
  currentLine,
  currentScriptId,
} = useScriptEngine();

// Watch for line changes to highlight
watch([currentLine, currentScriptId, selectedScript], ([line, runId, selScript]) => {
  if (!editorRef.value || !decorationsCollection) return;

  // Clear if not running or mismatch or invalid line
  if (!line || !runId || !selScript || runId !== selScript.id) {
    decorationsCollection.clear();
    return;
  }

  // Update Highlight
  decorationsCollection.set([
    {
      range: new monaco.Range(line, 1, line, 1),
      options: {
        isWholeLine: true,
        className: 'current-execution-line',
      },
    },
  ]);

  // Use revealLine instead of center to avoid jumpy behavior if possible, or center if far
  editorRef.value.revealLineInCenter(line, monaco.editor.ScrollType.Smooth);
});

const handleExecute = () => {
  if (selectedScript.value) {
    runScriptEngine(selectedScript.value.id, selectedScript.value.name);
  }
};

const { listenerRunning } = useKeyListener();

const { isRecording, startRecording, stopRecording } = useRecorder(selectedScript);

const {
  showClickModal,
  showKeyModal,
  capturingPosition,
  capturedKey,
  insertCode,
  insertClickCode,
  captureMousePosition,
  confirmKey,
  cancelKeyCapture,
} = useCodeInsertion(selectedScript, saveCurrentScript, editorRef);

const { captureHotkey, startCapture, stopCapture } = useHotkeyCapture(
  selectedScript,
  saveCurrentScript,
);

const { monacoRef } = useMonaco();

const { performCheck, handleChange, handleJumpToIssue } = useScriptLinting(
  editorRef,
  selectedScript,
  checkCurrentScript,
  monacoRef,
  saveCurrentScript,
);

// 監聽腳本切換，立即檢查
watch(
  () => selectedScript.value?.id,
  async (newId) => {
    if (newId) {
      await nextTick();
      performCheck();
    }
  },
);
</script>

<style>
.current-execution-line {
  background-color: rgba(234, 179, 8, 0.2);
  border-left: 3px solid #eab308;
}
</style>
