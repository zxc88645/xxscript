"""
腳本執行引擎
提供安全的腳本執行環境與預定義的 API
"""
import time
import json
import os
from datetime import datetime
from typing import List, Dict
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

class ScriptEngine:
    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.running = False
        self.history_file = os.path.join(os.path.dirname(__file__), "scripts", "history.json")
        
    def execute(self, script_content: str, script_id: str = "manual"):
        """執行腳本內容"""
        start_time = time.time()
        try:
            # 建立安全的執行環境
            safe_globals = {
                'click': self.click,
                'move': self.move,
                'press': self.press,
                'type_text': self.type_text,
                'sleep': time.sleep,
                'mouse_position': self.get_mouse_position,
                # 羅技風格的 down/release 函式
                'key_down': self.key_down,
                'key_release': self.key_release,
                'mouse_down': self.mouse_down,
                'mouse_release': self.mouse_release,
            }
            
            self.running = True
            exec(script_content, safe_globals)
            self.running = False
            
            # 記錄執行歷史
            duration = time.time() - start_time
            self._add_history(script_id, "success", duration)
            
            return {"status": "success", "message": "腳本執行完成"}
        except Exception as e:
            self.running = False
            
            # 記錄執行失敗
            duration = time.time() - start_time
            self._add_history(script_id, "error", duration, str(e))
            
            return {"status": "error", "message": str(e)}
    
    def _add_history(self, script_id: str, status: str, duration: float, error: str = None):
        """新增執行歷史記錄"""
        history = self.get_history()
        
        history.append({
            'script_id': script_id,
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'duration': round(duration, 3),
            'error': error
        })
        
        # 只保留最近 100 筆記錄
        if len(history) > 100:
            history = history[-100:]
        
        # 儲存到檔案
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def get_history(self) -> List[Dict]:
        """取得執行歷史"""
        if not os.path.exists(self.history_file):
            return []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def clear_history(self):
        """清除執行歷史"""
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
    
    def click(self, button='left', count=1):
        """點擊滑鼠"""
        btn = Button.left if button == 'left' else Button.right
        for _ in range(count):
            self.mouse.click(btn)
    
    def move(self, x: int, y: int):
        """移動滑鼠到絕對位置"""
        self.mouse.position = (x, y)
    
    def press(self, key: str, duration: float = 0.05):
        """按下鍵盤按鍵 (包含按下、延遲、釋放)"""
        try:
            # 嘗試特殊鍵
            special_key = getattr(Key, key.lower(), None)
            if special_key:
                self.keyboard.press(special_key)
                time.sleep(duration)  # 按住延遲
                self.keyboard.release(special_key)
            else:
                # 普通字元
                self.keyboard.press(key)
                time.sleep(duration)  # 按住延遲
                self.keyboard.release(key)
        except Exception as e:
            print(f"按鍵錯誤: {e}")
    
    def type_text(self, text: str):
        """輸入文字"""
        self.keyboard.type(text)
    
    def get_mouse_position(self):
        """取得滑鼠位置"""
        return self.mouse.position
    
    # 羅技風格的 down/release 函式
    def key_down(self, key: str):
        """按下鍵盤按鍵 (不釋放)"""
        try:
            special_key = getattr(Key, key.lower(), None)
            if special_key:
                self.keyboard.press(special_key)
            else:
                self.keyboard.press(key)
        except Exception as e:
            print(f"按鍵按下錯誤: {e}")
    
    def key_release(self, key: str):
        """釋放鍵盤按鍵"""
        try:
            special_key = getattr(Key, key.lower(), None)
            if special_key:
                self.keyboard.release(special_key)
            else:
                self.keyboard.release(key)
        except Exception as e:
            print(f"按鍵釋放錯誤: {e}")
    
    def mouse_down(self, button='left'):
        """按下滑鼠按鈕 (不釋放)"""
        btn = Button.left if button == 'left' else Button.right
        self.mouse.press(btn)
    
    def mouse_release(self, button='left'):
        """釋放滑鼠按鈕"""
        btn = Button.left if button == 'left' else Button.right
        self.mouse.release(btn)
