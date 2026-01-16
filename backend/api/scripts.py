"""
腳本相關 API 路由
"""

from fastapi import APIRouter, HTTPException

# 引用刷新監聽器的函數 (延遲引用或直接引用，這裡直接引用，因為 system.py 不依賴 scripts.py)
from api.system import refresh_listener_hotkeys
from models.schemas import (
    Script,
    ScriptCheckRequest,
    ScriptCheckResponse,
    ScriptCreate,
    ScriptUpdate,
)
from repositories.script_repository import ScriptRepository
from services.script_service import ScriptService

router = APIRouter(prefix="/scripts", tags=["scripts"])

# 依賴注入 - 創建服務實例
script_repository = ScriptRepository()
script_service = ScriptService(script_repository)


@router.get("", response_model=list[Script])
def get_scripts():
    """取得所有腳本"""
    return script_service.get_all_scripts()


@router.post("", response_model=Script)
def create_script(script: ScriptCreate):
    """建立新腳本"""
    result = script_service.create_script(script)
    refresh_listener_hotkeys()
    return result


@router.post("/check", response_model=ScriptCheckResponse)
def check_script(request: ScriptCheckRequest):
    """檢查腳本代碼"""
    issues = script_service.check_script(request.content)
    return ScriptCheckResponse(issues=issues)


@router.get("/{script_id}", response_model=Script)
def get_script(script_id: str):
    """取得特定腳本"""
    script = script_service.get_script(script_id)
    if not script:
        raise HTTPException(status_code=404, detail="腳本不存在")
    return script


@router.put("/{script_id}", response_model=Script)
def update_script(script_id: str, update: ScriptUpdate):
    """更新腳本"""
    script = script_service.update_script(script_id, update)
    if not script:
        raise HTTPException(status_code=404, detail="腳本不存在")
    refresh_listener_hotkeys()
    return script


@router.delete("/{script_id}")
def delete_script(script_id: str):
    """刪除腳本"""
    success = script_service.delete_script(script_id)
    if not success:
        raise HTTPException(status_code=404, detail="腳本不存在")
    refresh_listener_hotkeys()
    return {"status": "ok", "message": "腳本已刪除"}
