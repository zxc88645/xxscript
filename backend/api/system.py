"""
系統相關 API 路由
包括執行、錄製、歷史記錄、監聽器等
"""

from fastapi import APIRouter, HTTPException

from core.engine import ScriptEngine
from core.key_listener import KeyListener
from core.recorder import ScriptRecorder
from models.schemas import ExecutionResult, MousePosition, RecorderStatus, StatusResponse
from repositories.script_repository import ScriptRepository
from services.history_service import HistoryService
from services.script_service import ScriptService

router = APIRouter(tags=["system"])

# 全局實例 (保持向後兼容)
script_engine = ScriptEngine()
recorder = ScriptRecorder()
history_service = HistoryService()
script_repository = ScriptRepository()
script_service = ScriptService(script_repository)
key_listener = KeyListener(on_trigger=lambda content: script_engine.execute(content, "hotkey"))


@router.get("/", response_model=StatusResponse)
def get_status():
    """取得系統狀態"""
    return StatusResponse(
        status="ok", message="XXScript Backend Running", listener_running=key_listener.running
    )


@router.post("/scripts/{script_id}/execute", response_model=ExecutionResult)
def execute_script(script_id: str):
    """執行腳本"""
    script = script_service.get_script(script_id)
    if not script:
        raise HTTPException(status_code=404, detail="腳本不存在")

    result = script_engine.execute(script.content, script_id)
    return ExecutionResult(**result)


@router.post("/recorder/start")
def start_recording():
    """開始錄製"""
    recorder.start_recording()
    return {"status": "ok", "message": "開始錄製"}


@router.post("/recorder/stop")
def stop_recording():
    """停止錄製"""
    script_content = recorder.stop_recording()
    return {"status": "ok", "script": script_content}


@router.get("/recorder/status", response_model=RecorderStatus)
def get_recorder_status():
    """取得錄製狀態"""
    status = recorder.get_status()
    return RecorderStatus(**status)


@router.get("/history")
def get_history():
    """取得執行歷史"""
    return history_service.get_all()


@router.delete("/history")
def clear_history():
    """清除執行歷史"""
    history_service.clear()
    return {"status": "ok", "message": "歷史記錄已清除"}


@router.get("/mouse/position", response_model=MousePosition)
def get_mouse_position():
    """取得滑鼠位置"""
    position = script_engine.get_mouse_position()
    return MousePosition(x=position[0], y=position[1])


@router.post("/listener/start")
def start_listener():
    """啟動監聽器"""
    if not key_listener.running:
        # 同步熱鍵
        enabled_scripts = script_service.get_enabled_scripts()
        key_listener.clear_all()
        for script in enabled_scripts:
            if script.hotkey:
                key_listener.register_hotkey(script.hotkey, script.id, script.content)
        key_listener.start()
    return {"status": "ok", "message": "監聽器已啟動"}


@router.post("/listener/stop")
def stop_listener():
    """停止監聽器"""
    key_listener.stop()
    return {"status": "ok", "message": "監聽器已停止"}
