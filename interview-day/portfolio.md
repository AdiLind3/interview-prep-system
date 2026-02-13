# Interview Prep System -- Portfolio Document

> "I'd like to show you something about how I prepared for this interview.
> Rather than passively reviewing notes, I built an engineering system to
> make my preparation measurable and efficient."

---

## The Challenge

Prepare thoroughly for a Junior Data Engineer interview at tasq.ai in a
compressed timeline, covering SQL, Python/Pandas, system design, and
behavioral topics -- while demonstrating real engineering skills in the
process.

---

## What I Built

A fully integrated, terminal-based interview preparation system with
the following components:

| Component               | Description                                                  |
|-------------------------|--------------------------------------------------------------|
| SQL Exercise System     | Structured problems (easy/medium/hard) with schemas, sample data, auto-tested solutions |
| Python Challenges       | Pandas data manipulation and real-world scenario exercises   |
| Flashcard CLI           | Interactive spaced-repetition study tool (SM-2 algorithm)    |
| Searchable Cheatsheets  | CLI utility to instantly look up SQL and Python patterns      |
| Progress Tracker        | JSON-based tracker with analytics dashboard                  |
| Mock Interview Toolkit  | Timed coding simulator with hints and evaluation             |
| System Design Scenarios | Structured templates for pipeline architecture discussions   |
| Interview Day Kit       | Checklists, quick-review guides, and this portfolio document |

---

## Technical Highlights

### SM-2 Spaced Repetition Algorithm
The flashcard system implements the SuperMemo SM-2 algorithm to schedule
card reviews based on recall quality. Cards the user struggles with
appear more frequently, while mastered cards are pushed further out.
This is the same algorithm used by Anki and other professional study
tools.

### Automated SQL Testing
Each SQL exercise includes:
- A schema definition (`schema.sql`)
- Realistic sample data (`sample_data.sql`)
- An expected output specification (`expected_output.json`)
- A pytest-based test runner that loads everything into an in-memory
  SQLite database, executes the student query, and compares results
  order-independently.

### Rich Terminal UI
All interactive tools use the `rich` library for styled, readable
terminal output including syntax-highlighted code blocks, progress bars,
styled panels, and formatted tables. No external GUI or web server
required.

### Searchable Cheatsheet Utility
A CLI tool (`utils/search_cheatsheet.py`) that parses the SQL and
Python cheatsheet markdown files, finds sections matching one or more
search terms, and displays results with highlighted matches and
syntax-colored code blocks.

### Modular Configuration
A centralized `Config` class with dot-path access (`config.get("sql.time_limits.easy")`)
manages all settings, from exercise directories to spaced repetition
parameters, with sensible defaults and optional JSON override.

---

## Technologies Demonstrated

| Category       | Technologies                                            |
|----------------|---------------------------------------------------------|
| Languages      | Python 3.13, SQL (SQLite dialect)                       |
| Data           | pandas, numpy, SQLite, SQLAlchemy                       |
| Testing        | pytest, pytest-cov, automated SQL validation            |
| CLI / UI       | rich, click, prompt-toolkit, argparse                   |
| Code Quality   | black, flake8, mypy, type hints throughout              |
| Data Gen       | Faker for realistic sample data                         |
| Architecture   | Modular package layout, config management, logging      |
| Version Control| Git, GitHub                                             |

---

## Project Structure

```
interview-prep-system/
    sql/
        cheatsheet.md
        exercises/          (easy, medium, hard with full test suites)
        tests/
    python/
        cheatsheet.md
        exercises/          (pandas, real-world scenarios)
    concepts/
        flashcards/         (SM-2 spaced repetition CLI)
    system-design/
        scenarios/
    progress/
        tracker.json
        analytics.py
    utils/
        config.py
        database.py
        logger.py
        search_cheatsheet.py
    interview-day/
        checklist.md
        portfolio.md
        quick_review.md
```

---

## Key Talking Points

1. **Engineering approach to learning.** Instead of reading articles, I
   built a system that generates exercises, tests my solutions
   automatically, and tracks my progress over time.

2. **AI-assisted development.** I used Claude Code as a pair-programming
   partner to accelerate development while maintaining code quality and
   understanding every line.

3. **Production-quality habits.** Even for a personal project, I used
   type hints, structured logging, automated tests, modular design, and
   a clean Git history.

4. **Data engineering in practice.** The project itself exercises core
   data engineering skills: SQL query design, Python data transformation,
   automated testing pipelines, and system architecture thinking.

5. **Rapid execution.** The entire system was designed and built in a
   short preparation window, demonstrating the ability to deliver
   working software under time pressure.

---

## GitHub

Repository: [https://github.com/YOUR_USERNAME/interview-prep-system](https://github.com/YOUR_USERNAME/interview-prep-system)

*(Replace the placeholder above with the actual repository URL before
the interview.)*

---

## How This Relates to tasq.ai

- **Data pipeline thinking**: the exercise and testing system mirrors
  ETL patterns -- ingest (load schema/data), transform (run query),
  validate (compare output).
- **Quality-first mindset**: automated testing at every layer aligns
  with data quality and reliability goals.
- **Python + SQL fluency**: the two core languages for any data
  engineering role, demonstrated through building tools, not just
  solving toy problems.
- **AI collaboration**: practical experience using AI coding assistants
  productively, relevant for a company working at the intersection of
  AI and data.
