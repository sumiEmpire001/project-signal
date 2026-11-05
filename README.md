# Project Signal

A Python CLI for assessing project delivery health from a JSON task list.

## Usage

```bash
python project_signal.py examples/tasks.json
python project_signal.py examples/tasks.json --today 2026-11-05
python -m unittest discover -s tests -v
```

Task status must be one of `todo`, `in_progress`, `blocked`, `done`. Optional `due` dates use ISO format YYYY-MM-DD. Results include total, done, blocked, overdue, a score from 0–100, and issues.

The score is a simple **heuristic**: percentage completed minus ten points per blocked task and five points per overdue task, clamped to 0–100. It is not a predictive model or a substitute for project management judgement.

Python 3.9+; no external dependencies.
