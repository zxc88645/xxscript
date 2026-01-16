/**
 * TypeScript 類型定義
 * 統一管理所有前端類型
 */

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

export interface RecorderStatus {
  recording: boolean;
  event_count: number;
  duration: number;
}

export interface MousePosition {
  x: number;
  y: number;
}

export interface ExecutionResult {
  status: string;
  message: string;
}

export interface HistoryRecord {
  script_id: string;
  timestamp: string;
  status: string;
  duration: number;
  error?: string;
}

export interface StatusResponse {
  status: string;
  message: string;
  listener_running: boolean;
}

export interface ScriptCheckIssue {
  line: number;
  column: number;
  message: string;
  severity: 'error' | 'warning' | 'info' | 'hint';
  code?: string;
  script_context?: string;
}

export interface ScriptCheckResponse {
  issues: ScriptCheckIssue[];
}
