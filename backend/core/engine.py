import json
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController


class ScriptStoppedError(Exception):
    """腳本停止例外"""

    pass


class ScriptEngine:
    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.history_file = Path(__file__).parent / "scripts" / "history.json"

        # 執行狀態控制
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.set()  # 預設為非暫停狀態
        self._execution_thread = None

        # 公開狀態
        self.status = "IDLE"  # IDLE, RUNNING, PAUSED
        self.current_script_id = None
        self.current_script_name = None
        self.current_line = 0

    def execute(
        self, script_content: str, script_id: str = "manual", script_name: str = "手動執行"
    ):
        """
        非同步執行腳本
        """
        if self.status != "IDLE":
            return {"status": "error", "message": "已有腳本正在執行中"}

        self.status = "RUNNING"
        self.current_script_id = script_id
        self.current_script_name = script_name
        self.current_line = 0  # 重置行號
        self._stop_event.clear()
        self._pause_event.set()

        def run_script():
            start_time = time.time()
            status = "success"
            error_msg = None

            # 建立安全的執行環境
            safe_globals = {
                "click": self.click,
                "move": self.move,
                "press": self.press,
                "type_text": self.type_text,
                "scroll": self.scroll,
                "print": print,
                "sleep": self.sleep,  # 使用可中斷的 sleep
                "mouse_position": self.get_mouse_position,
                "key_down": self.key_down,
                "key_release": self.key_release,
                "mouse_down": self.mouse_down,
                "mouse_release": self.mouse_release,
            }

            # 移除 settrace 以避免效能問題和潛在的死鎖
            # 依賴 API 函數內的 _check_state 來處理停止和暫停
            # def trace_func(frame, event, arg):
            #     if self._stop_event.is_set():
            #         raise ScriptStoppedError()
            #     self._pause_event.wait()  # 如果暫停，這裡會阻塞
            #     return trace_func

            try:
                # sys.settrace(trace_func)
                exec(script_content, safe_globals)
            except ScriptStoppedError:
                status = "stopped"
                print("腳本已停止")
            except Exception as e:
                status = "error"
                error_msg = str(e)
                print(f"腳本執行錯誤: {e}")
            finally:
                # sys.settrace(None)
                self.status = "IDLE"
                self.current_script_id = None
                self.current_line = 0

                # 記錄執行歷史
                duration = time.time() - start_time
                self._add_history(script_id, status, duration, error_msg)
                print(f"腳本執行完成執行結束，狀態: {status}，耗時: {duration:.8f} 秒")

        self._execution_thread = threading.Thread(target=run_script)
        self._execution_thread.daemon = True
        self._execution_thread.start()

        return {"status": "running", "message": "腳本開始執行"}

    def stop(self):
        """停止執行"""
        if self.status == "IDLE":
            return {"status": "warning", "message": "沒有正在執行的腳本"}

        self._stop_event.set()
        self._pause_event.set()  # 確保如果暫停中也能繼續並檢測到停止
        return {"status": "success", "message": "已發送停止信號"}

    def pause(self):
        """暫停執行"""
        if self.status != "RUNNING":
            return {"status": "warning", "message": "腳本未在執行中"}

        self.status = "PAUSED"
        self._pause_event.clear()
        return {"status": "success", "message": "腳本已暫停"}

    def resume(self):
        """繼續執行"""
        if self.status != "PAUSED":
            return {"status": "warning", "message": "腳本未暫停"}

        self.status = "RUNNING"
        self._pause_event.set()
        return {"status": "success", "message": "腳本已繼續"}

    def get_status(self):
        """取得目前狀態"""
        return {
            "status": self.status,
            "script_id": self.current_script_id,
            "script_name": self.current_script_name,
            "current_line": self.current_line,
        }

    def _add_history(self, script_id: str, status: str, duration: float, error: str | None = None):
        """新增執行歷史記錄"""
        history = self.get_history()

        history.append(
            {
                "script_id": script_id,
                "timestamp": datetime.now().isoformat(),
                "status": status,
                "duration": round(duration, 3),
                "error": error,
            }
        )

        # 只保留最近 100 筆記錄
        if len(history) > 100:
            history = history[-100:]

        # 儲存到檔案
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with self.history_file.open("w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def get_history(self) -> list[dict]:
        """取得執行歷史"""
        if not self.history_file.exists():
            return []

        try:
            with self.history_file.open(encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError, OSError):
            return []

    def clear_history(self):
        """清除執行歷史"""
        if self.history_file.exists():
            self.history_file.unlink()

    def _update_line(self):
        """更新當前行號"""
        try:
            # frame 0: _update_line
            # frame 1: API method (e.g. sleep)
            # frame 2: script content
            frame = sys._getframe(2)
            self.current_line = frame.f_lineno
            # print(f"執行行號: {self.current_line}")
        except Exception:
            pass

    def _check_state(self):
        """手動檢查狀態 (用於 API 函數內部)"""
        if self._stop_event.is_set():
            raise ScriptStoppedError()
        self._pause_event.wait()

    def sleep(self, seconds: float):
        """可中斷的睡眠"""
        self._update_line()
        start = time.time()
        while time.time() - start < seconds:
            self._check_state()
            # 短暫睡眠以允許中斷，但不要太短以免消耗 CPU
            remaining = seconds - (time.time() - start)
            sleep_time = min(0.1, remaining)
            if sleep_time > 0:
                time.sleep(sleep_time)

    def click(self, button="left", count=1):
        """點擊滑鼠"""
        self._check_state()
        self._update_line()
        btn = Button.left if button == "left" else Button.right
        for _ in range(count):
            self._check_state()
            self.mouse.click(btn)

    def move(self, x: int, y: int):
        """移動滑鼠到絕對位置"""
        self._check_state()
        self._update_line()
        self.mouse.position = (x, y)

    def scroll(self, dx: int, dy: int):
        """滾動滑鼠滾輪"""
        self._check_state()
        self._update_line()
        self.mouse.scroll(dx, dy)

    def press(self, key: str, duration: float = 0.05):
        """按下鍵盤按鍵 (包含按下、延遲、釋放)"""
        self._check_state()
        self._update_line()
        try:
            # 嘗試特殊鍵
            special_key = getattr(Key, key.lower(), None)
            if special_key:
                self.keyboard.press(special_key)
                self.sleep(duration)  # 使用可中斷的 sleep
                self.keyboard.release(special_key)
            else:
                # 普通字元
                self.keyboard.press(key)
                self.sleep(duration)
                self.keyboard.release(key)
        except Exception as e:
            print(f"按鍵錯誤: {e}")

    def type_text(self, text: str):
        """輸入文字"""
        self._check_state()
        self._update_line()
        self.keyboard.type(text)

    def get_mouse_position(self):
        """取得滑鼠位置"""
        # 不檢查狀態，允許在暫停時查詢
        return self.mouse.position

    # 羅技風格的 down/release 函式
    def key_down(self, key: str):
        """按下鍵盤按鍵 (不釋放)"""
        self._check_state()
        self._update_line()
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
        self._check_state()
        self._update_line()
        try:
            special_key = getattr(Key, key.lower(), None)
            if special_key:
                self.keyboard.release(special_key)
            else:
                self.keyboard.release(key)
        except Exception as e:
            print(f"按鍵釋放錯誤: {e}")

    def mouse_down(self, button="left"):
        """按下滑鼠按鈕 (不釋放)"""
        self._check_state()
        self._update_line()
        btn = Button.left if button == "left" else Button.right
        self.mouse.press(btn)

    def mouse_release(self, button="left"):
        """釋放滑鼠按鈕"""
        self._check_state()
        self._update_line()
        btn = Button.left if button == "left" else Button.right
        self.mouse.release(btn)
