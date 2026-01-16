import { debounce } from 'lodash-es';
import type { ShallowRef } from 'vue';
import type { editor } from 'monaco-editor';
import type { ScriptCheckIssue } from '../types';

export function useScriptLinting(
  editorRef: ShallowRef<editor.IStandaloneCodeEditor | null>,
  selectedScript: { value: { id: number } | null },
  checkCurrentScript: () => Promise<ScriptCheckIssue[]>,
  monacoRef: { value: typeof import('monaco-editor') | null },
  saveCurrentScript: () => void,
) {
  const performCheck = async () => {
    if (!editorRef.value || !selectedScript.value || !monacoRef.value) return;

    const issues = await checkCurrentScript();
    const model = editorRef.value.getModel();
    const monacoInstance = monacoRef.value;

    if (model) {
      const markers = issues.map((issue) => {
        const maxCol = model.getLineMaxColumn(issue.line);

        return {
          severity:
            issue.severity === 'error'
              ? monacoInstance.MarkerSeverity.Error
              : monacoInstance.MarkerSeverity.Warning,
          message: issue.message,
          startLineNumber: issue.line,
          startColumn: issue.column,
          endLineNumber: issue.line,
          endColumn: maxCol,
        };
      });
      monacoInstance.editor.setModelMarkers(model, 'owner', markers);
    }
  };

  const debouncedCheck = debounce(performCheck, 1000);

  const handleChange = () => {
    saveCurrentScript();
    debouncedCheck();
  };

  const handleJumpToIssue = (issue: ScriptCheckIssue) => {
    if (editorRef.value) {
      editorRef.value.revealPositionInCenter({ lineNumber: issue.line, column: issue.column });
      editorRef.value.setPosition({ lineNumber: issue.line, column: issue.column });
      editorRef.value.focus();
    }
  };

  return {
    performCheck,
    handleChange,
    handleJumpToIssue,
  };
}
