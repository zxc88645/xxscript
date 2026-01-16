"""
腳本數據訪問層
負責腳本的持久化操作
"""
import json
from typing import List, Optional
from pathlib import Path

from models.schemas import Script, ScriptCreate, ScriptUpdate
from config.settings import SCRIPTS_FILE


class ScriptRepository:
    """腳本倉庫類 - 處理腳本數據的 CRUD 操作"""
    
    def __init__(self, storage_file: Path = SCRIPTS_FILE):
        self.storage_file = storage_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """確保儲存文件存在"""
        if not self.storage_file.exists():
            self.storage_file.parent.mkdir(parents=True, exist_ok=True)
            self._save_scripts([])
    
    def _load_scripts(self) -> List[dict]:
        """從文件載入腳本數據"""
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_scripts(self, scripts: List[dict]) -> None:
        """儲存腳本數據到文件"""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(scripts, f, ensure_ascii=False, indent=2)
    
    def get_all(self) -> List[Script]:
        """取得所有腳本"""
        data = self._load_scripts()
        return [Script(**item) for item in data]
    
    def get_by_id(self, script_id: str) -> Optional[Script]:
        """根據 ID 取得腳本"""
        scripts = self.get_all()
        for script in scripts:
            if script.id == script_id:
                return script
        return None
    
    def create(self, script_data: ScriptCreate) -> Script:
        """創建新腳本"""
        scripts_data = self._load_scripts()
        
        # 生成唯一 ID
        script_id = f"script_{len(scripts_data) + 1}"
        
        new_script = Script(
            id=script_id,
            name=script_data.name,
            content=script_data.content,
            hotkey=script_data.hotkey,
            enabled=True
        )
        
        scripts_data.append(new_script.model_dump())
        self._save_scripts(scripts_data)
        
        return new_script
    
    def update(self, script_id: str, update_data: ScriptUpdate) -> Optional[Script]:
        """更新腳本"""
        scripts_data = self._load_scripts()
        
        for i, script_dict in enumerate(scripts_data):
            if script_dict['id'] == script_id:
                # 只更新提供的字段
                if update_data.name is not None:
                    script_dict['name'] = update_data.name
                if update_data.content is not None:
                    script_dict['content'] = update_data.content
                if update_data.hotkey is not None:
                    script_dict['hotkey'] = update_data.hotkey
                if update_data.enabled is not None:
                    script_dict['enabled'] = update_data.enabled
                
                scripts_data[i] = script_dict
                self._save_scripts(scripts_data)
                
                return Script(**script_dict)
        
        return None
    
    def delete(self, script_id: str) -> bool:
        """刪除腳本"""
        scripts_data = self._load_scripts()
        original_length = len(scripts_data)
        
        scripts_data = [s for s in scripts_data if s['id'] != script_id]
        
        if len(scripts_data) < original_length:
            self._save_scripts(scripts_data)
            return True
        
        return False
    
    def get_enabled_scripts(self) -> List[Script]:
        """取得所有啟用的腳本"""
        all_scripts = self.get_all()
        return [s for s in all_scripts if s.enabled and s.hotkey]
