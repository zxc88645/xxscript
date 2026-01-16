"""
腳本業務邏輯層
處理腳本相關的業務邏輯
"""
from typing import List, Optional

from models.schemas import Script, ScriptCreate, ScriptUpdate
from repositories.script_repository import ScriptRepository


class ScriptService:
    """腳本服務類 - 處理腳本相關業務邏輯"""
    
    def __init__(self, repository: ScriptRepository):
        """
        初始化腳本服務
        
        Args:
            repository: 腳本數據倉庫實例
        """
        self.repository = repository
    
    def get_all_scripts(self) -> List[Script]:
        """取得所有腳本"""
        return self.repository.get_all()
    
    def get_script(self, script_id: str) -> Optional[Script]:
        """
        根據 ID 取得腳本
        
        Args:
            script_id: 腳本 ID
            
        Returns:
            腳本對象或 None
        """
        return self.repository.get_by_id(script_id)
    
    def create_script(self, script_data: ScriptCreate) -> Script:
        """
        創建新腳本
        
        Args:
            script_data: 腳本創建數據
            
        Returns:
            創建的腳本對象
        """
        return self.repository.create(script_data)
    
    def update_script(self, script_id: str, update_data: ScriptUpdate) -> Optional[Script]:
        """
        更新腳本
        
        Args:
            script_id: 腳本 ID
            update_data: 更新數據
            
        Returns:
            更新後的腳本對象或 None
        """
        return self.repository.update(script_id, update_data)
    
    def delete_script(self, script_id: str) -> bool:
        """
        刪除腳本
        
        Args:
            script_id: 腳本 ID
            
        Returns:
            是否刪除成功
        """
        return self.repository.delete(script_id)
    
    def get_enabled_scripts(self) -> List[Script]:
        """取得所有啟用的腳本"""
        return self.repository.get_enabled_scripts()
