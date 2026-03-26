# CLI-Anything python-docx Harness

Stateful CLI harness for `python-docx` with one-shot commands, JSON output, and REPL-first workflow.

## Install

From `agent-harness/`:

```bash
python -m pip install -e .
```

## Usage

One-shot examples:

```bash
cli-anything-python-docx --json new ./demo.docx --title "Demo"
cli-anything-python-docx add-paragraph --doc ./demo.docx "Hello from CLI"
cli-anything-python-docx --json summary --doc ./demo.docx
cli-anything-python-docx frontpage-templates
cli-anything-python-docx add-frontpage --doc ./demo.docx --template clean --title "Operations Review" --subtitle "Q1 2026" --author "CLI Agent" --organization "Nordflint" --date-text "2026-03-26"
cli-anything-python-docx add-table --doc ./demo.docx --header Qty --header Id --header Desc --record "3|101|Spam" --record "7|422|Eggs" --record "4|631|Spam, spam, eggs, and spam"
cli-anything-python-docx add-table --doc ./demo.docx --header Qty --header Id --header Desc --record "3|101|Spam" --record "7|422|Eggs" --record "4|631|Spam, spam, eggs, and spam" --header-bold --row-lines --column-lines --outer-border --line-style single --line-size 8 --line-color main
```

REPL (default when no subcommand is provided):

```bash
cli-anything-python-docx
python-docx> new ./notes.docx --title "Notes"
python-docx> add-heading "Sprint" --level 2
python-docx> add-paragraph "Action item"
python-docx> undo
python-docx> save
python-docx> exit
```

## Commands

- `new [PATH] [--title TEXT]`
- `open PATH`
- `save [PATH]`
- `summary [--doc PATH]` (use global `--json` before the subcommand)
- `list-paragraphs [--doc PATH] [--limit N]` (use global `--json` before the subcommand)
- `add-paragraph [--doc PATH] [--style NAME] TEXT`
- `add-heading [--doc PATH] [--level N] TEXT`
- `frontpage-templates`
- `add-frontpage [--doc PATH] [--template NAME] --title TEXT [--subtitle TEXT] [--author TEXT] [--organization TEXT] [--date-text TEXT] [--page-break/--no-page-break] [--set-core-title/--no-set-core-title]`
- `add-table [--doc PATH] [--rows N] [--cols N] [--header TEXT ...] [--record TEXT ...] [--delimiter CHAR] [--header-bold] [--header-bg-color HEX] [--row-lines] [--column-lines] [--outer-border] [--line-style STYLE] [--line-size N] [--line-color COLOR]`
- `set-core [--doc PATH] KEY VALUE`
- `undo`
- `redo`
- `repl`

`--doc` on mutating commands enables one-shot edits that auto-save back to that file.

Structured table mode (`--header`/`--record`) is useful for record-style inserts.
Each `--record` line is parsed by `--delimiter` (default `|`).
Border formatting can be enabled independently for row separators (`--row-lines`) and column separators (`--column-lines`), and optional outside borders (`--outer-border`).
Header formatting defaults to `main` background with white text, and can be customized with `--header-bold` and `--header-bg-color`.
Frontpage templates let the agent insert a predefined title-page layout with a single command.
The `corporate` frontpage template uses a blue (`main`) background with white text.

## Palette

This harness enforces a fixed palette:

- `main`: `#05206E`
- `secondary`: `#357AE9`

Title/header fonts and table styling use these colors by default. Color options only accept `main`, `secondary`, or those exact hex values.
