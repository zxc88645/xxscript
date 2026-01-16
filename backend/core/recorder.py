"""
腳本錄製器
記錄滑鼠與鍵盤操作,生成可執行的 Python 腳本
"""

import time

from pynput import keyboard, mouse


class ScriptRecorder:
    def __init__(self):
        self.recording = False
        self.events: list[dict] = []
        self.start_time: float = 0.0
        self.mouse_listener: mouse.Listener | None = None
        self.keyboard_listener: keyboard.Listener | None = None

    def start_recording(self):
        """開始錄製"""
        if self.recording:
            return

        self.recording = True
        self.events = []
        self.start_time = time.time()

        # 啟動滑鼠監聽
        self.mouse_listener = mouse.Listener(
            on_move=self.on_mouse_move, on_click=self.on_mouse_click
        )
        self.mouse_listener.start()

        # 啟動鍵盤監聽
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

        print("開始錄製腳本...")

    def stop_recording(self) -> str:
        """停止錄製並生成腳本"""
        if not self.recording:
            return ""

        self.recording = False

        # 停止監聽器
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

        # 生成腳本
        script = self.generate_script()
        print(f"錄製完成,共記錄 {len(self.events)} 個事件")

        return script

    def on_mouse_move(self, x, y):
        """滑鼠移動事件"""
        if not self.recording:
            return

        # 只記錄間隔較大的移動,避免過多事件
        if self.events and self.events[-1]["type"] == "mouse_move":
            last_event = self.events[-1]
            # 如果距離很近,更新最後一個事件而不是新增
            if abs(last_event["x"] - x) < 10 and abs(last_event["y"] - y) < 10:
                last_event["x"] = x
                last_event["y"] = y
                last_event["timestamp"] = time.time() - self.start_time
                return

        self.events.append(
            {"type": "mouse_move", "x": x, "y": y, "timestamp": time.time() - self.start_time}
        )

    def on_mouse_click(self, x, y, button, pressed):
        """滑鼠點擊事件"""
        if not self.recording or not pressed:  # 只記錄按下,不記錄釋放
            return

        button_name = "left" if button == mouse.Button.left else "right"

        self.events.append(
            {
                "type": "mouse_click",
                "x": x,
                "y": y,
                "button": button_name,
                "timestamp": time.time() - self.start_time,
            }
        )

    def on_key_press(self, key):
        """鍵盤按下事件"""
        if not self.recording:
            return

        try:
            # 取得按鍵字串
            if hasattr(key, "char") and key.char:
                key_str = key.char
            elif hasattr(key, "name"):
                key_str = key.name
            else:
                return

            self.events.append(
                {"type": "key_press", "key": key_str, "timestamp": time.time() - self.start_time}
            )
        except Exception:
            pass

    def generate_script(self) -> str:
        """生成 Python 腳本"""
        if not self.events:
            return "# 未記錄到任何操作\n"

        lines = [
            "# 自動生成的腳本",
            "# 錄製時間: " + time.strftime("%Y-%m-%d %H:%M:%S"),
            "",
        ]

        last_timestamp = 0

        for event in self.events:
            # 計算延遲
            delay = event["timestamp"] - last_timestamp
            if delay > 0.05:  # 大於 50ms 才加入延遲
                lines.append(f"sleep({delay:.2f})")

            # 根據事件類型生成程式碼
            if event["type"] == "mouse_move":
                lines.append(f"move({event['x']}, {event['y']})")
            elif event["type"] == "mouse_click":
                lines.append(f"click(button='{event['button']}')")
            elif event["type"] == "key_press":
                key = event["key"]
                if len(key) == 1:  # 單一字元
                    lines.append(f"type_text('{key}')")
                else:  # 特殊鍵
                    lines.append(f"press('{key}')")

            last_timestamp = event["timestamp"]

        return "\n".join(lines)

    def get_status(self) -> dict:
        """取得錄製狀態"""
        return {
            "recording": self.recording,
            "event_count": len(self.events),
            "duration": time.time() - self.start_time if self.recording else 0,
        }
