"""
歷史記錄服務
處理腳本執行歷史的記錄和查詢
"""

import json
from datetime import datetime
from pathlib import Path

from config.settings import HISTORY_FILE, MAX_HISTORY_RECORDS


class HistoryService:
    """歷史記錄服務類"""

    def __init__(self, history_file: Path = HISTORY_FILE):
        """
        初始化歷史記錄服務

        Args:
            history_file: 歷史記錄文件路徑
        """
        self.history_file = history_file
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """確保歷史記錄文件存在"""
        if not self.history_file.exists():
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            self._save_history([])

    def _load_history(self) -> list[dict]:
        """載入歷史記錄"""
        try:
            with self.history_file.open(encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_history(self, history: list[dict]) -> None:
        """儲存歷史記錄"""
        with self.history_file.open("w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def add_record(
        self, script_id: str, status: str, duration: float, error: str | None = None
    ) -> None:
        """
        添加執行記錄

        Args:
            script_id: 腳本 ID
            status: 執行狀態 (success/error)
            duration: 執行時長
            error: 錯誤訊息 (可選)
        """
        history = self._load_history()

        record = {
            "script_id": script_id,
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "duration": round(duration, 3),
            "error": error,
        }

        history.append(record)

        # 只保留最近的記錄
        if len(history) > MAX_HISTORY_RECORDS:
            history = history[-MAX_HISTORY_RECORDS:]

        self._save_history(history)

    def get_all(self) -> list[dict]:
        """取得所有歷史記錄"""
        return self._load_history()

    def clear(self) -> None:
        """清除所有歷史記錄"""
        if self.history_file.exists():
            self.history_file.unlink()
            self._ensure_file_exists()
