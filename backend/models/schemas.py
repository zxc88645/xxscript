"""
數據模型定義
使用 Pydantic 進行數據驗證
"""

from typing import Literal

from pydantic import BaseModel, Field


class ScriptBase(BaseModel):
    """腳本基礎模型"""

    name: str = Field(..., min_length=1, max_length=100, description="腳本名稱")
    content: str = Field(default="", description="腳本內容")
    hotkey: str | None = Field(None, max_length=50, description="觸發熱鍵")


class ScriptCreate(ScriptBase):
    """創建腳本請求模型"""

    pass


class ScriptUpdate(BaseModel):
    """更新腳本請求模型"""

    name: str | None = Field(None, min_length=1, max_length=100)
    content: str | None = None
    hotkey: str | None = Field(None, max_length=50)
    enabled: bool | None = None


class Script(ScriptBase):
    """腳本完整模型"""

    id: str = Field(..., description="腳本唯一標識")
    enabled: bool = Field(default=True, description="是否啟用")

    class Config:
        from_attributes = True


class ExecutionResult(BaseModel):
    """執行結果模型"""

    status: str = Field(..., description="執行狀態: success/error")
    message: str = Field(..., description="執行訊息")


class HistoryRecord(BaseModel):
    """歷史記錄模型"""

    script_id: str
    timestamp: str
    status: str
    duration: float
    error: str | None = None


class RecorderStatus(BaseModel):
    """錄製器狀態模型"""

    recording: bool
    event_count: int
    duration: float


class MousePosition(BaseModel):
    """滑鼠位置模型"""

    x: int
    y: int


class StatusResponse(BaseModel):
    """系統狀態響應模型"""

    status: str
    message: str
    listener_running: bool


class ScriptCheckRequest(BaseModel):
    """代碼檢查請求"""

    content: str = Field(..., description="待檢查的腳本內容")


class ScriptCheckIssue(BaseModel):
    """代碼檢查問題"""

    line: int
    column: int
    message: str
    severity: Literal["error", "warning", "info", "hint"]
    code: str | None = None
    script_context: str | None = None


class ScriptCheckResponse(BaseModel):
    """代碼檢查響應"""

    issues: list[ScriptCheckIssue]


class EngineStatus(BaseModel):
    """引擎狀態模型"""

    status: Literal["IDLE", "RUNNING", "PAUSED"]
    script_id: str | None = None
    script_name: str | None = None
    current_line: int | None = None


class EngineCommandResponse(BaseModel):
    """引擎控制指令響應"""

    status: str
    message: str
