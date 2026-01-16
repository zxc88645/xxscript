<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
    <!-- 頂部導航欄 -->
    <nav class="bg-black/30 backdrop-blur-lg border-b border-white/10">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div
              class="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center"
            >
              <span class="text-white font-bold text-xl">XX</span>
            </div>
            <h1 class="text-2xl font-bold text-white">XXScript</h1>
          </div>

          <div class="flex items-center gap-4">
            <div class="flex items-center gap-2">
              <div
                :class="[
                  'w-2 h-2 rounded-full',
                  listenerRunning ? 'bg-green-400 animate-pulse' : 'bg-red-400',
                ]"
              ></div>
              <span class="text-sm text-gray-300">{{ listenerRunning ? '監聽中' : '已停止' }}</span>
            </div>
            <button
              @click="toggleListener"
              :class="[
                'px-4 py-2 rounded-lg font-medium transition-all',
                listenerRunning
                  ? 'bg-red-500 hover:bg-red-600 text-white'
                  : 'bg-green-500 hover:bg-green-600 text-white',
              ]"
            >
              {{ listenerRunning ? '停止監聽' : '啟動監聽' }}
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要內容 -->
    <div class="max-w-7xl mx-auto px-6 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 左側:腳本列表 -->
        <div class="lg:col-span-1">
          <div class="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold text-white">腳本列表</h2>
              <button
                @click="createScript"
                class="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white rounded-lg font-medium transition-all"
              >
                + 新增
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
        <div class="lg:col-span-2">
          <div
            v-if="selectedScript"
            class="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-6"
          >
            <!-- 腳本資訊 -->
            <div class="mb-6">
              <input
                v-model="selectedScript.name"
                @blur="saveCurrentScript"
                class="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white text-xl font-semibold focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="腳本名稱"
              />
            </div>

            <!-- 熱鍵設定 -->
            <div class="mb-4">
              <label class="block text-sm text-gray-400 mb-2">觸發熱鍵</label>
              <input
                v-model="selectedScript.hotkey"
                @keydown="captureHotkey"
                @focus="startCapture"
                @blur="stopCapture"
                class="w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-white font-mono focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="點擊後按下組合鍵 (例: Ctrl+Shift+F1)"
                readonly
              />
            </div>

            <!-- 錄製按鈕 -->
            <div class="mb-4 flex gap-2">
              <button
                v-if="!isRecording"
                @click="startRecording"
                class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg font-medium transition-all"
              >
                🔴 開始錄製
              </button>
              <button
                v-else
                @click="stopRecording"
                class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg font-medium transition-all animate-pulse"
              >
                ⏹️ 停止錄製
              </button>
              <button
                @click="executeScript(selectedScript.id)"
                class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium transition-all"
              >
                ▶️ 執行
              </button>
              <button
                @click="deleteScript(selectedScript.id)"
                class="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 border border-red-500 rounded-lg font-medium transition-all"
              >
                🗑️ 刪除
              </button>
            </div>

            <!-- 程式碼編輯器 -->
            <div class="mb-4">
              <div class="flex items-center justify-between mb-2">
                <label class="block text-sm text-gray-400">腳本內容 (Python)</label>
                <QuickInsertBar
                  @insert="insertCode"
                  @insert-click="showClickModal = true"
                  @insert-key="showKeyModal = true"
                  @capture-position="captureMousePosition"
                />
              </div>
              <div class="border border-white/20 rounded-lg overflow-hidden" style="height: 400px">
                <vue-monaco-editor
                  v-model:value="selectedScript.content"
                  language="python"
                  theme="vs-dark"
                  :options="MONACO_EDITOR_OPTIONS"
                  @change="saveCurrentScript"
                />
              </div>
            </div>
          </div>

          <!-- 未選擇腳本時的提示 -->
          <div
            v-else
            class="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-12 text-center"
          >
            <div class="text-6xl mb-4">📝</div>
            <h3 class="text-xl font-semibold text-white mb-2">選擇或建立一個腳本</h3>
            <p class="text-gray-400">從左側列表選擇腳本,或點擊「新增」建立新腳本</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 模態框 -->
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
import ScriptList from './components/ScriptList.vue';
import QuickInsertBar from './components/QuickInsertBar.vue';
import ClickModal from './components/ClickModal.vue';
import KeyCaptureModal from './components/KeyCaptureModal.vue';
import PositionCapture from './components/PositionCapture.vue';

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
} = useCodeInsertion(selectedScript, saveCurrentScript);

const { captureHotkey, startCapture, stopCapture } = useHotkeyCapture(
  selectedScript,
  saveCurrentScript,
);
</script>
