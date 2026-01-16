"""
系統相關 API 路由
包括執行、錄製、歷史記錄、監聽器等
"""

import asyncio
import contextlib

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from core.engine import ScriptEngine
from core.key_listener import KeyListener
from core.recorder import ScriptRecorder
from models.schemas import (
    EngineCommandResponse,
    EngineStatus,
    ExecutionResult,
    MousePosition,
    RecorderStatus,
    StatusResponse,
)
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


# WebSocket 連線管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            with contextlib.suppress(Exception):
                await connection.send_json(message)


manager = ConnectionManager()


def on_f2_triggered():
    """當 F2 被按下時的回呼"""
    pos = script_engine.get_mouse_position()
    # 建立事件迴圈來發送非同步廣播 (在 KeyListener 的執行緒中)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        manager.broadcast({"type": "coordinate", "data": {"x": pos[0], "y": pos[1]}})
    )
    loop.close()


key_listener = KeyListener(
    on_trigger=lambda content: script_engine.execute(content, "hotkey"), on_f2=on_f2_triggered
)


@router.websocket("/ws/system")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # 保持連線, 接收訊息(如果需要)
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)


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

    result = script_engine.execute(script.content, script_id, script.name)
    return ExecutionResult(**result)


@router.post("/engine/stop", response_model=EngineCommandResponse)
def stop_execution():
    """停止執行腳本"""
    return script_engine.stop()


@router.post("/engine/pause", response_model=EngineCommandResponse)
def pause_execution():
    """暫停執行腳本"""
    return script_engine.pause()


@router.post("/engine/resume", response_model=EngineCommandResponse)
def resume_execution():
    """恢復執行腳本"""
    return script_engine.resume()


@router.get("/engine/status", response_model=EngineStatus)
def get_engine_status():
    """取得引擎狀態"""
    return script_engine.get_status()


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
