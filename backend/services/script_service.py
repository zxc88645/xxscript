"""
腳本業務邏輯層
處理腳本相關的業務邏輯
"""

import ast
import json
import subprocess
import tempfile
from pathlib import Path

from models.schemas import Script, ScriptCheckIssue, ScriptCreate, ScriptUpdate
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

    def get_all_scripts(self) -> list[Script]:
        """取得所有腳本"""
        return self.repository.get_all()

    def get_script(self, script_id: str) -> Script | None:
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

    def update_script(self, script_id: str, update_data: ScriptUpdate) -> Script | None:
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

    def get_enabled_scripts(self) -> list[Script]:
        """取得所有啟用的腳本"""
        return self.repository.get_enabled_scripts()

    def check_script(self, content: str) -> list[ScriptCheckIssue]:
        """
        檢查腳本代碼
        使用 AST 進行基礎語法檢查，並嘗試使用 ruff 進行 lint
        """
        issues = []

        # 1. 基礎 AST 語法檢查
        try:
            ast.parse(content)
        except SyntaxError as e:
            issues.append(
                ScriptCheckIssue(
                    line=e.lineno or 1,
                    column=e.offset or 1,
                    message=f"Syntax Error: {e.msg}",
                    severity="error",
                    code="SYNTAX",
                )
            )
            # 語法錯誤通常意味著無法進一步 lint，直接返回
            return issues
        except Exception as e:
            issues.append(
                ScriptCheckIssue(
                    line=1,
                    column=1,
                    message=f"Parse Error: {e!s}",
                    severity="error",
                    code="PARSE",
                )
            )
            return issues

        # 2. 使用 Ruff 進行檢查 (如果可用)
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False, encoding="utf-8"
            ) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            try:
                # 執行 ruff check --output-format=json
                result = subprocess.run(
                    [
                        "python",
                        "-m",
                        "ruff",
                        "check",
                        tmp_path,
                        "--output-format=json",
                        "--select=E,F,W",
                    ],
                    capture_output=True,
                    text=True,
                    check=False,  # ruff returns non-zero on violations, so check=False
                )

                if result.stdout:
                    ruff_violations = json.loads(result.stdout)
                    for v in ruff_violations:
                        issues.append(
                            ScriptCheckIssue(
                                line=v["location"]["row"],
                                column=v["location"]["column"],
                                message=v["message"],
                                severity="error",  # Ruff violations are usually errors or warnings, simpler to map to error for now unless we parse severity
                                code=v["code"],
                            )
                        )

            finally:
                Path(tmp_path).unlink(missing_ok=True)

        except Exception as e:
            print(f"Ruff check failed: {e}")
            # fall back to AST only if ruff fails
            pass

        return issues
