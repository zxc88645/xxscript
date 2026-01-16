# XXScript 使用說明

## 安裝與啟動

### 後端 (Python)

1. 建立虛擬環境並安裝依賴:

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. 啟動後端服務:

```bash
python main.py
```

後端將在 `http://127.0.0.1:8000` 啟動。

### 前端 (Vue)

1. 安裝依賴 (如果尚未安裝):

```bash
npm install
```

2. 啟動開發伺服器:

```bash
npm run dev
```

前端將在 `http://localhost:5173` 啟動。

## 使用方式

1. 開啟瀏覽器訪問前端介面
2. 點擊「新增」建立新腳本
3. 輸入腳本名稱與內容
4. 設定觸發熱鍵 (點擊輸入框後按下想要的按鍵)
5. 點擊「啟動監聽」開始監聽熱鍵
6. 按下設定的熱鍵即可執行腳本

## 可用的腳本 API

### 滑鼠控制

- `click(button='left', count=1)` - 點擊滑鼠
- `move(x, y)` - 移動滑鼠到指定位置
- `mouse_down(button='left')` - 按下滑鼠按鈕 (不釋放)
- `mouse_release(button='left')` - 釋放滑鼠按鈕
- `mouse_position()` - 取得目前滑鼠位置

### 鍵盤控制

- `press(key, duration=0.05)` - 按下鍵盤按鍵 (包含按下、延遲、釋放)
- `key_down(key)` - 按下鍵盤按鍵 (不釋放)
- `key_release(key)` - 釋放鍵盤按鍵
- `type_text(text)` - 輸入文字

### 其他

- `sleep(seconds)` - 延遲執行

## 範例腳本

```python
# 自動點擊範例
move(500, 300)
click()
sleep(0.5)
click(count=2)

# 輸入文字範例
type_text('Hello World')
press('enter', 0.1)  # 按住 0.1 秒

# 羅技風格 - 精細控制按鍵
key_down('shift')    # 按住 Shift
press('a')           # 按 A (會輸入大寫 A)
key_release('shift') # 釋放 Shift

# 拖曳範例
move(100, 100)
mouse_down('left')   # 按住左鍵
sleep(0.1)
move(200, 200)       # 拖曳到新位置
mouse_release('left') # 釋放左鍵

# 組合技範例
for i in range(5):
    move(100 + i * 50, 100)
    click()
    sleep(0.2)
```

## 注意事項

- Windows 系統可能需要以管理員權限執行後端程式
- 熱鍵監聽為全域監聽,請謹慎設定避免與系統快捷鍵衝突
- 腳本執行時會直接控制滑鼠鍵盤,請小心使用
