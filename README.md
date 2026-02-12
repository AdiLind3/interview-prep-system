# 🚀 AI-Powered Interview Prep System

> **A comprehensive, production-grade learning environment for Data Engineering interview preparation**

[![Made with Claude](https://img.shields.io/badge/Made%20with-Claude-blue)](https://claude.ai)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [System Components](#system-components)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Progress Dashboard](#progress-dashboard)
- [Why This Project?](#why-this-project)
- [Technologies](#technologies)

---

## 🎯 Overview

This isn't just a collection of study materials—it's an **intelligent, automated learning system** built specifically for interview preparation. Instead of passive studying, I built an AI-powered platform that:

✅ **Generates and validates** SQL and Python exercises with automated testing
✅ **Implements spaced repetition** with the SM-2 algorithm for optimal retention
✅ **Tracks progress** with detailed analytics and personalized recommendations
✅ **Simulates interviews** with timed coding challenges
✅ **Provides instant feedback** on solutions with detailed explanations

**Target Role**: Junior Data Engineer at tasq.ai
**Timeline**: 5-day intensive preparation
**Outcome**: Production-quality code that demonstrates engineering excellence

---

## ✨ Features

### 1. 📝 SQL Exercise System
- **30+ curated problems** across Easy, Medium, and Hard difficulties
- **Automated test runner** with visual feedback
- **Topics covered**: JOINs, Window Functions, CTEs, Subqueries, Optimization
- **Instant validation** against expected outputs
- **Beautiful CLI interface** with Rich library

### 2. 🐍 Python Coding Challenges
- **25+ exercises** covering real-world data engineering scenarios
- **Categories**: Pandas Manipulation, Data Structures, API Integration
- **Pytest framework** with comprehensive test coverage
- **Type hints** and modern Python practices
- **Performance benchmarking**

### 3. 🎴 Interactive Flashcard System
- **75 flashcards** across 5 key categories
- **SM-2 spaced repetition algorithm** for optimal learning
- **Progress tracking** and confidence scoring
- **Category filtering** for focused study
- **Beautiful terminal UI** with markdown rendering

### 4. 📊 Progress Analytics
- **Real-time progress tracking** across all activities
- **Visual dashboards** with completion percentages
- **Time investment tracking**
- **Personalized recommendations** based on weak areas
- **Days-until-interview countdown**

### 5. 🎯 System Design Scenarios
- **Real-world scenarios** (e.g., real-time analytics pipeline)
- **Detailed solutions** with architecture diagrams
- **Trade-off discussions** and alternatives
- **Evaluation rubrics** for self-assessment

### 6. 📚 Curated Resources
- **100+ vetted learning resources**
- **Company research templates** (tasq.ai specific)
- **Interview preparation checklists**
- **STAR story frameworks**

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd interview-prep-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Your First SQL Exercise

```bash
# Test a specific SQL exercise
python sql/tests/test_runner.py sql/exercises/easy/01_customer_orders

# Or test all exercises
python sql/tests/test_runner.py all
```

### Start a Flashcard Session

```bash
# Launch interactive flashcard CLI
python concepts/flashcards/cli.py
```

### Check Your Progress

```bash
# View progress dashboard
python progress/analytics.py --report=summary

# View detailed statistics
python progress/analytics.py --report=detailed

# Log a study session
python progress/analytics.py --log-session="sql,45,Completed 5 exercises"
```

---

## 🏗️ System Components

### Architecture Overview

```
interview-prep-system/
├── 🗄️  sql/                    # SQL exercises and tests
│   ├── exercises/
│   │   ├── easy/              # 10 problems
│   │   ├── medium/            # 15 problems
│   │   └── hard/              # 5 problems
│   ├── tests/                 # Automated test runner
│   └── cheatsheet.md          # Quick reference
│
├── 🐍 python/                  # Python exercises
│   ├── exercises/
│   │   ├── pandas_manipulation/
│   │   ├── data_structures/
│   │   ├── algorithms/
│   │   └── real_world_scenarios/
│   └── cheatsheet.md
│
├── 🎴 concepts/                # Flashcards
│   └── flashcards/
│       ├── cards.json         # 75 flashcards
│       └── cli.py             # Interactive CLI
│
├── 📊 progress/                # Progress tracking
│   ├── tracker.json           # Progress data
│   └── analytics.py           # Analytics engine
│
├── 🎨 system-design/           # System design prep
│   └── scenarios/             # Real-world scenarios
│
├── 📚 resources/               # Learning resources
│   ├── links.md               # Curated links
│   └── tasq_ai_research.md    # Company research
│
└── 🛠️  utils/                  # Core utilities
    ├── database.py            # SQLite helper
    ├── config.py              # Configuration
    └── logger.py              # Structured logging
```

---

## 📖 Usage Guide

### SQL Practice

#### Writing a Solution

1. Navigate to an exercise: `sql/exercises/easy/01_customer_orders/`
2. Read `problem_statement.md`
3. Edit `template.sql` with your solution
4. Run the test: `python sql/tests/test_runner.py sql/exercises/easy/01_customer_orders`

#### Example Output

```
Testing: 01_customer_orders

Loading schema...
Loading sample data...
Executing your solution...
✅ All tests passed!
   Returned 4 rows correctly.

┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ customer_id ┃ name           ┃ email              ┃ order_count ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 4           │ Diana Prince   │ diana@email.com    │ 3           │
│ 1           │ Alice Johnson  │ alice@email.com    │ 3           │
│ 2           │ Bob Smith      │ bob@email.com      │ 2           │
│ 3           │ Charlie Brown  │ charlie@email.com  │ 1           │
└─────────────┴────────────────┴────────────────────┴─────────────┘
```

### Python Exercises

#### Running Tests

```bash
# Run specific exercise tests
python python/exercises/pandas_manipulation/01_revenue_analysis.py

# Run all Python tests
pytest python/tests/ -v

# With coverage
pytest python/tests/ --cov=python/exercises
```

### Flashcard Study Session

The flashcard system uses **spaced repetition** to optimize learning:

```bash
python concepts/flashcards/cli.py
```

**Features**:
- Cards are scheduled based on your performance
- Rate yourself 0-5 after each card
- System calculates next review date using SM-2 algorithm
- Focus on categories (e.g., "SQL Concepts" or "AWS Services")

**Spaced Repetition Schedule**:
- ✅ Perfect recall (5): Next review in 6+ days
- 👍 Good recall (3-4): Next review in 1-6 days
- ⚠️ Struggled (0-2): Review again tomorrow

### Progress Tracking

Monitor your preparation with detailed analytics:

```bash
# Daily summary
python progress/analytics.py --report=summary
```

**Example Output**:

```
╔════════════════════════════════════════════════╗
║     📊 Interview Prep Progress Report           ║
║            Interview in 2 days                 ║
╚════════════════════════════════════════════════╝

Overall Progress: 76.4%
   ████████░░ 76.4%

📝 SQL Exercises
   Progress: 24/30 (80%)
   ✅ Easy: 10/10 (100%)
   ✅ Medium: 11/15 (73%)
   ⚠️  Hard: 3/5 (60%)

🐍 Python Exercises
   Progress: 18/25 (72%)
   ✅ Pandas: 9/10 (90%)
   ⚠️  Data Structures: 5/8 (62%)
   ✅ Real World: 4/7 (57%)

🎴 Flashcards
   Total Reviews: 45
   Cards Mastered: 30
   Avg Confidence: 4.2/5

⏱️  Time Investment
   Total: 8.5 hours (510 minutes)

🎯 Next Steps:
   1. Complete 4 more SQL Hard problems
   2. Review Data Structures (weak area)
   3. Do 1 mock interview
```

---

## 📁 Project Structure

### Key Files

| File | Purpose |
|------|---------|
| `sql/tests/test_runner.py` | Universal SQL test runner |
| `concepts/flashcards/cli.py` | Interactive spaced repetition system |
| `progress/analytics.py` | Progress tracking and analytics |
| `utils/database.py` | SQLite helper for SQL exercises |
| `requirements.txt` | Python dependencies |

### Configuration

Edit `utils/config.py` or create `config.json` to customize:
- Exercise time limits
- Daily goals
- Interview date
- Company information

---

## 📈 Progress Dashboard

Track your journey:

- **SQL Exercises**: 0/30 completed (0%)
- **Python Exercises**: 0/25 completed (0%)
- **Flashcards**: 0/75 reviewed
- **Mock Interviews**: 0 completed
- **Time Invested**: 0 hours
- **Days Until Interview**: TBD

---

## 🤔 Why This Project?

### The Challenge

I had **5 days** to prepare for a Data Engineer interview. Traditional approaches (reading docs, watching tutorials) felt passive and inefficient.

### The Solution

Instead of passively studying, I **built a production-grade learning system** that:

1. **Generates exercises** with automated validation
2. **Tracks progress** with data-driven insights
3. **Optimizes learning** with spaced repetition
4. **Simulates real interviews** with timed challenges

### The Meta-Lesson

This project itself demonstrates:
- 🧠 **Problem-solving**: Identified inefficiency, built a solution
- 🏗️ **System design**: Modular, extensible architecture
- 💻 **Software engineering**: Clean code, testing, documentation
- 📊 **Data engineering**: Schema design, data pipelines
- 🤖 **AI collaboration**: Leveraged Claude Code for rapid development
- 📈 **Results-oriented**: Measurable outcomes and analytics

**This IS my portfolio piece for the interview!**

---

## 🛠️ Technologies

### Languages & Frameworks
- **Python 3.8+**: Core language
- **SQL (SQLite)**: Exercise validation
- **Pandas**: Data manipulation exercises
- **Pytest**: Testing framework

### Libraries
- **Rich**: Beautiful terminal UI
- **SQLAlchemy**: Database ORM
- **Requests**: API interactions
- **Click**: CLI interfaces

### Methodologies
- **SM-2 Algorithm**: Spaced repetition
- **Test-Driven Development**: Automated testing
- **Modular Design**: Reusable components
- **Documentation-First**: Clear, comprehensive docs

---

## 📝 Learning Resources

All resources are curated and categorized in [`resources/links.md`](resources/links.md):

- 📚 **SQL Learning**: LeetCode, StrataScratch, Mode SQL Tutorial
- 🐍 **Python/Pandas**: Real Python, Pandas Exercises, Kaggle
- 🏗️ **System Design**: System Design Primer, DDIA, ByteByteGo
- ☁️ **Cloud (AWS)**: AWS Skill Builder, Workshop Studio
- 💼 **Interview Prep**: Tech Interview Handbook, STAR method

---

## 🎯 Next Steps

### For Immediate Use

1. ✅ Complete setup: `pip install -r requirements.txt`
2. 📝 Start with easy SQL exercises
3. 🎴 Begin flashcard reviews (15 min daily)
4. 📊 Check progress dashboard daily
5. 🎨 Review system design scenarios

### For Interview Day

1. 📖 Review cheat sheets ([SQL](sql/cheatsheet.md), [Python](python/cheatsheet.md))
2. 🔄 Do final flashcard review
3. 📝 Review company research ([tasq.ai](resources/tasq_ai_research.md))
4. 💪 Warm up with 1-2 easy exercises
5. 🚀 Stay confident—you've prepared systematically!

---

## 🏆 Results & Metrics

### Quantifiable Outcomes

- **Exercises Created**: 30+ SQL, 25+ Python
- **Flashcards**: 75 across 5 categories
- **Time Saved**: Automated testing vs manual validation
- **Retention**: Spaced repetition for long-term memory
- **Coverage**: All key data engineering topics

### The Real Achievement

This system transforms interview prep from:
- ❌ **Passive consumption** → ✅ **Active practice**
- ❌ **Scattered resources** → ✅ **Organized system**
- ❌ **Unknown progress** → ✅ **Data-driven insights**
- ❌ **Wasted time** → ✅ **Optimized learning**

---

## 🤝 Acknowledgments

- **Claude Code**: AI pair programmer for rapid development
- **Rich Library**: Beautiful terminal interfaces
- **SM-2 Algorithm**: SuperMemo spaced repetition
- **Data Engineering Community**: Inspiration and resources

---

## 📄 License

MIT License - Feel free to use this for your own interview prep!

---

## 💬 Feedback & Contributions

This is a living project. As I complete exercises and interviews, I'll:
- ✅ Add more exercises
- ✅ Refine based on actual interview questions
- ✅ Improve based on weak areas discovered
- ✅ Share lessons learned

---

## 🎓 Final Thoughts

**This project demonstrates that with the right tools and mindset, you can build production-quality systems in days, not weeks.**

When I walk into the tasq.ai interview, I'm not just bringing knowledge—I'm bringing **proof of my ability to identify problems, architect solutions, and ship working code.**

**Let's ace this interview! 🚀**

---

*Built with ❤️ and Claude Code in February 2026*
