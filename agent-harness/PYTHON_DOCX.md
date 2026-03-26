# PYTHON_DOCX Harness

Target software: `python-docx`
Source path: `python-docx/`

## Scope

This harness exposes high-value document operations from `python-docx` as a stateful CLI:

- create/open/save documents
- add paragraph, heading, and table content
- insert template-driven frontpages/title pages
- update core metadata properties
- inspect summary and paragraph lists
- run with one-shot subcommands or interactive REPL
- emit machine-readable JSON output using `--json`
- support undo/redo in-session via in-memory `.docx` snapshots
- enforce a fixed visual palette (`#05206E` main, `#357AE9` secondary)

## Backend strategy

The harness wraps the real `python-docx` APIs in `utils/python_docx_backend.py` and does not reimplement `.docx` behavior.

## Session model

A `DocxSession` instance tracks:

- active in-memory document
- current path (if saved/opened)
- undo stack
- redo stack

Undo and redo operate on serialized `.docx` bytes captured before each mutating operation.
