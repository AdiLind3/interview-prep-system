# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Interview preparation system for a Junior Data Engineer position, featuring SQL exercises, Python exercises, flashcards with spaced repetition, and progress tracking.

## Commands

### Run SQL Tests

```powershell
# Test a specific SQL exercise
python sql/tests/test_runner.py "easy/01_customer_orders"

# Test all SQL exercises
python sql/tests/test_runner.py all

# Filter by difficulty
python sql/tests/test_runner.py all --difficulty easy
```

### Run Python Exercises

```powershell
# Run a Python exercise (runs internal tests)
python python/exercises/pandas_manipulation/01_revenue_analysis.py
```

### Flashcard Study Session

```powershell
python concepts/flashcards/cli.py
```

### Progress Tracking

```powershell
# View progress summary
python progress/analytics.py --report summary

# View detailed stats
python progress/analytics.py --report detailed

# Log a study session
python progress/analytics.py --log-session "sql,30,Completed 5 exercises"
```

### Linting and Formatting

```powershell
black .
flake8 .
mypy .
```

## Architecture

### Core Modules (`utils/`)

- `config.py`: Configuration management with dot-notation access (e.g., `config.get("sql.time_limits.easy")`). Loads from `config.json` or uses defaults.
- `database.py`: `SQLiteHelper` class for SQL exercise testing. Uses in-memory SQLite databases with context manager support.
- `logger.py`: Rich-based logging setup. Use `from utils.logger import logger`.

### SQL Exercises (`sql/exercises/{difficulty}/{exercise_name}/`)

Each exercise contains:
- `schema.sql`: Database schema definition
- `sample_data.sql`: Test data
- `template.sql`: Where solutions are written
- `solution.sql`: Reference solution
- `expected_output.json`: Expected query results
- `test.py`: Exercise-specific test (optional, uses test_runner.py)

The test runner (`sql/tests/test_runner.py`) loads schema/data into an in-memory SQLite database, executes the template.sql query, and compares against expected_output.json.

### Python Exercises (`python/exercises/{category}/`)

Self-contained Python files with embedded tests at the bottom. Solutions go in the main function, tests run via `if __name__ == "__main__"`.

### Flashcards (`concepts/flashcards/`)

- `cards.json`: Flashcard data with SM-2 spaced repetition metadata (ease_factor, interval, repetitions)
- `cli.py`: Interactive terminal UI using Rich library

### Progress Tracking (`progress/`)

- `tracker.json`: Progress data (exercises completed, time spent, flashcard stats)
- `analytics.py`: CLI for viewing progress reports and logging sessions

## Development Notes

- All files should use UTF-8 encoding (Hebrew character support)
- Use Python's logging module for all logging
- Use `rich` library for terminal UI output
- SQL exercises use SQLite syntax
- Progress tracker references an interview date in config for countdown display
