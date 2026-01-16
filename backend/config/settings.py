"""
配置管理
集中管理所有應用配置
"""
import os
from pathlib import Path

# 基礎路徑
BASE_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
HISTORY_FILE = SCRIPTS_DIR / "history.json"
SCRIPTS_FILE = SCRIPTS_DIR / "scripts.json"

# API 配置
API_TITLE = "XXScript Backend"
API_HOST = "127.0.0.1"
API_PORT = 8000

# CORS 配置
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# 歷史記錄配置
MAX_HISTORY_RECORDS = 100

# 錄製配置
RECORDER_MIN_DELAY = 0.05  # 最小延遲閾值 (秒)
RECORDER_MOVE_THRESHOLD = 10  # 滑鼠移動距離閾值 (像素)

# 確保目錄存在
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
