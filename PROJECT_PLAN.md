# Interview Prep Project - Detailed Task Breakdown

## Phase 1: Foundation Setup (30 minutes)
**Objective**: Get the project structure ready

### Task 1.1: Initialize Project
- [ ] Create directory structure
- [ ] Initialize git repository
- [ ] Create `requirements.txt` with all dependencies
- [ ] Set up virtual environment
- [ ] Create `.gitignore`
- [ ] Write initial `README.md`

```bash
# Automated setup script
mkdir -p interview-prep/{sql,python,system-design,concepts,mock-interviews,progress,resources}/{exercises,solutions,tests}
cd interview-prep
git init
python -m venv venv
source venv/bin/activate
```

**Dependencies**:
```
# requirements.txt
pandas==2.1.0
pytest==7.4.0
rich==13.5.0
requests==2.31.0
beautifulsoup4==4.12.0
SQLAlchemy==2.0.0
faker==19.3.0
black==23.7.0
flake8==6.1.0
```

### Task 1.2: Create Core Utilities
- [ ] `utils/logger.py` - Structured logging
- [ ] `utils/config.py` - Configuration management
- [ ] `utils/database.py` - SQLite helper for SQL practice
- [ ] `utils/test_runner.py` - Universal test executor

---

## Phase 2: SQL Exercise System (3-4 hours)

### Task 2.1: LeetCode SQL Scraper
**File**: `scripts/fetch_leetcode_sql.py`

**Subtasks**:
- [ ] Research LeetCode API/scraping approach
- [ ] Identify 30+ relevant SQL problems:
  - [ ] 10 Easy (JOINs, basic aggregations)
  - [ ] 15 Medium (Window functions, CTEs, complex JOINs)
  - [ ] 5 Hard (Multi-level nesting, optimization)
- [ ] Extract problem metadata:
  - Title
  - Difficulty
  - Description
  - Schema
  - Expected output
- [ ] Save in structured format

**Alternative Sources** (if LeetCode is difficult):
- [ ] StrataScratch
- [ ] HackerRank
- [ ] Mode Analytics SQL Tutorial
- [ ] Manually curate from lists

### Task 2.2: SQL Exercise Template Generator
**File**: `scripts/generate_sql_exercise.py`

```python
def generate_exercise(problem_data: dict) -> None:
    """
    Creates complete exercise folder:
    - problem_statement.md
    - schema.sql
    - sample_data.sql (using Faker)
    - template.sql (empty for student)
    - solution.sql (reference answer)
    - test.py (validator)
    """
    pass
```

**Subtasks**:
- [ ] Create problem statement template
- [ ] Generate realistic sample data (Faker library)
- [ ] Build SQL validator using SQLite
- [ ] Create solution template
- [ ] Add automated test runner

### Task 2.3: SQL Test Framework
**File**: `sql/tests/test_runner.py`

```python
class SQLTestRunner:
    def run_test(self, exercise_path: str, solution_path: str):
        # 1. Load schema and sample data into SQLite
        # 2. Execute student's SQL
        # 3. Compare with expected output
        # 4. Generate diff report
        # 5. Update progress tracker
        pass
```

**Features**:
- [ ] Execute SQL against SQLite in-memory database
- [ ] Compare query results (order-independent)
- [ ] Show visual diff for wrong answers
- [ ] Performance metrics (execution time)
- [ ] Hints system (3 levels)

### Task 2.4: SQL Cheat Sheet
**File**: `sql/cheatsheet.md`

**Sections**:
- [ ] JOIN types with visual diagrams
- [ ] Window functions syntax reference
- [ ] Common Table Expressions (CTEs)
- [ ] Date/time functions
- [ ] String manipulation
- [ ] Aggregation patterns
- [ ] Performance optimization tips
- [ ] Hive/Impala/Trino differences

---

## Phase 3: Python Exercise System (3-4 hours)

### Task 3.1: Python Problem Curator
**File**: `scripts/fetch_python_problems.py`

**Categories & Count**:
1. **Pandas (10 problems)**:
   - [ ] DataFrame filtering
   - [ ] GroupBy operations
   - [ ] Merging/joining
   - [ ] Pivot tables
   - [ ] Time series
   - [ ] Missing data handling
   - [ ] Apply functions
   - [ ] Multi-index
   - [ ] IO operations
   - [ ] Performance optimization

2. **Data Structures (8 problems)**:
   - [ ] List comprehensions
   - [ ] Dict comprehensions
   - [ ] Set operations
   - [ ] Hash tables
   - [ ] Stacks/queues
   - [ ] Trees (basic)
   - [ ] Graphs (dependencies)
   - [ ] Sorting algorithms

3. **Real-World (7 problems)**:
   - [ ] API data fetching
   - [ ] Error handling & retries
   - [ ] File processing (CSV, JSON)
   - [ ] Data validation
   - [ ] Batch processing
   - [ ] Logging & monitoring
   - [ ] Config management

### Task 3.2: Python Exercise Generator
**File**: `scripts/generate_python_exercise.py`

**Template**:
```python
# Each exercise gets:
# 1. Problem description (docstring)
# 2. Function signature with type hints
# 3. Sample data generators
# 4. Comprehensive pytest tests
# 5. Expected time & difficulty
# 6. Related concepts & resources
```

**Subtasks**:
- [ ] Create exercise template with boilerplate
- [ ] Generate test fixtures
- [ ] Add difficulty ratings
- [ ] Include hints system
- [ ] Link to learning resources

### Task 3.3: Python Test Framework
**File**: `python/tests/conftest.py` + individual test files

```python
# pytest-based testing with:
@pytest.fixture
def sample_dataframe():
    """Generate test data"""
    pass

@pytest.mark.parametrize("input,expected", [...])
def test_solution(input, expected):
    """Parameterized tests for edge cases"""
    pass
```

**Features**:
- [ ] Automated test discovery
- [ ] Code coverage reports
- [ ] Performance benchmarks
- [ ] Memory usage tracking
- [ ] Type checking integration (mypy)

### Task 3.4: Code Quality Checker
**File**: `python/code_review.py`

```python
def review_solution(file_path: str) -> dict:
    """
    Returns:
    {
        "pep8_score": 95,
        "complexity": "low",
        "issues": [...],
        "suggestions": [...],
        "performance": "good",
        "compared_to_optimal": {
            "time_complexity": "Same: O(n)",
            "space_complexity": "Worse: O(n) vs O(1)",
            "readability": "Good"
        }
    }
    """
    # Use: black, flake8, pylint, radon (complexity)
    pass
```

### Task 3.5: Python Cheat Sheet
**File**: `python/cheatsheet.md`

**Sections**:
- [ ] Pandas operations quick reference
- [ ] List/dict comprehension patterns
- [ ] Common algorithms
- [ ] Error handling best practices
- [ ] Type hints guide
- [ ] Performance optimization tips
- [ ] Python 3.10+ features

---

## Phase 4: Flashcard System (1-2 hours)

### Task 4.1: Flashcard Generator
**File**: `concepts/flashcards/generator.py`

**Categories**:
1. **Data Engineering Concepts (20 cards)**:
   - ETL vs ELT
   - Batch vs Streaming
   - Data Lake vs Warehouse
   - Star vs Snowflake schema
   - Idempotency
   - Data quality dimensions
   - CAP theorem
   - Eventual consistency
   - Partitioning strategies
   - Indexing strategies
   - Normalization vs Denormalization
   - ACID properties
   - Data lineage
   - Schema evolution
   - Data governance
   - Slowly Changing Dimensions
   - Fact vs Dimension tables
   - Data vault modeling
   - Lambda architecture
   - Kappa architecture

2. **SQL Concepts (15 cards)**:
   - JOIN types
   - Window functions
   - CTEs vs subqueries
   - UNION vs UNION ALL
   - HAVING vs WHERE
   - Indexes
   - Query execution order
   - NULL handling
   - Aggregate functions
   - Correlated subqueries
   - Cross join use cases
   - Temporary tables
   - Views vs Materialized views
   - Transactions & locks
   - Query optimization

3. **Python/Pandas (15 cards)**:
   - List vs tuple
   - Dict vs set
   - Deep vs shallow copy
   - *args vs **kwargs
   - Decorators
   - Generators
   - Context managers
   - GIL (Global Interpreter Lock)
   - DataFrame vs Series
   - loc vs iloc
   - apply vs map
   - merge vs join
   - groupby mechanics
   - Memory optimization
   - Vectorization

4. **System Design (10 cards)**:
   - Load balancing
   - Caching strategies
   - Database replication
   - Sharding
   - Message queues
   - API design principles
   - Microservices
   - Event-driven architecture
   - Circuit breakers
   - Rate limiting

5. **AWS (10 cards)**:
   - S3 use cases
   - Lambda functions
   - Redshift architecture
   - Step Functions
   - ECS vs EKS
   - IAM best practices
   - CloudWatch
   - VPC basics
   - RDS vs DynamoDB
   - CDK overview

### Task 4.2: Flashcard CLI
**File**: `concepts/flashcards/cli.py`

```python
class FlashcardCLI:
    def study_session(self, duration_minutes: int = 15):
        """Interactive study session with spaced repetition"""
        # 1. Select cards due for review
        # 2. Quiz user
        # 3. Update confidence based on answer
        # 4. Calculate next review date
        # 5. Show session summary
        pass
```

**Features**:
- [ ] Spaced repetition algorithm (SM-2)
- [ ] Category filtering
- [ ] Difficulty adjustment
- [ ] Progress tracking
- [ ] Daily goals
- [ ] Beautiful terminal UI (rich library)

---

## Phase 5: Mock Interview Simulator (2-3 hours)

### Task 5.1: Interview Question Bank
**File**: `mock-interviews/questions.json`

```json
{
  "behavioral": [
    {
      "id": 1,
      "question": "Tell me about a time you optimized a slow query",
      "type": "STAR",
      "category": "technical_achievement",
      "suggested_points": [
        "Situation: Describe the slow query impact",
        "Task: What was your goal",
        "Action: Steps you took (EXPLAIN, indexing, etc.)",
        "Result: Performance improvement metrics"
      ]
    }
  ],
  "technical_sql": [...],
  "technical_python": [...],
  "system_design": [...]
}
```

**Behavioral Questions** (prepare 10):
- [ ] Technical achievement
- [ ] Debugging story
- [ ] Teamwork example
- [ ] Handling conflict
- [ ] Learning from failure
- [ ] Time management
- [ ] Taking initiative
- [ ] Handling ambiguity
- [ ] Why this company
- [ ] Career goals

### Task 5.2: Timed Coding Simulator
**File**: `mock-interviews/technical_interview.py`

```python
class TechnicalInterview:
    def __init__(self):
        self.console = Console()
        self.timer = Timer()
        
    def start(self, difficulty: str = "medium"):
        """
        1. Show problem (SQL or Python)
        2. Start 20-minute timer
        3. Provide hints if requested
        4. Auto-evaluate solution
        5. Generate feedback report
        """
        pass
    
    def provide_hint(self, level: int):
        """Progressive hints (3 max)"""
        pass
    
    def evaluate(self, code: str):
        """Run tests and analyze solution"""
        pass
```

**Features**:
- [ ] Countdown timer with visual progress
- [ ] Hint system (deducts points)
- [ ] Live code execution
- [ ] Automated scoring
- [ ] Performance metrics
- [ ] Comparison with optimal solution
- [ ] Interview report (PDF)

### Task 5.3: System Design Practice
**File**: `system-design/scenarios/`

**5 Scenarios** (prepare):
1. **Data Pipeline for Real-Time Analytics**
   - Input: API webhooks, 10K events/sec
   - Output: Dashboard with <1 min latency
   - Discuss: Kafka, streaming, aggregation

2. **Batch ETL for E-commerce**
   - Input: Daily sales files (100GB)
   - Output: Analytical warehouse
   - Discuss: Airflow, Spark, Redshift

3. **Data Quality System**
   - Monitor data freshness, completeness, accuracy
   - Alert on anomalies
   - Discuss: Great Expectations, monitoring

4. **AI Training Data Pipeline**
   - Collect, label, validate training data
   - Version control
   - Discuss: MLOps, data versioning

5. **Multi-Source Data Integration**
   - Combine data from APIs, databases, files
   - Handle schema changes
   - Discuss: CDC, schema registry

**Template**:
```markdown
# Scenario: [Name]

## Requirements
- [Functional requirement 1]
- [Non-functional: scale, latency, etc.]

## My Solution
[Draw architecture diagram]

### Components
1. **Ingestion Layer**: ...
2. **Processing Layer**: ...
3. **Storage Layer**: ...
4. **Serving Layer**: ...

### Technology Choices
- Tool X because...

### Trade-offs
- Chose X over Y because...

### Scalability
- How it handles 10x traffic

### Monitoring & Alerting
- Key metrics to track

## Evaluation Rubric
- [ ] Covers all requirements
- [ ] Discusses trade-offs
- [ ] Mentions monitoring
- [ ] Considers edge cases
- [ ] Realistic tech choices
```

---

## Phase 6: Progress Tracking (1 hour)

### Task 6.1: Progress Tracker
**File**: `progress/tracker.json`

```json
{
  "start_date": "2025-02-15",
  "interview_date": "2025-02-17",
  "sql_exercises": {
    "completed": 0,
    "total": 30,
    "by_difficulty": {...},
    "by_topic": {...}
  },
  "python_exercises": {...},
  "flashcards": {
    "total_reviews": 0,
    "cards_mastered": 0,
    "average_confidence": 0
  },
  "mock_interviews": [],
  "time_spent_minutes": 0,
  "daily_logs": []
}
```

### Task 6.2: Analytics Dashboard
**File**: `progress/analytics.py`

```python
def generate_report():
    """
    Creates daily progress report:
    - Completion percentage
    - Time spent
    - Weak areas
    - Recommended next steps
    - Motivational message
    """
    pass

def visualize_progress():
    """
    ASCII charts for:
    - Completion over time
    - Accuracy by topic
    - Time distribution
    """
    pass
```

**Output Example**:
```
╔════════════════════════════════════════════════╗
║     Interview Prep - Day 2 Summary             ║
╚════════════════════════════════════════════════╝

📊 Overall Progress: ████████░░ 76%

SQL Exercises:       ████████░░ 80% (24/30)
  ✅ Easy:           100% (10/10)
  ✅ Medium:         73% (11/15) 
  ⚠️  Hard:          60% (3/5)

Python Exercises:    ███████░░░ 72% (18/25)
  ✅ Pandas:         90% (9/10)
  ⚠️  Algorithms:    62% (5/8)
  ✅ Real-World:     57% (4/7)

Flashcards:          ██████░░░░ 64% (48/75)
  Confidence 4-5:    30 cards
  Needs Review:      18 cards

Mock Interviews:     2 completed
  Avg Score:         78/100

⏱️  Time Invested:   8h 45m total
  Today:            3h 30m
  SQL:              1h 45m
  Python:           1h 20m
  Flashcards:       25m

🎯 Next Steps:
  1. Complete 4 more SQL Hard problems
  2. Review Algorithms (weak area)
  3. Study AWS flashcards (0% reviewed)
  4. Do 1 mock interview

💪 You're on track! Interview in 2 days.
```

### Task 6.3: Daily Goals Generator
**File**: `progress/daily_goals.md`

```python
def generate_daily_plan(days_until_interview: int):
    """
    Smart planning based on:
    - Remaining exercises
    - Weak areas
    - Time available
    - Interview proximity
    """
    pass
```

---

## Phase 7: Resources & References (1 hour)

### Task 7.1: Curated Learning Links
**File**: `resources/links.md`

**Categories**:
- [ ] **SQL Tutorials**
  - Mode SQL Tutorial
  - SQLZoo
  - W3Schools SQL
  
- [ ] **Python/Pandas**
  - Real Python
  - Pandas documentation
  - Kaggle Learn

- [ ] **System Design**
  - System Design Primer (GitHub)
  - Designing Data-Intensive Applications
  - AWS Architecture Blog

- [ ] **Data Engineering**
  - Data Engineering Cookbook
  - Airflow documentation
  - DBT documentation

- [ ] **Interview Prep**
  - STAR method guide
  - Salary negotiation tips
  - Thank you email templates

### Task 7.2: tasq.ai Research
**File**: `resources/tasq_ai_research.md`

**Automated Research**:
```python
def research_company(company_name: str):
    """
    Scrape & summarize:
    - Company website
    - LinkedIn page
    - Recent news
    - Employee reviews
    - Tech stack (from job postings)
    """
    pass
```

**Manual Sections**:
- [ ] Company mission & values
- [ ] Products & services
- [ ] Target customers
- [ ] Recent news/funding
- [ ] Team structure
- [ ] Culture insights
- [ ] Potential questions to ask
- [ ] How my skills align

---

## Phase 8: Interview Day Kit (30 minutes)

### Task 8.1: Pre-Interview Checklist
**File**: `interview-day/checklist.md`

```markdown
## 1 Day Before
- [ ] Review cheat sheets
- [ ] Do 1 mock interview
- [ ] Review weak areas
- [ ] Prepare questions for them
- [ ] Test Zoom/setup

## Morning Of
- [ ] 15-minute quick review
- [ ] Review company research
- [ ] Prepare STAR examples
- [ ] Check equipment

## During Interview
- [ ] Think out loud
- [ ] Ask clarifying questions
- [ ] Manage time
- [ ] Take notes

## After Interview
- [ ] Send thank you email (within 24h)
- [ ] Note topics discussed
- [ ] Reflect on performance
```

### Task 8.2: Portfolio Presentation
**File**: `interview-day/portfolio.md`

```markdown
# How I Prepared for This Interview

"I'd like to show you something interesting about my preparation process..."

## The Challenge
I had 2 days to prepare for a data engineering interview covering SQL, Python, system design, and your specific tech stack.

## My Approach
Instead of passive studying, I built an AI-powered learning system:

1. **Automated Exercise Generation**
   - Curated 30 SQL + 25 Python problems
   - Auto-generated tests and validation
   - Progress tracking & analytics

2. **Smart Learning Tools**
   - Flashcard system with spaced repetition
   - Mock interview simulator
   - Code quality analyzer
   - Weak area identification

3. **Results**
   - [Show progress dashboard]
   - Completed X exercises in Y hours
   - Identified and improved weak areas
   - Practiced under interview conditions

## Why This Matters
This demonstrates how I:
- Use AI to solve real problems
- Build production-quality tools quickly
- Approach learning systematically
- Measure and optimize my progress

[Link to GitHub repo]
```

### Task 8.3: Quick Review Guide
**File**: `interview-day/quick_review.md`

```markdown
# 15-Minute Pre-Interview Review

## Top 10 SQL Patterns (5 min)
1. INNER JOIN: ...
2. LEFT JOIN NULL check: ...
3. ROW_NUMBER() for ranking: ...
...

## Top 10 Python Patterns (5 min)
1. List comprehension: ...
2. Dict.get() with default: ...
...

## Key Talking Points (5 min)
About Me:
- "I build petabyte-scale data infrastructure at PMO..."
- "I've developed production RAG chatbots..."
- "Currently working on SoftLanding, an AI platform..."

Why tasq.ai:
- "Intersection of AI and data quality fascinates me..."
- "My RAG chatbot experience aligns with your AI agents work..."

Questions for Them:
- "What does your data pipeline architecture look like?"
- "How do you handle data quality validation?"
- "What's the team's approach to testing?"
```

---

## Phase 9: Automation & Quality (Ongoing)

### Task 9.1: Makefile for Common Tasks
**File**: `Makefile`

```makefile
.PHONY: setup test review progress clean

setup:
	python -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	python scripts/initialize_database.py

test-sql:
	python sql/tests/test_runner.py

test-python:
	pytest python/tests/ -v

review:
	python progress/analytics.py

study-flashcards:
	python concepts/flashcards/cli.py

mock-interview:
	python mock-interviews/technical_interview.py

progress:
	python progress/analytics.py --report=daily

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
```

### Task 9.2: GitHub Actions (Optional)
**File**: `.github/workflows/test.yml`

```yaml
name: Test Solutions

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run SQL tests
        run: python sql/tests/test_runner.py
      - name: Run Python tests
        run: pytest
```

---

## Success Metrics

### By End of Day 1 (Saturday):
- [ ] Project structure complete
- [ ] 15 SQL exercises ready with tests
- [ ] 12 Python exercises ready with tests
- [ ] 40 flashcards created
- [ ] SQL cheat sheet complete
- [ ] Progress tracker working

### By End of Day 2 (Sunday):
- [ ] All 30 SQL exercises completed
- [ ] All 25 Python exercises completed
- [ ] 75 flashcards reviewed
- [ ] 2 mock interviews done
- [ ] System design scenarios prepared
- [ ] Company research complete
- [ ] Portfolio document ready

### Interview Day (Monday):
- [ ] 15-minute review done
- [ ] Equipment tested
- [ ] Questions prepared
- [ ] Confident & ready! 🚀

---

## Time Allocation

| Phase | Estimated Time | Priority |
|-------|---------------|----------|
| Foundation Setup | 30 min | P0 |
| SQL System | 3-4 hours | P0 |
| Python System | 3-4 hours | P0 |
| Flashcards | 1-2 hours | P1 |
| Mock Interviews | 2-3 hours | P1 |
| Progress Tracking | 1 hour | P2 |
| Resources | 1 hour | P2 |
| Interview Kit | 30 min | P1 |
| **Total** | **12-16 hours** | - |

---

## Execution Strategy

### Saturday (Day 1): Foundation + SQL
- Morning: Setup + SQL exercise generation (4h)
- Afternoon: Practice 10-15 SQL problems (3h)
- Evening: Python setup + 5 problems (2h)

### Sunday (Day 2): Completion + Practice
- Morning: Finish Python exercises (2h)
- Afternoon: Flashcards + Mock interviews (3h)
- Evening: System design + Final review (2h)

### Monday (Interview Day): Light review
- Morning: 15-min quick review
- Keep calm, you're prepared! 💪

---

## Notes for Claude Code

Please implement this systematically:

1. **Start with `PROJECT_PLAN.md`** - Use it as a checklist
2. **Build incrementally** - Test each component
3. **Prioritize quality** - Production-grade code
4. **Automate everything** - Minimal manual work
5. **Make it beautiful** - Rich terminal UI
6. **Think showcase** - This is portfolio material

Let's build something I can be proud to show at the interview! 🎯
