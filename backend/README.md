# 後端開發指南

## 環境設置

### 1. 安裝 Python 依賴

```bash
cd backend
pip install -r requirements.txt
```

## 程式碼品質工具

本專案使用以下工具來確保程式碼品質：

### Ruff

Ruff 是一個極快的 Python linter 和 formatter，整合了多個工具的功能（Flake8、isort、Black 等）。

#### 功能

- **Linting**: 檢查程式碼風格和潛在錯誤
- **Formatting**: 自動格式化程式碼
- **Import 排序**: 自動整理 import 語句

### mypy

靜態類型檢查工具，幫助在執行前發現類型相關的錯誤。

## 可用的 NPM 腳本

在專案根目錄執行以下命令：

### 檢查程式碼（Linting）

```bash
npm run backend:lint
```

這會執行 Ruff 檢查並自動修復可修復的問題。

### 格式化程式碼

```bash
npm run backend:format
```

使用 Ruff 格式化所有 Python 檔案。

### 類型檢查

```bash
npm run backend:type-check
```

使用 mypy 進行靜態類型檢查。

### 完整檢查

```bash
npm run backend:check
```

依序執行 lint、format 和 type-check。

## 直接使用 Ruff

如果您在 `backend` 目錄中，也可以直接使用 Ruff：

```bash
# 檢查程式碼
ruff check .

# 檢查並自動修復
ruff check . --fix

# 格式化程式碼
ruff format .

# 查看特定檔案的問題
ruff check path/to/file.py
```

## VS Code 整合

如果您使用 VS Code：

1. 安裝推薦的擴充套件（會自動提示）：
   - Python (ms-python.python)
   - Ruff (charliermarsh.ruff)

2. 設定已自動配置為：
   - 儲存時自動格式化
   - 儲存時自動修復 lint 問題
   - 儲存時自動整理 imports

## 配置檔案

- `pyproject.toml`: Ruff 和 mypy 的配置
- `.vscode/settings.json`: VS Code 的 Python 設定

## 程式碼風格規則

主要規則包括：

- **行長度**: 最多 100 字元
- **引號風格**: 雙引號
- **縮排**: 4 個空格
- **Import 排序**: 按照標準庫、第三方庫、本地模組的順序

詳細規則請參考 `pyproject.toml` 中的配置。

## 提交前檢查

建議在提交程式碼前執行：

```bash
npm run backend:check
```

確保所有檢查都通過。

## 常見問題

### Q: Ruff 和 Black 有什麼不同？

A: Ruff 是用 Rust 編寫的，速度比 Black 快 10-100 倍，並且整合了更多功能。它可以完全取代 Black、Flake8、isort 等工具。

### Q: 如何忽略特定的 lint 規則？

A: 在程式碼中使用註解：

```python
# ruff: noqa: E501
very_long_line = "這行很長但我想忽略行長度檢查"

# 或忽略整個檔案的特定規則
# ruff: noqa: F401
```

### Q: 類型檢查太嚴格怎麼辦？

A: 目前 mypy 設定為較寬鬆的模式（`disallow_untyped_defs = false`）。您可以在 `pyproject.toml` 中調整設定，逐步提高嚴格程度。
