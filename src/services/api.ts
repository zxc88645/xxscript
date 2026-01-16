// API 服務層
import axios from 'axios';
import type { ScriptCheckIssue } from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Script {
  id: string;
  name: string;
  content: string;
  hotkey?: string;
  enabled: boolean;
}

export interface ScriptCreate {
  name: string;
  content: string;
  hotkey?: string;
}

export interface ScriptUpdate {
  name?: string;
  content?: string;
  hotkey?: string;
  enabled?: boolean;
}

export const scriptApi = {
  // 取得所有腳本
  getScripts: () => api.get<Script[]>('/scripts'),

  // 取得單一腳本
  getScript: (id: string) => api.get<Script>(`/scripts/${id}`),

  // 建立腳本
  createScript: (data: ScriptCreate) => api.post<Script>('/scripts', data),

  // 更新腳本
  updateScript: (id: string, data: ScriptUpdate) => api.put<Script>(`/scripts/${id}`, data),

  // 刪除腳本
  deleteScript: (id: string) => api.delete(`/scripts/${id}`),

  // 執行腳本
  executeScript: (id: string) => api.post(`/scripts/${id}/execute`),

  // 啟動監聽器
  startListener: () => api.post('/listener/start'),

  // 停止監聽器
  stopListener: () => api.post('/listener/stop'),

  // 取得狀態
  getStatus: () => api.get('/'),

  // 錄製 API
  startRecording: () => api.post('/recorder/start'),
  stopRecording: () => api.post<{ status: string; script: string }>('/recorder/stop'),
  getRecorderStatus: () =>
    api.get<{ recording: boolean; event_count: number; duration: number }>('/recorder/status'),

  // 歷史記錄 API
  getHistory: () => api.get('/history'),
  clearHistory: () => api.delete('/history'),

  // 滑鼠位置 API
  getMousePosition: () => api.get<{ x: number; y: number }>('/mouse/position'),

  // 引擎控制 API
  getEngineStatus: () =>
    api.get<{
      status: 'IDLE' | 'RUNNING' | 'PAUSED';
      script_id: string | null;
      script_name: string | null;
      current_line: number | null;
    }>('/engine/status'),
  stopEngine: () => api.post<{ status: string; message: string }>('/engine/stop'),
  pauseEngine: () => api.post<{ status: string; message: string }>('/engine/pause'),
  resumeEngine: () => api.post<{ status: string; message: string }>('/engine/resume'),

  // 檢查腳本
  checkScript: (content: string) =>
    api.post<{ issues: ScriptCheckIssue[] }>('/scripts/check', { content }),
};
