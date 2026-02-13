# -*- coding: utf-8 -*-
"""
Technical Mock Interview Simulator for Data Engineering preparation.

A full-featured CLI tool that simulates timed technical interviews with
multiple question types, hint systems, auto-evaluation, and session reporting.

Usage:
    python mock-interviews/technical_interview.py

Requires: rich, python 3.13+
"""

import json
import logging
import os
import random
import subprocess
import sys
import tempfile
import textwrap
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.text import Text
from rich.rule import Rule
from rich.align import Align
from rich import box

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("mock_interview")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
SESSIONS_DIR = BASE_DIR / "sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Console
# ---------------------------------------------------------------------------
console = Console()

# ---------------------------------------------------------------------------
# Question dataclass-style dicts
# ---------------------------------------------------------------------------

BEHAVIORAL_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": "beh_01",
        "title": "Handling a Tight Deadline",
        "prompt": (
            "Tell me about a time when you had to deliver a project under a very "
            "tight deadline. How did you prioritize tasks, manage your time, and "
            "what was the outcome?"
        ),
        "follow_up": "What would you do differently if you faced the same situation again?",
        "hints": [
            "Use the STAR method: Situation, Task, Action, Result.",
            "Focus on concrete actions you took, not just the pressure you felt.",
            "Mention how you communicated progress or blockers to stakeholders.",
        ],
        "evaluation_criteria": [
            "Uses a structured answer (STAR or similar)",
            "Gives specific examples with measurable outcomes",
            "Shows self-awareness and learning",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "beh_02",
        "title": "Conflict with a Teammate",
        "prompt": (
            "Describe a situation where you had a disagreement with a colleague "
            "about a technical approach. How did you handle it and what was the "
            "resolution?"
        ),
        "follow_up": "How do you generally approach technical disagreements?",
        "hints": [
            "Show that you listen to the other person's perspective first.",
            "Emphasize data-driven decision making over personal preference.",
            "Mention the relationship outcome, not just the technical outcome.",
        ],
        "evaluation_criteria": [
            "Demonstrates empathy and active listening",
            "Shows willingness to compromise or use data to decide",
            "Maintains professional relationship",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "beh_03",
        "title": "Learning a New Technology Quickly",
        "prompt": (
            "Give an example of a time you had to learn a new technology or tool "
            "quickly to complete a project. What was the technology, how did you "
            "approach learning it, and what was the result?"
        ),
        "follow_up": "What is your general strategy for picking up new tools?",
        "hints": [
            "Describe your learning process step by step.",
            "Mention specific resources you used (docs, tutorials, mentors).",
            "Quantify the outcome -- how fast did you become productive?",
        ],
        "evaluation_criteria": [
            "Shows a systematic learning approach",
            "Demonstrates resourcefulness",
            "Connects learning to project success",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "beh_04",
        "title": "Dealing with Ambiguous Requirements",
        "prompt": (
            "Tell me about a project where the requirements were unclear or kept "
            "changing. How did you handle the ambiguity and still deliver value?"
        ),
        "follow_up": "How do you proactively reduce ambiguity in future projects?",
        "hints": [
            "Explain how you sought clarification from stakeholders.",
            "Mention iterative approaches or prototyping to validate assumptions.",
            "Show how you documented decisions to prevent future confusion.",
        ],
        "evaluation_criteria": [
            "Proactive communication with stakeholders",
            "Iterative delivery to reduce risk",
            "Documentation and decision tracking",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "beh_05",
        "title": "A Mistake You Made and How You Fixed It",
        "prompt": (
            "Describe a significant mistake you made in a work or academic project. "
            "What happened, how did you discover it, and what did you do to fix it?"
        ),
        "follow_up": "What processes or habits did you adopt to prevent similar mistakes?",
        "hints": [
            "Be honest about the mistake -- interviewers value authenticity.",
            "Focus most of your answer on the recovery and lessons learned.",
            "Mention any systemic improvements you introduced afterward.",
        ],
        "evaluation_criteria": [
            "Demonstrates accountability",
            "Shows problem-solving under pressure",
            "Implements preventive measures",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "beh_06",
        "title": "Why Data Engineering at tasq.ai",
        "prompt": (
            "Why are you interested in a Junior Data Engineer role at tasq.ai "
            "specifically? What excites you about the company and the position?"
        ),
        "follow_up": "Where do you see yourself growing in the next two years in this role?",
        "hints": [
            "Research tasq.ai's product and mention specifics.",
            "Connect your skills and interests to the job description.",
            "Show genuine enthusiasm, not generic answers.",
        ],
        "evaluation_criteria": [
            "Demonstrates company research",
            "Connects personal goals to role",
            "Shows genuine enthusiasm",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "beh_07",
        "title": "Working with Data Quality Issues",
        "prompt": (
            "Tell me about a time you encountered messy or unreliable data. "
            "How did you identify the issues and what steps did you take to "
            "clean or validate the data?"
        ),
        "follow_up": "How would you design a data quality framework from scratch?",
        "hints": [
            "Describe the specific data quality issues (nulls, duplicates, schema drift).",
            "Explain the tools or techniques you used for validation.",
            "Mention the business impact of having clean data.",
        ],
        "evaluation_criteria": [
            "Identifies data quality dimensions",
            "Uses systematic cleaning approach",
            "Understands business impact",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "beh_08",
        "title": "Collaboration on a Cross-functional Team",
        "prompt": (
            "Describe a time when you worked with people from different backgrounds "
            "or departments (e.g., analysts, product managers, backend engineers). "
            "How did you ensure effective communication?"
        ),
        "follow_up": "What tools or practices help you collaborate across teams?",
        "hints": [
            "Highlight how you adapted your communication style for different audiences.",
            "Mention any shared documentation or alignment meetings.",
            "Give a concrete outcome of the collaboration.",
        ],
        "evaluation_criteria": [
            "Adapts communication to audience",
            "Uses collaboration tools effectively",
            "Achieves shared goals",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "beh_09",
        "title": "Going Above and Beyond",
        "prompt": (
            "Can you share an example where you went beyond what was expected of you "
            "in a project or role? What motivated you and what was the impact?"
        ),
        "follow_up": "How do you balance going the extra mile with avoiding burnout?",
        "hints": [
            "Pick an example where your extra effort had measurable impact.",
            "Explain your intrinsic motivation, not just obligation.",
            "Show awareness of sustainable work habits.",
        ],
        "evaluation_criteria": [
            "Demonstrates initiative",
            "Shows measurable impact",
            "Maintains healthy boundaries",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "beh_10",
        "title": "Receiving Critical Feedback",
        "prompt": (
            "Tell me about a time you received tough feedback on your work. "
            "How did you react, and what changes did you make as a result?"
        ),
        "follow_up": "How do you actively seek feedback in your day-to-day work?",
        "hints": [
            "Show you can separate feedback on work from personal criticism.",
            "Describe the concrete changes you made after receiving feedback.",
            "Mention how the feedback improved your subsequent work.",
        ],
        "evaluation_criteria": [
            "Demonstrates openness to feedback",
            "Takes concrete action",
            "Shows growth mindset",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "beh_11",
        "title": "Explaining a Technical Concept to a Non-Technical Person",
        "prompt": (
            "Describe a time when you had to explain a complex technical concept "
            "to someone without a technical background. How did you approach it "
            "and was the explanation successful?"
        ),
        "follow_up": "What analogies or techniques do you find most effective?",
        "hints": [
            "Use analogies or real-world comparisons.",
            "Focus on the 'why it matters' before the 'how it works'.",
            "Check for understanding by asking questions.",
        ],
        "evaluation_criteria": [
            "Uses clear analogies",
            "Adapts depth to audience",
            "Confirms understanding",
        ],
        "time_limit_minutes": 5,
    },
]

SQL_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": "sql_01",
        "title": "Revenue by Product Category",
        "prompt": (
            "Write a SQL query that returns the total revenue for each product "
            "category, ordered by revenue descending. The tables are:\n\n"
            "  orders(order_id INT, product_id INT, quantity INT, order_date DATE)\n"
            "  products(product_id INT, product_name VARCHAR, category VARCHAR, price DECIMAL)\n\n"
            "Include only categories with total revenue above 1000."
        ),
        "expected_keywords": ["JOIN", "GROUP BY", "HAVING", "ORDER BY", "SUM"],
        "sample_solution": textwrap.dedent("""\
            SELECT p.category,
                   SUM(o.quantity * p.price) AS total_revenue
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            GROUP BY p.category
            HAVING SUM(o.quantity * p.price) > 1000
            ORDER BY total_revenue DESC;
        """),
        "hints": [
            "You need to JOIN orders with products on product_id.",
            "Use SUM(quantity * price) for revenue, then GROUP BY category.",
            "Use HAVING to filter groups after aggregation, and ORDER BY ... DESC.",
        ],
        "difficulty": "easy",
        "time_limit_minutes": 15,
        "topics": ["JOIN", "GROUP BY", "HAVING", "aggregation"],
    },
    {
        "id": "sql_02",
        "title": "Running Total of Daily Sales",
        "prompt": (
            "Given a table daily_sales(sale_date DATE, amount DECIMAL), write a "
            "query that returns each date along with a running total of the amount "
            "column, ordered by sale_date."
        ),
        "expected_keywords": ["SUM", "OVER", "ORDER BY"],
        "sample_solution": textwrap.dedent("""\
            SELECT sale_date,
                   amount,
                   SUM(amount) OVER (ORDER BY sale_date) AS running_total
            FROM daily_sales
            ORDER BY sale_date;
        """),
        "hints": [
            "This requires a window function, not a regular GROUP BY.",
            "Use SUM(amount) OVER (ORDER BY sale_date) to compute the running total.",
            "The default window frame for ORDER BY in a window is UNBOUNDED PRECEDING to CURRENT ROW.",
        ],
        "difficulty": "medium",
        "time_limit_minutes": 15,
        "topics": ["window functions", "running total"],
    },
    {
        "id": "sql_03",
        "title": "Top 3 Customers per Region",
        "prompt": (
            "Write a query to find the top 3 customers by total spending in each region.\n\n"
            "  customers(customer_id INT, name VARCHAR, region VARCHAR)\n"
            "  orders(order_id INT, customer_id INT, amount DECIMAL)\n\n"
            "Return region, customer name, total_spent, and their rank within the region."
        ),
        "expected_keywords": ["ROW_NUMBER", "RANK", "DENSE_RANK", "PARTITION BY", "CTE", "WITH"],
        "sample_solution": textwrap.dedent("""\
            WITH ranked AS (
                SELECT c.region,
                       c.name,
                       SUM(o.amount) AS total_spent,
                       ROW_NUMBER() OVER (PARTITION BY c.region ORDER BY SUM(o.amount) DESC) AS rn
                FROM customers c
                JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.region, c.name
            )
            SELECT region, name, total_spent, rn AS rank
            FROM ranked
            WHERE rn <= 3
            ORDER BY region, rn;
        """),
        "hints": [
            "Use a CTE (WITH clause) to first compute per-customer totals with a ranking.",
            "Use ROW_NUMBER() or RANK() with PARTITION BY region ORDER BY total DESC.",
            "Filter to rn <= 3 in the outer query.",
        ],
        "difficulty": "medium",
        "time_limit_minutes": 15,
        "topics": ["CTE", "window functions", "PARTITION BY", "JOIN"],
    },
    {
        "id": "sql_04",
        "title": "Consecutive Active Days",
        "prompt": (
            "Given a table user_logins(user_id INT, login_date DATE), find all "
            "users who logged in for at least 3 consecutive days. Return user_id "
            "and the start date of their first 3-day streak."
        ),
        "expected_keywords": ["LAG", "LEAD", "ROW_NUMBER", "DATE", "GROUP"],
        "sample_solution": textwrap.dedent("""\
            WITH numbered AS (
                SELECT user_id,
                       login_date,
                       login_date - INTERVAL '1 day' * ROW_NUMBER()
                           OVER (PARTITION BY user_id ORDER BY login_date) AS grp
                FROM (SELECT DISTINCT user_id, login_date FROM user_logins) t
            ),
            streaks AS (
                SELECT user_id,
                       MIN(login_date) AS streak_start,
                       COUNT(*) AS streak_length
                FROM numbered
                GROUP BY user_id, grp
                HAVING COUNT(*) >= 3
            )
            SELECT user_id, streak_start
            FROM streaks
            ORDER BY user_id, streak_start;
        """),
        "hints": [
            "The classic trick: subtract a row number from the date to create a group identifier for consecutive dates.",
            "First, deduplicate login dates per user. Then assign ROW_NUMBER partitioned by user ordered by date.",
            "Group by user_id and the computed group, filter streaks with HAVING COUNT(*) >= 3.",
        ],
        "difficulty": "hard",
        "time_limit_minutes": 15,
        "topics": ["consecutive sequences", "window functions", "CTE", "date arithmetic"],
    },
    {
        "id": "sql_05",
        "title": "Year-over-Year Growth Rate",
        "prompt": (
            "Given a table monthly_revenue(year INT, month INT, revenue DECIMAL), "
            "write a query that computes the year-over-year growth rate for each "
            "month. Return year, month, revenue, previous_year_revenue, and "
            "growth_rate_pct (as a percentage)."
        ),
        "expected_keywords": ["LAG", "OVER", "PARTITION BY"],
        "sample_solution": textwrap.dedent("""\
            SELECT year,
                   month,
                   revenue,
                   LAG(revenue) OVER (PARTITION BY month ORDER BY year) AS previous_year_revenue,
                   ROUND(
                       (revenue - LAG(revenue) OVER (PARTITION BY month ORDER BY year))
                       / LAG(revenue) OVER (PARTITION BY month ORDER BY year) * 100, 2
                   ) AS growth_rate_pct
            FROM monthly_revenue
            ORDER BY month, year;
        """),
        "hints": [
            "Use LAG() to look back exactly one year for the same month.",
            "PARTITION BY month ORDER BY year gives you the right comparison.",
            "Growth rate = (current - previous) / previous * 100.",
        ],
        "difficulty": "medium",
        "time_limit_minutes": 15,
        "topics": ["LAG", "window functions", "PARTITION BY"],
    },
    {
        "id": "sql_06",
        "title": "Pivot Monthly Sales by Quarter",
        "prompt": (
            "Given a table sales(sale_id INT, sale_date DATE, amount DECIMAL), "
            "write a query that pivots the data to show total sales per year with "
            "separate columns for Q1, Q2, Q3, and Q4."
        ),
        "expected_keywords": ["CASE", "SUM", "EXTRACT", "GROUP BY"],
        "sample_solution": textwrap.dedent("""\
            SELECT EXTRACT(YEAR FROM sale_date) AS sale_year,
                   SUM(CASE WHEN EXTRACT(QUARTER FROM sale_date) = 1 THEN amount ELSE 0 END) AS q1,
                   SUM(CASE WHEN EXTRACT(QUARTER FROM sale_date) = 2 THEN amount ELSE 0 END) AS q2,
                   SUM(CASE WHEN EXTRACT(QUARTER FROM sale_date) = 3 THEN amount ELSE 0 END) AS q3,
                   SUM(CASE WHEN EXTRACT(QUARTER FROM sale_date) = 4 THEN amount ELSE 0 END) AS q4
            FROM sales
            GROUP BY EXTRACT(YEAR FROM sale_date)
            ORDER BY sale_year;
        """),
        "hints": [
            "Use conditional aggregation with CASE WHEN inside SUM.",
            "EXTRACT(QUARTER FROM sale_date) gives you the quarter number.",
            "Group by year to get one row per year.",
        ],
        "difficulty": "medium",
        "time_limit_minutes": 15,
        "topics": ["CASE WHEN", "pivot", "aggregation"],
    },
    {
        "id": "sql_07",
        "title": "Find Duplicate Records",
        "prompt": (
            "Given a table employees(emp_id INT, first_name VARCHAR, last_name VARCHAR, "
            "email VARCHAR, hire_date DATE), write a query that finds all duplicate "
            "email addresses and returns the email, the count of duplicates, and "
            "the emp_ids involved (as a comma-separated string)."
        ),
        "expected_keywords": ["GROUP BY", "HAVING", "COUNT", "STRING_AGG"],
        "sample_solution": textwrap.dedent("""\
            SELECT email,
                   COUNT(*) AS duplicate_count,
                   STRING_AGG(CAST(emp_id AS VARCHAR), ', ' ORDER BY emp_id) AS emp_ids
            FROM employees
            GROUP BY email
            HAVING COUNT(*) > 1
            ORDER BY duplicate_count DESC;
        """),
        "hints": [
            "Group by email and use HAVING COUNT(*) > 1 to find duplicates.",
            "Use STRING_AGG (PostgreSQL) or GROUP_CONCAT (MySQL) to combine emp_ids.",
            "Order by duplicate_count DESC to show worst offenders first.",
        ],
        "difficulty": "easy",
        "time_limit_minutes": 15,
        "topics": ["GROUP BY", "HAVING", "STRING_AGG", "duplicates"],
    },
    {
        "id": "sql_08",
        "title": "Recursive CTE for Org Chart",
        "prompt": (
            "Given a table employees(emp_id INT, name VARCHAR, manager_id INT), "
            "write a recursive CTE that returns the full reporting chain for "
            "employee with emp_id = 10. Include emp_id, name, manager_id, and "
            "the level in the hierarchy (0 for the employee, 1 for their manager, etc.)."
        ),
        "expected_keywords": ["WITH RECURSIVE", "UNION ALL", "CTE"],
        "sample_solution": textwrap.dedent("""\
            WITH RECURSIVE chain AS (
                SELECT emp_id, name, manager_id, 0 AS level
                FROM employees
                WHERE emp_id = 10
                UNION ALL
                SELECT e.emp_id, e.name, e.manager_id, c.level + 1
                FROM employees e
                JOIN chain c ON e.emp_id = c.manager_id
            )
            SELECT emp_id, name, manager_id, level
            FROM chain
            ORDER BY level;
        """),
        "hints": [
            "Start the recursive CTE with the base case: WHERE emp_id = 10.",
            "The recursive part joins employees ON emp_id = previous.manager_id.",
            "Increment level by 1 at each step.",
        ],
        "difficulty": "hard",
        "time_limit_minutes": 15,
        "topics": ["recursive CTE", "hierarchy", "UNION ALL"],
    },
    {
        "id": "sql_09",
        "title": "Sessionization of User Events",
        "prompt": (
            "Given a table events(user_id INT, event_time TIMESTAMP, event_type VARCHAR), "
            "define a session as a sequence of events by the same user where no two "
            "consecutive events are more than 30 minutes apart. Write a query that "
            "assigns a session_id to each event."
        ),
        "expected_keywords": ["LAG", "OVER", "PARTITION BY", "SUM", "CASE"],
        "sample_solution": textwrap.dedent("""\
            WITH time_diffs AS (
                SELECT *,
                       LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) AS prev_time
                FROM events
            ),
            flagged AS (
                SELECT *,
                       CASE
                           WHEN prev_time IS NULL THEN 1
                           WHEN EXTRACT(EPOCH FROM (event_time - prev_time)) > 1800 THEN 1
                           ELSE 0
                       END AS new_session_flag
                FROM time_diffs
            )
            SELECT user_id,
                   event_time,
                   event_type,
                   SUM(new_session_flag) OVER (
                       PARTITION BY user_id ORDER BY event_time
                   ) AS session_id
            FROM flagged
            ORDER BY user_id, event_time;
        """),
        "hints": [
            "Use LAG to get the previous event time per user.",
            "Flag rows where the gap exceeds 30 minutes (1800 seconds) as a new session.",
            "Use a cumulative SUM of that flag to assign session IDs.",
        ],
        "difficulty": "hard",
        "time_limit_minutes": 15,
        "topics": ["sessionization", "LAG", "window functions", "CASE"],
    },
    {
        "id": "sql_10",
        "title": "Gaps in Sequential IDs",
        "prompt": (
            "Given a table invoices(invoice_id INT), where invoice_id values should be "
            "sequential but some are missing, write a query that finds all the gaps. "
            "Return gap_start and gap_end for each missing range."
        ),
        "expected_keywords": ["LEAD", "OVER", "WHERE"],
        "sample_solution": textwrap.dedent("""\
            SELECT invoice_id + 1 AS gap_start,
                   next_id - 1 AS gap_end
            FROM (
                SELECT invoice_id,
                       LEAD(invoice_id) OVER (ORDER BY invoice_id) AS next_id
                FROM invoices
            ) t
            WHERE next_id - invoice_id > 1
            ORDER BY gap_start;
        """),
        "hints": [
            "Use LEAD to peek at the next invoice_id in sorted order.",
            "A gap exists wherever next_id - current_id > 1.",
            "The gap range is (current_id + 1) to (next_id - 1).",
        ],
        "difficulty": "medium",
        "time_limit_minutes": 15,
        "topics": ["LEAD", "window functions", "gaps and islands"],
    },
    {
        "id": "sql_11",
        "title": "Cumulative Percentage of Total",
        "prompt": (
            "Given a table product_sales(product VARCHAR, revenue DECIMAL), write "
            "a query that returns each product, its revenue, the cumulative revenue "
            "(ordered by revenue DESC), and the cumulative percentage of total revenue. "
            "This is useful for Pareto (80/20) analysis."
        ),
        "expected_keywords": ["SUM", "OVER", "ORDER BY"],
        "sample_solution": textwrap.dedent("""\
            SELECT product,
                   revenue,
                   SUM(revenue) OVER (ORDER BY revenue DESC) AS cumulative_revenue,
                   ROUND(
                       SUM(revenue) OVER (ORDER BY revenue DESC)
                       / SUM(revenue) OVER () * 100, 2
                   ) AS cumulative_pct
            FROM product_sales
            ORDER BY revenue DESC;
        """),
        "hints": [
            "Use SUM(revenue) OVER (ORDER BY revenue DESC) for cumulative revenue.",
            "Use SUM(revenue) OVER () -- with empty OVER -- for the grand total.",
            "Divide cumulative by total and multiply by 100 for percentage.",
        ],
        "difficulty": "medium",
        "time_limit_minutes": 15,
        "topics": ["window functions", "cumulative sum", "Pareto analysis"],
    },
]

PYTHON_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": "py_01",
        "title": "Flatten Nested Dictionary",
        "prompt": (
            "Write a function flatten_dict(d: dict, parent_key: str = '', sep: str = '.') -> dict "
            "that flattens a nested dictionary.\n\n"
            "Example:\n"
            "  Input:  {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}\n"
            "  Output: {'a': 1, 'b.c': 2, 'b.d.e': 3}"
        ),
        "test_code": textwrap.dedent("""\
            result1 = flatten_dict({'a': 1, 'b': {'c': 2, 'd': {'e': 3}}})
            assert result1 == {'a': 1, 'b.c': 2, 'b.d.e': 3}, f"Test 1 failed: {result1}"

            result2 = flatten_dict({})
            assert result2 == {}, f"Test 2 failed: {result2}"

            result3 = flatten_dict({'x': {'y': {'z': 42}}})
            assert result3 == {'x.y.z': 42}, f"Test 3 failed: {result3}"

            result4 = flatten_dict({'a': 1, 'b': 2})
            assert result4 == {'a': 1, 'b': 2}, f"Test 4 failed: {result4}"

            print("All tests passed!")
        """),
        "sample_solution": textwrap.dedent("""\
            def flatten_dict(d: dict, parent_key: str = '', sep: str = '.') -> dict:
                items: list[tuple[str, object]] = []
                for k, v in d.items():
                    new_key = f"{parent_key}{sep}{k}" if parent_key else k
                    if isinstance(v, dict):
                        items.extend(flatten_dict(v, new_key, sep).items())
                    else:
                        items.append((new_key, v))
                return dict(items)
        """),
        "hints": [
            "Use recursion: if a value is a dict, recurse with an updated parent key.",
            "Build the new key as parent_key + sep + current_key when parent_key is non-empty.",
            "Collect results in a list of (key, value) tuples and convert to dict at the end.",
        ],
        "difficulty": "easy",
        "time_limit_minutes": 20,
        "topics": ["recursion", "dictionaries"],
    },
    {
        "id": "py_02",
        "title": "Group Anagrams",
        "prompt": (
            "Write a function group_anagrams(words: list[str]) -> list[list[str]] "
            "that groups a list of strings into anagram groups.\n\n"
            "Example:\n"
            "  Input:  ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']\n"
            "  Output: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]"
        ),
        "test_code": textwrap.dedent("""\
            result = group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])
            result_sorted = [sorted(g) for g in result]
            result_sorted.sort()
            expected = [['ate', 'eat', 'tea'], ['nat', 'tan'], ['bat']]
            expected.sort()
            assert result_sorted == expected, f"Test 1 failed: {result_sorted}"

            result2 = group_anagrams([''])
            assert result2 == [['']], f"Test 2 failed: {result2}"

            result3 = group_anagrams(['a'])
            assert result3 == [['a']], f"Test 3 failed: {result3}"

            print("All tests passed!")
        """),
        "sample_solution": textwrap.dedent("""\
            from collections import defaultdict

            def group_anagrams(words: list[str]) -> list[list[str]]:
                groups: dict[str, list[str]] = defaultdict(list)
                for word in words:
                    key = ''.join(sorted(word))
                    groups[key].append(word)
                return list(groups.values())
        """),
        "hints": [
            "Anagrams have the same letters when sorted. Use sorted(word) as a grouping key.",
            "Use a defaultdict(list) to collect words sharing the same sorted key.",
            "Return the values of the dictionary as a list of lists.",
        ],
        "difficulty": "easy",
        "time_limit_minutes": 20,
        "topics": ["hash maps", "sorting", "string manipulation"],
    },
    {
        "id": "py_03",
        "title": "LRU Cache Implementation",
        "prompt": (
            "Implement an LRU (Least Recently Used) cache class with the following interface:\n\n"
            "  class LRUCache:\n"
            "      def __init__(self, capacity: int): ...\n"
            "      def get(self, key: int) -> int:  # returns -1 if not found\n"
            "      def put(self, key: int, value: int) -> None:\n\n"
            "Both get and put should run in O(1) average time."
        ),
        "test_code": textwrap.dedent("""\
            cache = LRUCache(2)
            cache.put(1, 1)
            cache.put(2, 2)
            assert cache.get(1) == 1, "Test 1 failed"
            cache.put(3, 3)  # evicts key 2
            assert cache.get(2) == -1, "Test 2 failed"
            cache.put(4, 4)  # evicts key 1
            assert cache.get(1) == -1, "Test 3 failed"
            assert cache.get(3) == 3, "Test 4 failed"
            assert cache.get(4) == 4, "Test 5 failed"

            print("All tests passed!")
        """),
        "sample_solution": textwrap.dedent("""\
            from collections import OrderedDict

            class LRUCache:
                def __init__(self, capacity: int):
                    self.capacity = capacity
                    self.cache: OrderedDict[int, int] = OrderedDict()

                def get(self, key: int) -> int:
                    if key not in self.cache:
                        return -1
                    self.cache.move_to_end(key)
                    return self.cache[key]

                def put(self, key: int, value: int) -> None:
                    if key in self.cache:
                        self.cache.move_to_end(key)
                    self.cache[key] = value
                    if len(self.cache) > self.capacity:
                        self.cache.popitem(last=False)
        """),
        "hints": [
            "Use collections.OrderedDict which maintains insertion order and supports move_to_end.",
            "On get: move the accessed key to the end (most recent). On put: add/update and move to end.",
            "When capacity is exceeded, pop the first item (least recently used) with popitem(last=False).",
        ],
        "difficulty": "medium",
        "time_limit_minutes": 20,
        "topics": ["data structures", "OrderedDict", "caching"],
    },
    {
        "id": "py_04",
        "title": "Merge Overlapping Intervals",
        "prompt": (
            "Write a function merge_intervals(intervals: list[list[int]]) -> list[list[int]] "
            "that merges all overlapping intervals.\n\n"
            "Example:\n"
            "  Input:  [[1,3],[2,6],[8,10],[15,18]]\n"
            "  Output: [[1,6],[8,10],[15,18]]"
        ),
        "test_code": textwrap.dedent("""\
            assert merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]], "Test 1 failed"
            assert merge_intervals([[1,4],[4,5]]) == [[1,5]], "Test 2 failed"
            assert merge_intervals([[1,4],[0,4]]) == [[0,4]], "Test 3 failed"
            assert merge_intervals([]) == [], "Test 4 failed"
            assert merge_intervals([[1,2]]) == [[1,2]], "Test 5 failed"

            print("All tests passed!")
        """),
        "sample_solution": textwrap.dedent("""\
            def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
                if not intervals:
                    return []
                intervals.sort(key=lambda x: x[0])
                merged = [intervals[0]]
                for start, end in intervals[1:]:
                    if start <= merged[-1][1]:
                        merged[-1][1] = max(merged[-1][1], end)
                    else:
                        merged.append([start, end])
                return merged
        """),
        "hints": [
            "Sort intervals by their start value first.",
            "Iterate through sorted intervals, merging with the last result if they overlap.",
            "Two intervals overlap when the current start is less than or equal to the previous end.",
        ],
        "difficulty": "medium",
        "time_limit_minutes": 20,
        "topics": ["sorting", "intervals", "greedy"],
    },
    {
        "id": "py_05",
        "title": "DataFrame: Fill Missing Dates",
        "prompt": (
            "Write a function fill_missing_dates(df: pd.DataFrame) -> pd.DataFrame that:\n"
            "1. Takes a DataFrame with columns ['date', 'value']\n"
            "2. Fills in any missing dates in the date range with value = 0\n"
            "3. Returns the complete DataFrame sorted by date\n\n"
            "Example: if input has dates [2024-01-01, 2024-01-03], output should also "
            "include 2024-01-02 with value 0."
        ),
        "test_code": textwrap.dedent("""\
            import pandas as pd

            df = pd.DataFrame({
                'date': pd.to_datetime(['2024-01-01', '2024-01-03', '2024-01-05']),
                'value': [10, 30, 50]
            })
            result = fill_missing_dates(df)
            assert len(result) == 5, f"Expected 5 rows, got {len(result)}"
            assert result[result['date'] == '2024-01-02']['value'].iloc[0] == 0, "Missing date not filled with 0"
            assert result[result['date'] == '2024-01-04']['value'].iloc[0] == 0, "Missing date not filled with 0"
            assert list(result['value']) == [10, 0, 30, 0, 50], f"Values wrong: {list(result['value'])}"

            print("All tests passed!")
        """),
        "sample_solution": textwrap.dedent("""\
            import pandas as pd

            def fill_missing_dates(df: pd.DataFrame) -> pd.DataFrame:
                full_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
                full_df = pd.DataFrame({'date': full_range})
                merged = full_df.merge(df, on='date', how='left')
                merged['value'] = merged['value'].fillna(0).astype(int)
                return merged.sort_values('date').reset_index(drop=True)
        """),
        "hints": [
            "Use pd.date_range to generate all dates between min and max.",
            "Create a full DataFrame and merge (left join) with the original.",
            "Fill NaN values with 0 using fillna.",
        ],
        "difficulty": "easy",
        "time_limit_minutes": 20,
        "topics": ["pandas", "date manipulation", "merge"],
    },
    {
        "id": "py_06",
        "title": "Implement a Rate Limiter",
        "prompt": (
            "Implement a RateLimiter class that allows at most N requests in a "
            "sliding window of T seconds.\n\n"
            "  class RateLimiter:\n"
            "      def __init__(self, max_requests: int, window_seconds: float): ...\n"
            "      def allow_request(self) -> bool: ...\n\n"
            "allow_request returns True if the request is allowed, False if rate limited."
        ),
        "test_code": textwrap.dedent("""\
            import time

            limiter = RateLimiter(3, 1.0)
            assert limiter.allow_request() == True, "Request 1 should be allowed"
            assert limiter.allow_request() == True, "Request 2 should be allowed"
            assert limiter.allow_request() == True, "Request 3 should be allowed"
            assert limiter.allow_request() == False, "Request 4 should be rejected"

            time.sleep(1.1)
            assert limiter.allow_request() == True, "After window, request should be allowed"

            print("All tests passed!")
        """),
        "sample_solution": textwrap.dedent("""\
            import time
            from collections import deque

            class RateLimiter:
                def __init__(self, max_requests: int, window_seconds: float):
                    self.max_requests = max_requests
                    self.window_seconds = window_seconds
                    self.requests: deque[float] = deque()

                def allow_request(self) -> bool:
                    now = time.time()
                    while self.requests and now - self.requests[0] > self.window_seconds:
                        self.requests.popleft()
                    if len(self.requests) < self.max_requests:
                        self.requests.append(now)
                        return True
                    return False
        """),
        "hints": [
            "Use a deque to store timestamps of recent requests.",
            "On each call, remove timestamps older than the window.",
            "Allow the request only if the deque length is below max_requests.",
        ],
        "difficulty": "medium",
        "time_limit_minutes": 20,
        "topics": ["sliding window", "deque", "rate limiting"],
    },
    {
        "id": "py_07",
        "title": "Detect Cycle in a Directed Graph",
        "prompt": (
            "Write a function has_cycle(graph: dict[str, list[str]]) -> bool that "
            "detects whether a directed graph (given as an adjacency list) contains "
            "a cycle.\n\n"
            "Example:\n"
            "  has_cycle({'A': ['B'], 'B': ['C'], 'C': ['A']})  -> True\n"
            "  has_cycle({'A': ['B'], 'B': ['C'], 'C': []})     -> False"
        ),
        "test_code": textwrap.dedent("""\
            assert has_cycle({'A': ['B'], 'B': ['C'], 'C': ['A']}) == True, "Test 1 failed"
            assert has_cycle({'A': ['B'], 'B': ['C'], 'C': []}) == False, "Test 2 failed"
            assert has_cycle({'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}) == False, "Test 3 failed"
            assert has_cycle({'A': ['A']}) == True, "Test 4 (self-loop) failed"
            assert has_cycle({}) == False, "Test 5 (empty) failed"

            print("All tests passed!")
        """),
        "sample_solution": textwrap.dedent("""\
            def has_cycle(graph: dict[str, list[str]]) -> bool:
                WHITE, GRAY, BLACK = 0, 1, 2
                color: dict[str, int] = {node: WHITE for node in graph}

                def dfs(node: str) -> bool:
                    color[node] = GRAY
                    for neighbor in graph.get(node, []):
                        if color.get(neighbor) == GRAY:
                            return True
                        if color.get(neighbor) == WHITE and dfs(neighbor):
                            return True
                    color[node] = BLACK
                    return False

                for node in graph:
                    if color[node] == WHITE:
                        if dfs(node):
                            return True
                return False
        """),
        "hints": [
            "Use DFS with three states: unvisited, in-progress (on the current path), and done.",
            "A cycle exists if you encounter an in-progress node during DFS.",
            "Make sure to start DFS from every unvisited node to handle disconnected components.",
        ],
        "difficulty": "medium",
        "time_limit_minutes": 20,
        "topics": ["graphs", "DFS", "cycle detection"],
    },
    {
        "id": "py_08",
        "title": "DataFrame: Rolling Average with Grouping",
        "prompt": (
            "Write a function rolling_avg_by_group(df: pd.DataFrame, window: int) -> pd.DataFrame "
            "that adds a column 'rolling_avg' containing the rolling average of 'value' "
            "within each 'group', over the specified window size. Use min_periods=1.\n\n"
            "Input columns: ['date', 'group', 'value']\n"
            "Output: same DataFrame with an extra 'rolling_avg' column."
        ),
        "test_code": textwrap.dedent("""\
            import pandas as pd

            df = pd.DataFrame({
                'date': pd.to_datetime(['2024-01-01','2024-01-02','2024-01-03',
                                         '2024-01-01','2024-01-02','2024-01-03']),
                'group': ['A','A','A','B','B','B'],
                'value': [10, 20, 30, 100, 200, 300]
            })
            result = rolling_avg_by_group(df, 2)
            assert 'rolling_avg' in result.columns, "Missing rolling_avg column"
            a_vals = result[result['group'] == 'A']['rolling_avg'].tolist()
            assert a_vals == [10.0, 15.0, 25.0], f"Group A wrong: {a_vals}"
            b_vals = result[result['group'] == 'B']['rolling_avg'].tolist()
            assert b_vals == [100.0, 150.0, 250.0], f"Group B wrong: {b_vals}"

            print("All tests passed!")
        """),
        "sample_solution": textwrap.dedent("""\
            import pandas as pd

            def rolling_avg_by_group(df: pd.DataFrame, window: int) -> pd.DataFrame:
                df = df.sort_values(['group', 'date']).reset_index(drop=True)
                df['rolling_avg'] = df.groupby('group')['value'].transform(
                    lambda x: x.rolling(window, min_periods=1).mean()
                )
                return df
        """),
        "hints": [
            "Sort by group and date first, then use groupby + transform.",
            "Inside transform, apply rolling(window, min_periods=1).mean().",
            "transform keeps the same index as the original DataFrame.",
        ],
        "difficulty": "medium",
        "time_limit_minutes": 20,
        "topics": ["pandas", "groupby", "rolling window"],
    },
    {
        "id": "py_09",
        "title": "Implement a Trie (Prefix Tree)",
        "prompt": (
            "Implement a Trie class with the following methods:\n\n"
            "  class Trie:\n"
            "      def __init__(self): ...\n"
            "      def insert(self, word: str) -> None: ...\n"
            "      def search(self, word: str) -> bool: ...\n"
            "      def starts_with(self, prefix: str) -> bool: ...\n"
        ),
        "test_code": textwrap.dedent("""\
            trie = Trie()
            trie.insert("apple")
            assert trie.search("apple") == True, "Test 1 failed"
            assert trie.search("app") == False, "Test 2 failed"
            assert trie.starts_with("app") == True, "Test 3 failed"
            trie.insert("app")
            assert trie.search("app") == True, "Test 4 failed"
            assert trie.starts_with("xyz") == False, "Test 5 failed"
            assert trie.search("") == False, "Test 6 failed"

            print("All tests passed!")
        """),
        "sample_solution": textwrap.dedent("""\
            class TrieNode:
                def __init__(self):
                    self.children: dict[str, 'TrieNode'] = {}
                    self.is_end: bool = False

            class Trie:
                def __init__(self):
                    self.root = TrieNode()

                def insert(self, word: str) -> None:
                    node = self.root
                    for ch in word:
                        if ch not in node.children:
                            node.children[ch] = TrieNode()
                        node = node.children[ch]
                    node.is_end = True

                def search(self, word: str) -> bool:
                    node = self._find_node(word)
                    return node is not None and node.is_end

                def starts_with(self, prefix: str) -> bool:
                    return self._find_node(prefix) is not None

                def _find_node(self, prefix: str):
                    node = self.root
                    for ch in prefix:
                        if ch not in node.children:
                            return None
                        node = node.children[ch]
                    return node
        """),
        "hints": [
            "Each node has a dict mapping characters to child nodes, and a boolean is_end flag.",
            "insert walks/creates nodes for each character and marks the last as is_end=True.",
            "search and starts_with both traverse the trie; search also checks is_end at the final node.",
        ],
        "difficulty": "medium",
        "time_limit_minutes": 20,
        "topics": ["trie", "data structures", "string matching"],
    },
    {
        "id": "py_10",
        "title": "Chunked File Reader Generator",
        "prompt": (
            "Write a generator function read_in_chunks(filepath: str, chunk_size: int = 1024) "
            "that reads a file in chunks of chunk_size bytes and yields each chunk as bytes. "
            "Also write a function count_lines_chunked(filepath: str) -> int that uses "
            "read_in_chunks to count the total number of lines in a file without loading "
            "the entire file into memory."
        ),
        "test_code": textwrap.dedent("""\
            import tempfile, os

            content = "line1\\nline2\\nline3\\nline4\\nline5\\n"
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(content)
                tmp_path = f.name

            try:
                chunks = list(read_in_chunks(tmp_path, chunk_size=10))
                assert len(chunks) > 1, f"Expected multiple chunks, got {len(chunks)}"
                assert b''.join(chunks) == content.encode('utf-8'), "Chunks do not reassemble correctly"

                line_count = count_lines_chunked(tmp_path)
                assert line_count == 5, f"Expected 5 lines, got {line_count}"
            finally:
                os.unlink(tmp_path)

            print("All tests passed!")
        """),
        "sample_solution": textwrap.dedent("""\
            from typing import Generator

            def read_in_chunks(filepath: str, chunk_size: int = 1024) -> Generator[bytes, None, None]:
                with open(filepath, 'rb') as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        yield chunk

            def count_lines_chunked(filepath: str) -> int:
                count = 0
                for chunk in read_in_chunks(filepath):
                    count += chunk.count(b'\\n')
                return count
        """),
        "hints": [
            "Open the file in binary mode ('rb') and read chunk_size bytes in a loop.",
            "yield each chunk; stop when read returns empty bytes.",
            "For line counting, count occurrences of b'\\n' in each chunk and sum them.",
        ],
        "difficulty": "easy",
        "time_limit_minutes": 20,
        "topics": ["generators", "file I/O", "memory efficiency"],
    },
    {
        "id": "py_11",
        "title": "Data Pipeline: Extract-Transform-Load",
        "prompt": (
            "Write three functions forming a mini ETL pipeline:\n\n"
            "1. extract(data: list[dict]) -> list[dict]  -- filters out records where 'status' != 'active'\n"
            "2. transform(data: list[dict]) -> list[dict] -- adds a 'full_name' field by joining 'first_name' and 'last_name', and uppercases 'email'\n"
            "3. load(data: list[dict]) -> dict  -- returns a summary dict with 'total_records' (int) and 'emails' (sorted list of emails)\n\n"
            "Also write run_pipeline(raw_data: list[dict]) -> dict that chains all three steps."
        ),
        "test_code": textwrap.dedent("""\
            raw = [
                {'first_name': 'Alice', 'last_name': 'Smith', 'email': 'alice@test.com', 'status': 'active'},
                {'first_name': 'Bob', 'last_name': 'Jones', 'email': 'bob@test.com', 'status': 'inactive'},
                {'first_name': 'Carol', 'last_name': 'White', 'email': 'carol@test.com', 'status': 'active'},
            ]

            extracted = extract(raw)
            assert len(extracted) == 2, f"Extract: expected 2, got {len(extracted)}"

            transformed = transform(extracted)
            assert transformed[0]['full_name'] == 'Alice Smith', f"Transform name failed: {transformed[0]}"
            assert transformed[0]['email'] == 'ALICE@TEST.COM', f"Transform email failed: {transformed[0]}"

            result = run_pipeline(raw)
            assert result['total_records'] == 2, f"Pipeline total wrong: {result}"
            assert result['emails'] == ['ALICE@TEST.COM', 'CAROL@TEST.COM'], f"Pipeline emails wrong: {result}"

            print("All tests passed!")
        """),
        "sample_solution": textwrap.dedent("""\
            def extract(data: list[dict]) -> list[dict]:
                return [rec for rec in data if rec.get('status') == 'active']

            def transform(data: list[dict]) -> list[dict]:
                result = []
                for rec in data:
                    new_rec = dict(rec)
                    new_rec['full_name'] = f"{rec['first_name']} {rec['last_name']}"
                    new_rec['email'] = rec['email'].upper()
                    result.append(new_rec)
                return result

            def load(data: list[dict]) -> dict:
                return {
                    'total_records': len(data),
                    'emails': sorted(rec['email'] for rec in data),
                }

            def run_pipeline(raw_data: list[dict]) -> dict:
                return load(transform(extract(raw_data)))
        """),
        "hints": [
            "extract is a simple list comprehension filtering on status.",
            "transform creates new dicts with the added/modified fields; do not mutate originals.",
            "run_pipeline chains: load(transform(extract(raw_data))).",
        ],
        "difficulty": "easy",
        "time_limit_minutes": 20,
        "topics": ["ETL", "data pipeline", "list comprehension"],
    },
]

SYSTEM_DESIGN_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": "sd_01",
        "title": "Real-Time Analytics Data Pipeline",
        "prompt": (
            "Design a real-time analytics pipeline that ingests clickstream data "
            "from a web application (10,000 events/second), processes it, and "
            "serves dashboards with sub-second latency.\n\n"
            "Discuss:\n"
            "  - Data ingestion layer\n"
            "  - Stream processing\n"
            "  - Storage choices\n"
            "  - Serving layer\n"
            "  - How you would handle late-arriving data"
        ),
        "key_points": [
            "Kafka or similar for ingestion and buffering",
            "Flink/Spark Streaming for processing",
            "Hot storage (Redis/Druid) for real-time, cold storage (S3/HDFS) for batch",
            "Materialized views or pre-aggregations for dashboards",
            "Watermarks and late-data policies for out-of-order events",
        ],
        "hints": [
            "Start with the ingestion: think about a durable, distributed message queue.",
            "For processing, compare micro-batch (Spark Streaming) vs true streaming (Flink).",
            "Address the tradeoff between freshness and correctness for late data.",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "sd_02",
        "title": "ETL Pipeline for a Data Warehouse",
        "prompt": (
            "Design an ETL pipeline that extracts data from three sources (a "
            "PostgreSQL OLTP database, a third-party REST API, and CSV files "
            "uploaded to cloud storage), transforms it into a star schema, "
            "and loads it into a data warehouse on a daily schedule.\n\n"
            "Discuss:\n"
            "  - Orchestration tool\n"
            "  - Extraction strategies for each source\n"
            "  - Transformation approach (ELT vs ETL)\n"
            "  - Data quality checks\n"
            "  - Failure handling and retries"
        ),
        "key_points": [
            "Airflow or similar orchestrator for scheduling and dependency management",
            "CDC or timestamp-based incremental extraction from PostgreSQL",
            "Pagination and rate-limiting for API extraction",
            "dbt or SQL-based transformations in the warehouse (ELT pattern)",
            "Great Expectations or custom checks for data quality",
            "Idempotent tasks, retries with exponential backoff, alerting on failure",
        ],
        "hints": [
            "Think about orchestration first: what tool will manage dependencies and scheduling?",
            "For each source, the extraction strategy is different; describe each one.",
            "Address idempotency: what happens if a task runs twice?",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "sd_03",
        "title": "Data Lake Architecture",
        "prompt": (
            "Design a data lake architecture for a mid-size company that needs to "
            "store raw data from multiple sources, enable data scientists to run "
            "ad-hoc queries, and feed curated datasets to a BI tool.\n\n"
            "Discuss:\n"
            "  - Storage layers (raw, curated, consumption)\n"
            "  - File formats and partitioning\n"
            "  - Catalog and schema management\n"
            "  - Access control\n"
            "  - Cost optimization"
        ),
        "key_points": [
            "Multi-layer architecture: bronze (raw), silver (cleaned), gold (aggregated)",
            "Parquet or Delta Lake for columnar, compressed storage",
            "Partition by date and high-cardinality columns",
            "Glue Data Catalog or Hive Metastore for schema management",
            "IAM roles and column-level security",
            "Lifecycle policies to move old data to cheaper tiers",
        ],
        "hints": [
            "Organize the lake into layers: raw landing, cleaned, and business-ready.",
            "Choose a columnar format like Parquet for analytics workloads.",
            "Think about how users discover and understand the data (catalog, documentation).",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "sd_04",
        "title": "Change Data Capture System",
        "prompt": (
            "Design a change data capture (CDC) system that tracks all inserts, "
            "updates, and deletes in a PostgreSQL production database and replicates "
            "them to a downstream analytics database with minimal latency.\n\n"
            "Discuss:\n"
            "  - CDC approach (log-based vs trigger-based vs polling)\n"
            "  - Technology choices\n"
            "  - Schema evolution handling\n"
            "  - Exactly-once delivery guarantees\n"
            "  - Monitoring and alerting"
        ),
        "key_points": [
            "Log-based CDC with Debezium reading PostgreSQL WAL",
            "Kafka as the transport layer for durability and decoupling",
            "Schema Registry for evolution and compatibility checks",
            "Kafka Connect with exactly-once semantics configuration",
            "Monitoring replication lag, connector health, and schema changes",
        ],
        "hints": [
            "Log-based CDC (reading the WAL) is the least intrusive approach.",
            "Debezium is the standard open-source tool for this; describe how it works.",
            "Address what happens when the source schema changes (column added/removed).",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "sd_05",
        "title": "Batch vs Stream Processing Tradeoffs",
        "prompt": (
            "A company currently runs nightly batch jobs to compute aggregate metrics "
            "from transactional data. The business now wants some metrics available "
            "within 5 minutes. Design a hybrid architecture that supports both batch "
            "and near-real-time processing.\n\n"
            "Discuss:\n"
            "  - Lambda vs Kappa architecture\n"
            "  - Which metrics stay batch vs go real-time\n"
            "  - Consistency between batch and stream results\n"
            "  - Technology stack\n"
            "  - Migration strategy"
        ),
        "key_points": [
            "Lambda: separate batch and speed layers with a serving layer merging results",
            "Kappa: single stream processing layer (simpler but harder for complex aggregations)",
            "Prioritize real-time for high-value, low-complexity metrics first",
            "Use the batch layer as the source of truth to reconcile stream approximations",
            "Incremental migration: move one metric at a time to streaming",
        ],
        "hints": [
            "Start by explaining Lambda and Kappa architectures at a high level.",
            "Discuss criteria for deciding which metrics to move to real-time.",
            "Address the consistency challenge: stream results may differ from batch.",
        ],
        "time_limit_minutes": 5,
    },
    {
        "id": "sd_06",
        "title": "Data Quality Monitoring Platform",
        "prompt": (
            "Design a data quality monitoring platform that continuously checks "
            "incoming data for anomalies, schema violations, and freshness issues "
            "across 200+ tables in a data warehouse.\n\n"
            "Discuss:\n"
            "  - Types of quality checks\n"
            "  - Scheduling and integration with pipelines\n"
            "  - Alerting and notification\n"
            "  - Dashboard and reporting\n"
            "  - How to avoid alert fatigue"
        ),
        "key_points": [
            "Check categories: completeness, accuracy, consistency, timeliness, uniqueness",
            "Run checks as post-load steps in the pipeline (Airflow sensors or dbt tests)",
            "Tiered alerting: critical issues page on-call, warnings go to Slack",
            "Lineage-aware: if upstream fails, do not fire alerts for all downstream tables",
            "SLA-based freshness checks with configurable thresholds per table",
        ],
        "hints": [
            "Categorize checks: schema, completeness, freshness, statistical anomalies.",
            "Integrate checks into the pipeline so they block bad data from propagating.",
            "Think about reducing noise: group related alerts, use severity levels.",
        ],
        "time_limit_minutes": 5,
    },
]


# ---------------------------------------------------------------------------
# Helper: question type metadata
# ---------------------------------------------------------------------------
QUESTION_TYPES: dict[str, dict[str, Any]] = {
    "behavioral": {
        "label": "Behavioral",
        "bank": BEHAVIORAL_QUESTIONS,
        "color": "cyan",
        "default_time": 5,
        "auto_eval": False,
    },
    "sql": {
        "label": "SQL",
        "bank": SQL_QUESTIONS,
        "color": "green",
        "default_time": 15,
        "auto_eval": True,
    },
    "python": {
        "label": "Python",
        "bank": PYTHON_QUESTIONS,
        "color": "yellow",
        "default_time": 20,
        "auto_eval": True,
    },
    "system_design": {
        "label": "System Design",
        "bank": SYSTEM_DESIGN_QUESTIONS,
        "color": "magenta",
        "default_time": 5,
        "auto_eval": False,
    },
}


# ---------------------------------------------------------------------------
# Timer helpers
# ---------------------------------------------------------------------------

class QuestionTimer:
    """Tracks elapsed time for a question and provides warnings."""

    def __init__(self, time_limit_seconds: int) -> None:
        self.time_limit = time_limit_seconds
        self.start_time: float = 0.0
        self.warned_50 = False
        self.warned_75 = False
        self._running = False

    def start(self) -> None:
        """Start the timer."""
        self.start_time = time.time()
        self._running = True

    def elapsed(self) -> float:
        """Return elapsed seconds."""
        if not self._running:
            return 0.0
        return time.time() - self.start_time

    def remaining(self) -> float:
        """Return remaining seconds (can be negative if over time)."""
        return self.time_limit - self.elapsed()

    def stop(self) -> float:
        """Stop and return elapsed seconds."""
        self._running = False
        return self.elapsed()

    def check_warnings(self) -> str | None:
        """Check if a warning threshold has been crossed. Returns warning text or None."""
        pct = self.elapsed() / self.time_limit if self.time_limit > 0 else 0
        if pct >= 0.75 and not self.warned_75:
            self.warned_75 = True
            return "75% of time used -- consider wrapping up soon!"
        if pct >= 0.50 and not self.warned_50:
            self.warned_50 = True
            return "50% of time used -- halfway point."
        return None

    def format_remaining(self) -> str:
        """Return a human-readable string for remaining time."""
        rem = self.remaining()
        if rem <= 0:
            return "TIME IS UP"
        minutes = int(rem // 60)
        seconds = int(rem % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def format_elapsed(self) -> str:
        """Return a human-readable string for elapsed time."""
        el = self.elapsed()
        minutes = int(el // 60)
        seconds = int(el % 60)
        return f"{minutes:02d}:{seconds:02d}"


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

class InterviewSession:
    """Holds all state for one mock interview session."""

    def __init__(self, duration_minutes: int = 45) -> None:
        self.session_id: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.duration_minutes: int = duration_minutes
        self.start_time: datetime = datetime.now()
        self.end_time: datetime | None = None
        self.questions_attempted: list[dict[str, Any]] = []
        self.total_score: float = 0.0
        self.total_possible: float = 0.0
        self.session_timer = QuestionTimer(duration_minutes * 60)

    def add_result(self, result: dict[str, Any]) -> None:
        """Record the result of one question attempt."""
        self.questions_attempted.append(result)
        self.total_score += result.get("score", 0)
        self.total_possible += result.get("max_score", 10)

    def finalize(self) -> dict[str, Any]:
        """Build the final session report dict."""
        self.end_time = datetime.now()
        elapsed = (self.end_time - self.start_time).total_seconds()
        return {
            "session_id": self.session_id,
            "date": self.start_time.isoformat(),
            "duration_planned_minutes": self.duration_minutes,
            "duration_actual_seconds": round(elapsed, 1),
            "questions_attempted": len(self.questions_attempted),
            "total_score": round(self.total_score, 1),
            "total_possible": round(self.total_possible, 1),
            "score_pct": round(
                (self.total_score / self.total_possible * 100) if self.total_possible > 0 else 0, 1
            ),
            "details": self.questions_attempted,
        }


# ---------------------------------------------------------------------------
# Code evaluation
# ---------------------------------------------------------------------------

def evaluate_python_code(user_code: str, test_code: str) -> tuple[bool, str]:
    """Run user Python code against test cases in a subprocess.

    Returns:
        Tuple of (passed: bool, output: str).
    """
    full_code = user_code + "\n\n" + test_code
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(full_code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
        )
        output = result.stdout + result.stderr
        passed = result.returncode == 0 and "All tests passed" in result.stdout
        return passed, output.strip()
    except subprocess.TimeoutExpired:
        return False, "Execution timed out after 30 seconds."
    except Exception as exc:
        return False, f"Execution error: {exc}"
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def evaluate_sql_keywords(user_sql: str, expected_keywords: list[str]) -> tuple[float, list[str]]:
    """Check which expected SQL keywords appear in the user's answer.

    Returns:
        Tuple of (score fraction 0-1, list of missing keywords).
    """
    upper_sql = user_sql.upper()
    missing: list[str] = []
    for kw in expected_keywords:
        if kw.upper() not in upper_sql:
            missing.append(kw)
    if not expected_keywords:
        return 1.0, []
    score = (len(expected_keywords) - len(missing)) / len(expected_keywords)
    return score, missing


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def show_welcome_banner() -> None:
    """Display the welcome banner."""
    banner_text = Text()
    banner_text.append("Technical Mock Interview Simulator\n", style="bold white")
    banner_text.append("Data Engineering @ tasq.ai\n", style="dim white")
    banner_text.append("Prepare. Practice. Perform.", style="italic dim white")
    console.print(Panel(
        Align.center(banner_text),
        border_style="bright_blue",
        box=box.DOUBLE,
        padding=(1, 4),
    ))
    console.print()


def show_question_panel(
    question: dict[str, Any],
    q_type: str,
    question_num: int,
    total_questions: int,
) -> None:
    """Display a question inside a styled panel."""
    meta = QUESTION_TYPES[q_type]
    title = (
        f"[{meta['color']}][{meta['label']}][/{meta['color']}] "
        f"Question {question_num}/{total_questions}: {question['title']}"
    )
    body = question["prompt"]
    if q_type == "system_design" and "key_points" in question:
        body += "\n\n[dim]Key areas to cover are listed above in the prompt.[/dim]"
    console.print(Panel(body, title=title, border_style=meta["color"], padding=(1, 2)))


def show_timer_status(timer: QuestionTimer, session_timer: QuestionTimer) -> None:
    """Print a compact timer status line."""
    q_remaining = timer.format_remaining()
    s_remaining = session_timer.format_remaining()
    console.print(
        f"  [dim]Question time remaining:[/dim] [bold]{q_remaining}[/bold]"
        f"  |  [dim]Session remaining:[/dim] [bold]{s_remaining}[/bold]"
    )


def show_hint(hint_text: str, hint_num: int, max_hints: int) -> None:
    """Display a hint panel."""
    console.print(Panel(
        hint_text,
        title=f"Hint {hint_num}/{max_hints}",
        border_style="yellow",
        padding=(0, 2),
    ))


def show_evaluation_result(passed: bool, output: str, score: float, max_score: float) -> None:
    """Display code evaluation results."""
    status = "[bold green]PASSED[/bold green]" if passed else "[bold red]FAILED[/bold red]"
    console.print(f"\n  Evaluation: {status}  ({score}/{max_score} points)")
    if output:
        console.print(Panel(output, title="Output", border_style="dim", padding=(0, 1)))


def show_sample_solution(question: dict[str, Any]) -> None:
    """Display the sample solution for a question."""
    sol = question.get("sample_solution", question.get("key_points"))
    if isinstance(sol, list):
        text = "\n".join(f"  - {pt}" for pt in sol)
    else:
        text = str(sol)
    console.print(Panel(text, title="Sample Solution", border_style="green", padding=(0, 2)))


def build_summary_table(session: InterviewSession) -> Table:
    """Build a Rich table summarizing all question results."""
    table = Table(
        title="Session Results",
        box=box.ROUNDED,
        show_lines=True,
        title_style="bold white",
    )
    table.add_column("#", style="dim", width=4, justify="center")
    table.add_column("Type", width=12)
    table.add_column("Title", min_width=20)
    table.add_column("Time", width=8, justify="center")
    table.add_column("Hints", width=6, justify="center")
    table.add_column("Score", width=10, justify="center")

    for i, q in enumerate(session.questions_attempted, 1):
        q_type = q.get("type", "unknown")
        color = QUESTION_TYPES.get(q_type, {}).get("color", "white")
        score_str = f"{q['score']}/{q['max_score']}"
        table.add_row(
            str(i),
            f"[{color}]{q_type}[/{color}]",
            q.get("title", "N/A"),
            q.get("time_taken", "N/A"),
            str(q.get("hints_used", 0)),
            score_str,
        )

    return table


def show_final_report(session: InterviewSession) -> None:
    """Display the final interview report."""
    report = session.finalize()
    console.print()
    console.print(Rule("Interview Complete", style="bright_blue"))
    console.print()

    # Summary stats
    stats_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    stats_table.add_column("Metric", style="bold")
    stats_table.add_column("Value")
    stats_table.add_row("Session ID", report["session_id"])
    stats_table.add_row("Date", report["date"][:10])
    actual_min = report["duration_actual_seconds"] / 60
    stats_table.add_row("Duration", f"{actual_min:.1f} min (planned {report['duration_planned_minutes']} min)")
    stats_table.add_row("Questions Attempted", str(report["questions_attempted"]))
    stats_table.add_row("Total Score", f"{report['total_score']}/{report['total_possible']}")
    stats_table.add_row("Percentage", f"{report['score_pct']}%")
    console.print(Panel(stats_table, title="Summary", border_style="bright_blue"))

    # Per-question table
    console.print()
    console.print(build_summary_table(session))

    # Score interpretation
    pct = report["score_pct"]
    if pct >= 80:
        verdict = "Excellent performance! You are well prepared."
    elif pct >= 60:
        verdict = "Good effort. Review the questions you missed and practice more."
    elif pct >= 40:
        verdict = "Fair performance. Focus on your weak areas and try again."
    else:
        verdict = "Needs significant improvement. Study the solutions and fundamentals."

    console.print()
    console.print(Panel(verdict, title="Assessment", border_style="bright_blue", padding=(0, 2)))

    return report


def save_session_report(report: dict[str, Any]) -> Path:
    """Save the session report to a JSON file."""
    filename = f"session_{report['session_id']}.json"
    filepath = SESSIONS_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    logger.info("Session report saved to %s", filepath)
    return filepath


# ---------------------------------------------------------------------------
# Interview flow
# ---------------------------------------------------------------------------

def collect_multiline_input(prompt_text: str = "Your answer") -> str:
    """Collect multi-line input from the user.

    Type your answer and press Enter twice (empty line) to submit.
    Type 'hint' on its own line to request a hint.
    Type 'skip' on its own line to skip the question.
    Type 'solution' on its own line to see the sample solution.
    """
    console.print(f"  [dim]{prompt_text} (Enter twice to submit, 'hint'/'skip'/'solution' as commands):[/dim]")
    lines: list[str] = []
    while True:
        try:
            line = input("  > ")
        except EOFError:
            break
        if line.strip().lower() in ("hint", "skip", "solution"):
            return f"__{line.strip().lower()}__"
        if line == "" and lines and lines[-1] == "":
            # Two consecutive empty lines -> submit
            lines.pop()  # remove the trailing empty line
            break
        lines.append(line)
    return "\n".join(lines)


def run_question(
    question: dict[str, Any],
    q_type: str,
    question_num: int,
    total_questions: int,
    session: InterviewSession,
) -> dict[str, Any]:
    """Run a single interview question and return the result dict."""
    meta = QUESTION_TYPES[q_type]
    max_score = 10.0
    hints_used = 0
    max_hints = 3
    hint_list = question.get("hints", [])

    time_limit_sec = question.get("time_limit_minutes", meta["default_time"]) * 60
    timer = QuestionTimer(time_limit_sec)

    console.print()
    show_question_panel(question, q_type, question_num, total_questions)
    show_timer_status(timer, session.session_timer)
    console.print()

    timer.start()
    user_answer = ""
    skipped = False
    showed_solution = False

    while True:
        raw = collect_multiline_input()

        # Check timer warnings
        warning = timer.check_warnings()
        if warning:
            console.print(f"  [bold yellow]{warning}[/bold yellow]")
            show_timer_status(timer, session.session_timer)

        if raw == "__hint__":
            if hints_used < max_hints and hints_used < len(hint_list):
                hints_used += 1
                show_hint(hint_list[hints_used - 1], hints_used, max_hints)
            elif hints_used >= max_hints:
                console.print("  [dim]No more hints available (max 3).[/dim]")
            else:
                console.print("  [dim]No hints available for this question.[/dim]")
            continue

        if raw == "__skip__":
            skipped = True
            console.print("  [dim]Question skipped.[/dim]")
            break

        if raw == "__solution__":
            showed_solution = True
            show_sample_solution(question)
            console.print("  [dim]You viewed the solution. No score for this question.[/dim]")
            break

        if raw.strip():
            user_answer = raw
            break
        else:
            console.print("  [dim]Empty answer. Type 'skip' to skip or enter your answer.[/dim]")

    elapsed = timer.stop()
    elapsed_str = timer.format_elapsed()

    # Evaluate
    score = 0.0
    eval_output = ""

    if skipped or showed_solution:
        score = 0.0
        eval_output = "Skipped or solution viewed."
    elif q_type == "python" and meta["auto_eval"]:
        test_code = question.get("test_code", "")
        if test_code:
            passed, output = evaluate_python_code(user_answer, test_code)
            eval_output = output
            if passed:
                score = max_score - (hints_used * 1.5)
                score = max(score, 1.0)
            else:
                score = max(2.0 - hints_used * 0.5, 0.0)
            show_evaluation_result(passed, output, score, max_score)
        else:
            score = 5.0
            eval_output = "No auto-evaluation available."
    elif q_type == "sql" and meta["auto_eval"]:
        expected_kw = question.get("expected_keywords", [])
        kw_score, missing = evaluate_sql_keywords(user_answer, expected_kw)
        score = round(kw_score * max_score - (hints_used * 1.0), 1)
        score = max(score, 0.0)
        if missing:
            eval_output = f"Missing expected keywords: {', '.join(missing)}"
            console.print(f"  [yellow]Missing keywords:[/yellow] {', '.join(missing)}")
        else:
            eval_output = "All expected keywords found."
            console.print("  [green]All expected SQL keywords found.[/green]")
        console.print(f"  Score: {score}/{max_score}")
    else:
        # Behavioral / system design -- self-assessment
        console.print()
        console.print("  [dim]Rate your own answer (1-10):[/dim]")
        try:
            self_score = IntPrompt.ask("  Self-score", default=5, console=console)
            self_score = max(1, min(10, self_score))
        except (KeyboardInterrupt, EOFError):
            self_score = 5
        score = float(self_score) - (hints_used * 1.0)
        score = max(score, 0.0)
        eval_output = f"Self-assessed: {self_score}/10"

    # Offer to view sample solution after answering
    if not showed_solution and not skipped:
        try:
            show_sol = Confirm.ask("  View sample solution?", default=False, console=console)
            if show_sol:
                show_sample_solution(question)
        except (KeyboardInterrupt, EOFError):
            pass

    result: dict[str, Any] = {
        "id": question["id"],
        "type": q_type,
        "title": question["title"],
        "time_taken": elapsed_str,
        "time_seconds": round(elapsed, 1),
        "hints_used": hints_used,
        "skipped": skipped,
        "solution_viewed": showed_solution,
        "score": round(score, 1),
        "max_score": max_score,
        "evaluation": eval_output,
        "user_answer_preview": user_answer[:500] if user_answer else "",
    }

    session.add_result(result)
    return result


def select_questions(
    question_types: list[str],
    count_per_type: dict[str, int],
) -> list[tuple[str, dict[str, Any]]]:
    """Randomly select questions from the banks.

    Returns:
        List of (question_type, question_dict) tuples.
    """
    selected: list[tuple[str, dict[str, Any]]] = []
    for qt in question_types:
        bank = QUESTION_TYPES[qt]["bank"]
        n = min(count_per_type.get(qt, 1), len(bank))
        chosen = random.sample(bank, n)
        for q in chosen:
            selected.append((qt, q))
    random.shuffle(selected)
    return selected


def configure_session() -> tuple[int, list[tuple[str, dict[str, Any]]]]:
    """Interactive session configuration. Returns duration and selected questions."""
    console.print(Panel(
        "Configure your mock interview session.\n"
        "You can adjust the duration and the mix of question types.",
        title="Session Setup",
        border_style="bright_blue",
        padding=(0, 2),
    ))
    console.print()

    try:
        duration = IntPrompt.ask(
            "  Session duration (minutes)",
            default=45,
            console=console,
        )
        duration = max(5, min(180, duration))
    except (KeyboardInterrupt, EOFError):
        duration = 45

    console.print()
    console.print("  Available question types:")
    for key, meta in QUESTION_TYPES.items():
        color = meta["color"]
        bank_size = len(meta["bank"])
        console.print(
            f"    [{color}]{meta['label']:15}[/{color}] "
            f"({bank_size} questions, ~{meta['default_time']} min each)"
        )
    console.print()

    count_per_type: dict[str, int] = {}
    types_to_include: list[str] = []

    for key, meta in QUESTION_TYPES.items():
        try:
            n = IntPrompt.ask(
                f"  How many {meta['label']} questions?",
                default=2,
                console=console,
            )
            n = max(0, min(n, len(meta["bank"])))
        except (KeyboardInterrupt, EOFError):
            n = 2
        if n > 0:
            count_per_type[key] = n
            types_to_include.append(key)

    if not types_to_include:
        console.print("  [dim]No questions selected. Using defaults (2 of each).[/dim]")
        types_to_include = list(QUESTION_TYPES.keys())
        count_per_type = {k: 2 for k in types_to_include}

    questions = select_questions(types_to_include, count_per_type)
    total_q = len(questions)
    console.print(f"\n  Selected {total_q} questions. Starting interview...\n")
    return duration, questions


def run_interview() -> None:
    """Main interview loop."""
    show_welcome_banner()

    try:
        duration, questions = configure_session()
    except KeyboardInterrupt:
        console.print("\n  [dim]Session cancelled.[/dim]")
        return

    session = InterviewSession(duration_minutes=duration)
    session.session_timer.start()

    total_q = len(questions)

    try:
        for i, (q_type, question) in enumerate(questions, 1):
            # Check if session time is up
            if session.session_timer.remaining() <= 0:
                console.print("\n  [bold red]Session time is up![/bold red]")
                break

            console.print(Rule(f"Question {i} of {total_q}", style="dim"))
            run_question(question, q_type, i, total_q, session)

            # Check session timer after each question
            warning = session.session_timer.check_warnings()
            if warning:
                console.print(f"\n  [bold yellow]Session: {warning}[/bold yellow]")

            if i < total_q:
                try:
                    cont = Confirm.ask(
                        "  Continue to next question?",
                        default=True,
                        console=console,
                    )
                    if not cont:
                        console.print("  [dim]Ending interview early.[/dim]")
                        break
                except (KeyboardInterrupt, EOFError):
                    console.print("\n  [dim]Ending interview.[/dim]")
                    break

    except KeyboardInterrupt:
        console.print("\n  [dim]Interview interrupted. Saving progress...[/dim]")

    # Final report
    report = show_final_report(session)
    filepath = save_session_report(report)
    console.print(f"\n  [dim]Report saved to:[/dim] {filepath}")
    console.print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point for the mock interview simulator."""
    logger.info("Starting Technical Mock Interview Simulator")
    try:
        run_interview()
    except KeyboardInterrupt:
        console.print("\n\n  [dim]Goodbye![/dim]")
        logger.info("Session ended by user interrupt")
    except Exception as exc:
        logger.exception("Unexpected error: %s", exc)
        console.print(f"\n  [bold red]Unexpected error:[/bold red] {exc}")
        sys.exit(1)
    finally:
        logger.info("Simulator exiting")


if __name__ == "__main__":
    main()
