# Test Plan

This harness includes two test layers:

1. `test_core.py`
- validates `DocxSession` state transitions
- confirms mutating operations alter document state correctly
- verifies undo/redo stack behavior
- checks save/open round-trip and metadata writes

2. `test_full_e2e.py`
- exercises the installed CLI command via subprocess
- verifies one-shot JSON output and persisted `.docx` edits
- verifies default REPL path and in-session undo

## Planned validation commands

From `python-docx/agent-harness`:

```bash
python -m pip install -e .
python -m pytest -q cli_anything/python_docx/tests
```