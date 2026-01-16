"""
全域按鍵監聽器
監聽使用者設定的觸發鍵並執行對應腳本
支援組合鍵 (Ctrl+Shift+F1 等)
"""

import threading
from collections.abc import Callable

from pynput import keyboard


class KeyListener:
    def __init__(self, on_trigger: Callable, on_f2: Callable | None = None):
        self.on_trigger = on_trigger
        self.on_f2 = on_f2
        self.hotkeys: dict[str, dict] = {}  # {key_combo: {script_id, script_content}}
        self.listener: keyboard.Listener | None = None
        self.running = False
        self.pressed_keys: set[str] = set()  # 追蹤目前按下的按鍵

    def register_hotkey(self, key_combo: str, script_id: str, script_content: str):
        """註冊熱鍵"""
        self.hotkeys[key_combo.lower()] = {"script_id": script_id, "script_content": script_content}
        print(f"已註冊熱鍵: {key_combo} -> 腳本 {script_id}")

    def unregister_hotkey(self, key_combo: str):
        """取消註冊熱鍵"""
        if key_combo.lower() in self.hotkeys:
            del self.hotkeys[key_combo.lower()]
            print(f"已取消熱鍵: {key_combo}")

    def clear_all(self):
        """清除所有熱鍵"""
        self.hotkeys.clear()

    def _get_current_combo(self) -> str:
        """取得目前按鍵組合字串"""
        if not self.pressed_keys:
            return ""

        # 修飾鍵順序: ctrl, shift, alt
        modifiers = []
        main_keys = []

        for key in self.pressed_keys:
            if key in ["ctrl", "shift", "alt"]:
                modifiers.append(key)
            else:
                main_keys.append(key)

        # 排序修飾鍵
        modifier_order = {"ctrl": 0, "shift": 1, "alt": 2}
        modifiers.sort(key=lambda x: modifier_order.get(x, 999))

        # 組合字串
        all_keys = modifiers + main_keys
        return "+".join(all_keys) if all_keys else ""

    def on_press(self, key):
        """按鍵按下事件"""
        try:
            # 轉換按鍵為字串
            key_str = self._key_to_string(key)
            if not key_str:
                return

            # 加入已按下的按鍵集合
            self.pressed_keys.add(key_str)

            # 處理系統功能鍵 (例如 F2)
            if key_str == "f2" and self.on_f2:
                # 在新執行緒中執行回呼，以免阻塞監聽器
                threading.Thread(target=self.on_f2).start()
                return

            # 取得目前組合鍵
            current_combo = self._get_current_combo()

            # 檢查是否為註冊的熱鍵
            if current_combo in self.hotkeys:
                script_info = self.hotkeys[current_combo]
                print(f"觸發熱鍵: {current_combo}")
                # 在新執行緒中執行腳本,避免阻塞監聽器
                threading.Thread(
                    target=self.on_trigger, args=(script_info["script_content"],)
                ).start()
        except Exception as e:
            print(f"按鍵處理錯誤: {e}")

    def on_release(self, key):
        """按鍵釋放事件"""
        try:
            key_str = self._key_to_string(key)
            if key_str and key_str in self.pressed_keys:
                self.pressed_keys.remove(key_str)
        except Exception as e:
            print(f"按鍵釋放錯誤: {e}")

    def _key_to_string(self, key) -> str:
        """將按鍵轉換為字串"""
        try:
            # 修飾鍵
            if key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                return "ctrl"
            elif (
                key == keyboard.Key.shift
                or key == keyboard.Key.shift_l
                or key == keyboard.Key.shift_r
            ):
                return "shift"
            elif key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                return "alt"
            # 特殊鍵
            elif hasattr(key, "name"):
                return str(key.name).lower()
            # 普通字元
            elif hasattr(key, "char") and key.char:
                return str(key.char).lower()
            return ""
        except Exception:
            return ""

    def start(self):
        """啟動監聽器"""
        if self.running:
            return

        self.running = True
        self.pressed_keys.clear()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        print("按鍵監聽器已啟動")

    def stop(self):
        """停止監聽器"""
        if self.listener:
            self.listener.stop()
            self.running = False
            self.pressed_keys.clear()
            print("按鍵監聽器已停止")
