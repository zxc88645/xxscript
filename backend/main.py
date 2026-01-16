"""
XXScript Backend - 重構版本
遵循 SOLID 原則的分層架構
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.settings import (
    API_TITLE,
    CORS_ORIGINS,
    CORS_CREDENTIALS,
    CORS_METHODS,
    CORS_HEADERS
)
from api import scripts, system


@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用生命週期管理"""
    # 啟動時
    print("🚀 XXScript Backend 啟動中...")
    # 啟動監聽器
    from api.system import key_listener, script_service
    enabled_scripts = script_service.get_enabled_scripts()
    key_listener.clear_all()
    for script in enabled_scripts:
        if script.hotkey:
            key_listener.register_hotkey(script.hotkey, script.id, script.content)
    key_listener.start()
    print("✅ 按鍵監聽器已啟動")
    
    yield
    
    # 關閉時
    print("🛑 XXScript Backend 關閉中...")
    key_listener.stop()
    print("✅ 按鍵監聽器已停止")


# 創建 FastAPI 應用
app = FastAPI(title=API_TITLE, lifespan=lifespan)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# 註冊路由
app.include_router(scripts.router)
app.include_router(system.router)


if __name__ == "__main__":
    import uvicorn
    from config.settings import API_HOST, API_PORT
    
    uvicorn.run(
        "main_refactored:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )
