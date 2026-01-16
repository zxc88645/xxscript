<template>
  <div class="flex min-h-screen bg-bg-main">
    <!-- 側邊欄 -->
    <AppSidebar />

    <!-- 主要內容區 -->
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
              狀態：{{ listenerRunning ? '監聽中' : '已停止' }}
            </span>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <button
            @click="toggleListener"
            :class="[
              'px-4 py-2 rounded-xl font-medium transition-all flex items-center gap-2',
              listenerRunning
                ? 'bg-red-500 hover:bg-red-600 text-white'
                : 'bg-green-500 hover:bg-green-600 text-white',
            ]"
          >
            <span v-if="listenerRunning">⏹️</span>
            <span v-else>▶️</span>
            {{ listenerRunning ? '停止監聽' : '啟動監聽' }}
          </button>
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
                    @click="() => createScript()"
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

                  <div class="flex items-center gap-2">
                    <button
                      @click="executeScript(selectedScript.id)"
                      class="px-4 py-2 bg-primary/10 text-primary border border-primary/20 hover:bg-primary/20 rounded-xl font-medium transition-all flex items-center gap-2"
                    >
                      <span>▶️</span> 快速模擬
                    </button>
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
                    <label class="text-sm font-medium text-text-muted">程式碼邏輯 (Python)</label>
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
                        @change="saveCurrentScript"
                      />
                    </div>
                  </div>
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
    </div>

    <!-- 全域模態框 -->
    <ClickModal v-model="showClickModal" @select="insertClickCode" />
    <KeyCaptureModal
      v-model="showKeyModal"
      :captured-key="capturedKey"
      @confirm="confirmKey"
      @cancel="cancelKeyCapture"
    />
    <PositionCapture :show="capturingPosition" />
  </div>
</template>

<script setup lang="ts">
import { shallowRef } from 'vue';
import type { editor } from 'monaco-editor';
import AppSidebar from './components/AppSidebar.vue';
import ScriptList from './components/ScriptList.vue';
import QuickInsertBar from './components/QuickInsertBar.vue';
import ClickModal from './components/ClickModal.vue';
import KeyCaptureModal from './components/KeyCaptureModal.vue';
import PositionCapture from './components/PositionCapture.vue';

// Stores
import { useThemeStore } from './stores/theme';
const themeStore = useThemeStore();

// Composables
import { useScripts } from './composables/useScripts';
import { useKeyListener } from './composables/useKeyListener';
import { useRecorder } from './composables/useRecorder';
import { useCodeInsertion } from './composables/useCodeInsertion';
import { useHotkeyCapture } from './composables/useHotkeyCapture';

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
const handleMount = (editor: editor.IStandaloneCodeEditor) => {
  editorRef.value = editor;
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
  executeScript,
} = useScripts();

const { listenerRunning, toggleListener } = useKeyListener();

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
</script>
