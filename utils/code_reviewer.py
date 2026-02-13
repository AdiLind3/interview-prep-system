# -*- coding: utf-8 -*-
"""Automated code reviewer for SQL and Python solutions.

Provides regex-based static analysis for SQL queries and Python code,
checking for common issues, performance problems, and best practices.

Can be used as an importable module or as a CLI tool:
    python utils/code_reviewer.py <file_path>
"""
import re
import sys
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

# Add project root to path so we can import sibling modules
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from utils.logger import setup_logger

logger = setup_logger("code-reviewer", level=logging.DEBUG)
console = Console()


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Issue:
    """A single issue found during code review.

    Attributes:
        severity: One of 'error', 'warning', 'info'.
        category: Short label such as 'performance' or 'style'.
        line: The approximate line number (0 means whole-file).
        message: Human-readable description of the issue.
        suggestion: Optional suggestion for how to fix it.
    """
    severity: str
    category: str
    line: int
    message: str
    suggestion: str = ""


@dataclass
class ReviewResult:
    """Aggregated result of a code review.

    Attributes:
        file_path: Path to the reviewed file.
        language: 'sql' or 'python'.
        issues: List of issues found.
        complexity_score: Numeric complexity estimate.
        summary: Short one-line summary.
    """
    file_path: str
    language: str
    issues: list[Issue] = field(default_factory=list)
    complexity_score: int = 0
    summary: str = ""


# ---------------------------------------------------------------------------
# SQL Review
# ---------------------------------------------------------------------------

def review_sql(code: str, file_path: str = "<stdin>") -> ReviewResult:
    """Review a SQL query for performance issues, best practices, and common mistakes.

    Args:
        code: The SQL source code to review.
        file_path: Path to the file (used in reporting only).

    Returns:
        A ReviewResult containing all detected issues.
    """
    logger.info("Starting SQL review for %s", file_path)
    result = ReviewResult(file_path=file_path, language="sql")
    lines = code.splitlines()
    upper_code = code.upper()

    # -- Performance issues --------------------------------------------------

    # SELECT *
    for idx, line in enumerate(lines, start=1):
        if re.search(r"\bSELECT\s+\*", line, re.IGNORECASE):
            result.issues.append(Issue(
                severity="warning",
                category="performance",
                line=idx,
                message="SELECT * retrieves all columns, which can hurt performance.",
                suggestion="Explicitly list only the columns you need.",
            ))

    # Missing WHERE clause on SELECT (simple heuristic)
    select_blocks = list(re.finditer(
        r"\bSELECT\b.+?\bFROM\b\s+\w+",
        upper_code,
        re.DOTALL,
    ))
    for m in select_blocks:
        # Grab everything after the FROM table until the next major keyword or end
        rest_start = m.end()
        rest = upper_code[rest_start:rest_start + 500]
        # If there is no WHERE before the next SELECT / UNION / semicolon, flag it
        has_where = re.search(r"\bWHERE\b", rest)
        next_boundary = re.search(r"(\bSELECT\b|\bUNION\b|;)", rest)
        boundary_pos = next_boundary.start() if next_boundary else len(rest)
        if not has_where or (has_where and has_where.start() > boundary_pos):
            line_no = code[:m.start()].count("\n") + 1
            result.issues.append(Issue(
                severity="info",
                category="performance",
                line=line_no,
                message="SELECT without a WHERE clause may return more rows than intended.",
                suggestion="Add a WHERE clause to limit the result set if appropriate.",
            ))

    # Cartesian join (comma-separated tables without JOIN keyword)
    # Pattern: FROM a, b  (without JOIN between them)
    cartesian_pattern = re.compile(
        r"\bFROM\s+\w+\s*,\s*\w+", re.IGNORECASE
    )
    for m in cartesian_pattern.finditer(code):
        line_no = code[:m.start()].count("\n") + 1
        result.issues.append(Issue(
            severity="warning",
            category="performance",
            line=line_no,
            message="Comma-separated tables in FROM may produce a cartesian join.",
            suggestion="Use explicit JOIN syntax (INNER JOIN, LEFT JOIN, etc.).",
        ))

    # Functions on indexed columns in WHERE (e.g., WHERE UPPER(col) = ...)
    func_on_col = re.compile(
        r"\bWHERE\b.*?\b(UPPER|LOWER|TRIM|CAST|CONVERT|SUBSTR|SUBSTRING|COALESCE|IFNULL|NVL|DATE|YEAR|MONTH)\s*\(",
        re.IGNORECASE | re.DOTALL,
    )
    for m in func_on_col.finditer(code):
        line_no = code[:m.start()].count("\n") + 1
        func_name = m.group(1)
        result.issues.append(Issue(
            severity="warning",
            category="performance",
            line=line_no,
            message=f"Function {func_name.upper()}() on a column in WHERE may prevent index usage.",
            suggestion="Consider using a computed/virtual column or restructure the condition.",
        ))

    # -- Best practices ------------------------------------------------------

    # Implicit JOIN (old-style comma join with WHERE for join condition)
    if cartesian_pattern.search(code) and re.search(r"\bWHERE\b", code, re.IGNORECASE):
        result.issues.append(Issue(
            severity="info",
            category="best-practice",
            line=0,
            message="Old-style implicit JOIN syntax detected.",
            suggestion="Prefer explicit JOIN ... ON syntax for clarity.",
        ))

    # Inconsistent keyword casing
    keywords = ["SELECT", "FROM", "WHERE", "JOIN", "LEFT", "RIGHT", "INNER",
                "OUTER", "ON", "GROUP", "ORDER", "BY", "HAVING", "INSERT",
                "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "AND", "OR",
                "IN", "NOT", "NULL", "AS", "DISTINCT", "UNION", "LIMIT",
                "OFFSET", "CASE", "WHEN", "THEN", "ELSE", "END", "WITH",
                "BETWEEN", "LIKE", "EXISTS", "INTO", "VALUES", "SET"]
    upper_count = 0
    lower_count = 0
    for kw in keywords:
        upper_count += len(re.findall(r"\b" + kw + r"\b", code))
        lower_count += len(re.findall(r"\b" + kw.lower() + r"\b", code))
    if upper_count > 0 and lower_count > 0:
        total = upper_count + lower_count
        # Only flag when the mix is significant (not just one stray keyword)
        minority_pct = min(upper_count, lower_count) / total
        if minority_pct > 0.15:
            result.issues.append(Issue(
                severity="info",
                category="style",
                line=0,
                message="Inconsistent SQL keyword casing (mix of UPPER and lower).",
                suggestion="Pick one convention (UPPER is most common) and stick with it.",
            ))

    # Missing table alias on JOINs
    join_no_alias = re.compile(
        r"\bJOIN\s+(\w+)\s+ON\b", re.IGNORECASE
    )
    for m in join_no_alias.finditer(code):
        table_name = m.group(1)
        # Check if the table name is followed by an alias (word that is not ON)
        after_table = code[m.start():m.end()]
        if not re.search(r"\bJOIN\s+\w+\s+\w+\s+ON\b", after_table, re.IGNORECASE):
            line_no = code[:m.start()].count("\n") + 1
            result.issues.append(Issue(
                severity="info",
                category="best-practice",
                line=line_no,
                message=f"Table '{table_name}' in JOIN has no alias.",
                suggestion="Add a short alias (e.g., JOIN {0} AS {1}).".format(
                    table_name, table_name[:1].lower()
                ),
            ))

    # -- Complexity scoring --------------------------------------------------
    join_count = len(re.findall(r"\bJOIN\b", upper_code))
    subquery_count = max(0, upper_code.count("SELECT") - 1)
    window_count = len(re.findall(r"\bOVER\s*\(", upper_code))
    cte_count = len(re.findall(r"\bWITH\b\s+\w+\s+AS\s*\(", upper_code))
    union_count = len(re.findall(r"\bUNION\b", upper_code))
    case_count = len(re.findall(r"\bCASE\b", upper_code))

    complexity = (
        join_count * 2
        + subquery_count * 3
        + window_count * 2
        + cte_count * 1
        + union_count * 2
        + case_count * 1
    )
    result.complexity_score = complexity

    # -- Missing optimizations -----------------------------------------------

    # Suggest CTEs when there are subqueries
    if subquery_count >= 2 and cte_count == 0:
        result.issues.append(Issue(
            severity="info",
            category="optimization",
            line=0,
            message=f"Query has {subquery_count} subqueries and no CTEs.",
            suggestion="Consider using WITH (CTE) for readability and maintenance.",
        ))

    # Suggest window functions when self-join pattern is detected
    self_join = re.compile(
        r"\bFROM\s+(\w+)\s+\w+\s+.*?\bJOIN\s+\1\b", re.IGNORECASE | re.DOTALL
    )
    if self_join.search(code) and window_count == 0:
        result.issues.append(Issue(
            severity="info",
            category="optimization",
            line=0,
            message="Self-join detected; a window function might be simpler.",
            suggestion="ROW_NUMBER(), LAG(), LEAD(), or RANK() can often replace self-joins.",
        ))

    # -- Common mistakes -----------------------------------------------------

    # GROUP BY without aggregation function
    if re.search(r"\bGROUP\s+BY\b", upper_code):
        agg_funcs = re.findall(
            r"\b(COUNT|SUM|AVG|MIN|MAX|GROUP_CONCAT|STRING_AGG|ARRAY_AGG)\s*\(",
            upper_code,
        )
        if not agg_funcs:
            result.issues.append(Issue(
                severity="warning",
                category="correctness",
                line=0,
                message="GROUP BY found but no aggregation functions detected.",
                suggestion="Verify that you need GROUP BY, or add aggregate functions.",
            ))

    # Ambiguous column reference (same column name used without table qualifier
    # in a multi-table query) -- rough heuristic
    if join_count > 0:
        select_match = re.search(
            r"\bSELECT\b(.+?)\bFROM\b", code, re.IGNORECASE | re.DOTALL
        )
        if select_match:
            select_cols = select_match.group(1)
            bare_cols = re.findall(r"(?<![.\w])([a-zA-Z_]\w*)(?!\s*\()", select_cols)
            # Columns that have no dot-prefix (table.col) might be ambiguous
            qualified = re.findall(r"\w+\.\w+", select_cols)
            unqualified = [c for c in bare_cols if c.upper() not in keywords and c not in ("AS",)]
            if unqualified and not qualified:
                result.issues.append(Issue(
                    severity="info",
                    category="correctness",
                    line=0,
                    message="Multi-table query with unqualified column names in SELECT.",
                    suggestion="Prefix columns with table alias to avoid ambiguity (e.g., t.column).",
                ))

    # -- Summary -------------------------------------------------------------
    error_count = sum(1 for i in result.issues if i.severity == "error")
    warning_count = sum(1 for i in result.issues if i.severity == "warning")
    info_count = sum(1 for i in result.issues if i.severity == "info")
    result.summary = (
        f"SQL review: {error_count} errors, {warning_count} warnings, "
        f"{info_count} info -- complexity score {complexity}"
    )
    logger.info("SQL review complete: %s", result.summary)
    return result


# ---------------------------------------------------------------------------
# Python Review
# ---------------------------------------------------------------------------

def review_python(code: str, file_path: str = "<stdin>") -> ReviewResult:
    """Review Python code for PEP 8, code smells, performance, and anti-patterns.

    Args:
        code: The Python source code to review.
        file_path: Path to the file (used in reporting only).

    Returns:
        A ReviewResult containing all detected issues.
    """
    logger.info("Starting Python review for %s", file_path)
    result = ReviewResult(file_path=file_path, language="python")
    lines = code.splitlines()

    # -- PEP 8 compliance ----------------------------------------------------

    for idx, line in enumerate(lines, start=1):
        # Line length (PEP 8 recommends 79, many projects use 120)
        if len(line) > 120:
            result.issues.append(Issue(
                severity="info",
                category="style",
                line=idx,
                message=f"Line is {len(line)} characters long (exceeds 120).",
                suggestion="Break the line or refactor for readability.",
            ))

        # Trailing whitespace
        if line != line.rstrip():
            result.issues.append(Issue(
                severity="info",
                category="style",
                line=idx,
                message="Trailing whitespace detected.",
                suggestion="Remove trailing spaces.",
            ))

        # Tabs mixed with spaces (only for indentation)
        if line and line[0] in (" ", "\t"):
            indent = re.match(r"^[\t ]+", line)
            if indent and "\t" in indent.group() and " " in indent.group():
                result.issues.append(Issue(
                    severity="warning",
                    category="style",
                    line=idx,
                    message="Mixed tabs and spaces in indentation.",
                    suggestion="Use spaces only (PEP 8 standard is 4 spaces).",
                ))

    # Naming conventions
    # Top-level function names should be snake_case
    func_defs = re.finditer(r"^def\s+([a-zA-Z_]\w*)\s*\(", code, re.MULTILINE)
    for m in func_defs:
        name = m.group(1)
        if name.startswith("__"):
            continue  # dunder methods are fine
        if re.search(r"[A-Z]", name):
            line_no = code[:m.start()].count("\n") + 1
            result.issues.append(Issue(
                severity="info",
                category="style",
                line=line_no,
                message=f"Function '{name}' uses camelCase or PascalCase.",
                suggestion="PEP 8 recommends snake_case for function names.",
            ))

    # Class names should be PascalCase
    class_defs = re.finditer(r"^class\s+([a-zA-Z_]\w*)", code, re.MULTILINE)
    for m in class_defs:
        name = m.group(1)
        if not re.match(r"^[A-Z]", name):
            line_no = code[:m.start()].count("\n") + 1
            result.issues.append(Issue(
                severity="info",
                category="style",
                line=line_no,
                message=f"Class '{name}' does not start with an uppercase letter.",
                suggestion="PEP 8 recommends PascalCase for class names.",
            ))

    # -- Code smells ---------------------------------------------------------

    # Deeply nested code (3+ levels of indentation inside a function)
    max_indent = 0
    for idx, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        indent_level = (len(line) - len(stripped))
        # Assume 4-space indent
        nesting = indent_level // 4
        if nesting > max_indent:
            max_indent = nesting
        if nesting >= 5:
            result.issues.append(Issue(
                severity="warning",
                category="code-smell",
                line=idx,
                message=f"Deeply nested code (indent level {nesting}).",
                suggestion="Extract inner logic into helper functions or use early returns.",
            ))

    # God functions (functions longer than 50 lines)
    func_starts: list[tuple[int, str]] = []
    for idx, line in enumerate(lines):
        m = re.match(r"^(\s*)def\s+(\w+)\s*\(", line)
        if m:
            func_starts.append((idx, m.group(2)))
    for i, (start, name) in enumerate(func_starts):
        end = func_starts[i + 1][0] if i + 1 < len(func_starts) else len(lines)
        func_len = end - start
        if func_len > 50:
            result.issues.append(Issue(
                severity="warning",
                category="code-smell",
                line=start + 1,
                message=f"Function '{name}' is {func_len} lines long.",
                suggestion="Consider breaking it into smaller, focused functions.",
            ))

    # Magic numbers (numeric literals other than 0, 1, -1 outside of assignments
    # to UPPER_CASE constants)
    magic_pattern = re.compile(r"(?<!=\s)(?<!['\"\w.])\b(\d+\.?\d*)\b(?!['\"\w.])")
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("import"):
            continue
        # Skip constant assignments like MAX_SIZE = 100
        if re.match(r"^[A-Z_]+\s*=", stripped):
            continue
        # Skip lines that are just numeric returns or list indices
        for nm in magic_pattern.finditer(line):
            val = nm.group(1)
            if val in ("0", "1", "2", "0.0", "1.0", "100"):
                continue
            # Only flag if the number appears in logic, not in string formatting etc.
            context_before = line[:nm.start()].rstrip()
            if context_before.endswith(("'", '"', ":", "[", ",")):
                continue
            # Crude filter: flag numbers > 1 that appear in comparisons or arithmetic
            try:
                num_val = float(val)
            except ValueError:
                continue
            if num_val > 1 and ("if " in line or "while " in line or "return " in line
                                or " > " in line or " < " in line or " == " in line):
                result.issues.append(Issue(
                    severity="info",
                    category="code-smell",
                    line=idx,
                    message=f"Magic number {val} -- consider using a named constant.",
                    suggestion="Define a descriptively named constant at module level.",
                ))
                break  # one per line is enough

    # -- Performance issues --------------------------------------------------

    # Using a loop where pandas vectorized operations could work
    if "import pandas" in code or "from pandas" in code:
        for idx, line in enumerate(lines, start=1):
            if ".iterrows()" in line:
                result.issues.append(Issue(
                    severity="warning",
                    category="performance",
                    line=idx,
                    message="DataFrame.iterrows() is slow for large DataFrames.",
                    suggestion="Use vectorized operations, .apply(), or .itertuples() instead.",
                ))
            if ".iteritems()" in line:
                result.issues.append(Issue(
                    severity="warning",
                    category="performance",
                    line=idx,
                    message="DataFrame.iteritems() is deprecated and slow.",
                    suggestion="Use .items() or vectorized operations.",
                ))
            # Chained indexing (df["a"]["b"] or df[cond][col])
            if re.search(r"\w+\[.+?\]\[.+?\]", line) and "df" in line.lower():
                result.issues.append(Issue(
                    severity="warning",
                    category="performance",
                    line=idx,
                    message="Possible chained indexing on DataFrame.",
                    suggestion="Use .loc[] or .iloc[] to avoid SettingWithCopyWarning.",
                ))

    # String concatenation in a loop
    in_loop = False
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith(("for ", "while ")):
            in_loop = True
        elif in_loop and stripped and not stripped[0].isspace() and not line[0].isspace():
            # Rough heuristic: a non-indented line after loop ends the loop
            in_loop = False
        if in_loop and re.search(r"\w+\s*\+=\s*['\"]", line):
            result.issues.append(Issue(
                severity="info",
                category="performance",
                line=idx,
                message="String concatenation with += inside a loop.",
                suggestion="Collect pieces in a list and use ''.join() at the end.",
            ))

    # -- Type hints usage check ----------------------------------------------

    func_defs_all = list(re.finditer(
        r"def\s+\w+\s*\(([^)]*)\)\s*(->)?", code
    ))
    funcs_without_return_type = 0
    funcs_without_param_types = 0
    for m in func_defs_all:
        params = m.group(1)
        has_return = m.group(2) is not None
        if not has_return:
            funcs_without_return_type += 1
        # Check param type hints (skip 'self' and 'cls')
        param_list = [p.strip() for p in params.split(",") if p.strip()]
        param_list = [p for p in param_list if p not in ("self", "cls")
                      and not p.startswith("*")]
        for p in param_list:
            if ":" not in p:
                funcs_without_param_types += 1
                break

    total_funcs = len(func_defs_all)
    if total_funcs > 0:
        if funcs_without_return_type > 0:
            result.issues.append(Issue(
                severity="info",
                category="type-hints",
                line=0,
                message=f"{funcs_without_return_type}/{total_funcs} functions lack return type hints.",
                suggestion="Add return type annotations (-> type) for better maintainability.",
            ))
        if funcs_without_param_types > 0:
            result.issues.append(Issue(
                severity="info",
                category="type-hints",
                line=0,
                message=f"{funcs_without_param_types}/{total_funcs} functions have untyped parameters.",
                suggestion="Add parameter type annotations for clarity.",
            ))

    # -- Documentation quality -----------------------------------------------

    funcs_without_docstring = 0
    for i, (start, name) in enumerate(func_starts):
        # The line after def should be a docstring (triple quotes)
        body_start = start + 1
        if body_start < len(lines):
            first_body = lines[body_start].strip()
            if not (first_body.startswith('"""') or first_body.startswith("'''")):
                funcs_without_docstring += 1
    if funcs_without_docstring > 0 and total_funcs > 0:
        result.issues.append(Issue(
            severity="info",
            category="documentation",
            line=0,
            message=f"{funcs_without_docstring}/{total_funcs} functions are missing docstrings.",
            suggestion="Add docstrings describing purpose, args, and return values.",
        ))

    # Module-level docstring
    first_non_empty = ""
    for line in lines:
        stripped = line.strip()
        if stripped:
            first_non_empty = stripped
            break
    if first_non_empty and not (first_non_empty.startswith('"""')
                                 or first_non_empty.startswith("'''")
                                 or first_non_empty.startswith("#!")):
        # Allow shebang or encoding declaration before docstring
        if not first_non_empty.startswith("# -*-"):
            result.issues.append(Issue(
                severity="info",
                category="documentation",
                line=1,
                message="Module-level docstring is missing.",
                suggestion="Add a docstring at the top of the module describing its purpose.",
            ))

    # -- Common anti-patterns ------------------------------------------------

    # Bare except
    for idx, line in enumerate(lines, start=1):
        if re.search(r"\bexcept\s*:", line):
            result.issues.append(Issue(
                severity="warning",
                category="anti-pattern",
                line=idx,
                message="Bare 'except:' catches all exceptions including SystemExit and KeyboardInterrupt.",
                suggestion="Catch specific exceptions, or at minimum use 'except Exception:'.",
            ))

    # Mutable default arguments
    mutable_default = re.compile(
        r"def\s+\w+\s*\([^)]*:\s*\w*\s*=\s*(\[\]|\{\}|set\(\)|list\(\)|dict\(\))",
    )
    for m in mutable_default.finditer(code):
        line_no = code[:m.start()].count("\n") + 1
        result.issues.append(Issue(
            severity="warning",
            category="anti-pattern",
            line=line_no,
            message=f"Mutable default argument ({m.group(1)}) in function definition.",
            suggestion="Use None as default and create the mutable object inside the function.",
        ))

    # Global variable usage
    for idx, line in enumerate(lines, start=1):
        if re.match(r"\s+global\s+\w+", line):
            result.issues.append(Issue(
                severity="info",
                category="anti-pattern",
                line=idx,
                message="Use of 'global' keyword.",
                suggestion="Consider passing values as function parameters or using a class.",
            ))

    # -- Complexity scoring --------------------------------------------------

    func_count = total_funcs
    class_count = len(re.findall(r"^class\s+", code, re.MULTILINE))
    import_count = len(re.findall(r"^(?:from|import)\s+", code, re.MULTILINE))
    loc = sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))

    complexity = (
        func_count * 1
        + class_count * 2
        + max_indent
        + (loc // 50)  # 1 point per 50 lines
        + len([i for i in result.issues if i.severity == "warning"]) * 1
    )
    result.complexity_score = complexity

    # -- Summary -------------------------------------------------------------
    error_count = sum(1 for i in result.issues if i.severity == "error")
    warning_count = sum(1 for i in result.issues if i.severity == "warning")
    info_count = sum(1 for i in result.issues if i.severity == "info")
    result.summary = (
        f"Python review: {error_count} errors, {warning_count} warnings, "
        f"{info_count} info -- complexity score {complexity}"
    )
    logger.info("Python review complete: %s", result.summary)
    return result


# ---------------------------------------------------------------------------
# Integration helpers
# ---------------------------------------------------------------------------

def review_solution(file_path: str) -> ReviewResult:
    """Auto-detect language from file extension and run the appropriate review.

    Args:
        file_path: Path to the file to review.

    Returns:
        A ReviewResult from the appropriate reviewer.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is not supported.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    code = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()

    if suffix == ".sql":
        logger.info("Detected SQL file: %s", file_path)
        return review_sql(code, file_path)
    elif suffix == ".py":
        logger.info("Detected Python file: %s", file_path)
        return review_python(code, file_path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}  (expected .sql or .py)")


def generate_report(reviews: list[ReviewResult]) -> None:
    """Print a formatted report for one or more review results using rich.

    Args:
        reviews: List of ReviewResult objects to include in the report.
    """
    for review in reviews:
        # Header panel
        lang_label = review.language.upper()
        header_text = Text()
        header_text.append(f"Code Review: ", style="bold")
        header_text.append(f"{review.file_path}", style="cyan")
        header_text.append(f"  [{lang_label}]", style="bold magenta")
        console.print(Panel(header_text, expand=False, border_style="blue"))

        if not review.issues:
            console.print("  [green]No issues found -- looks good![/green]\n")
        else:
            # Issues table
            table = Table(
                box=box.ROUNDED,
                show_header=True,
                header_style="bold",
                title="Issues",
                title_style="bold",
            )
            table.add_column("Sev", style="bold", width=8)
            table.add_column("Line", justify="right", width=6)
            table.add_column("Category", width=14)
            table.add_column("Message", min_width=40)
            table.add_column("Suggestion", min_width=30)

            severity_styles = {
                "error": "bold red",
                "warning": "yellow",
                "info": "dim",
            }

            for issue in review.issues:
                sev_style = severity_styles.get(issue.severity, "")
                line_str = str(issue.line) if issue.line > 0 else "-"
                table.add_row(
                    Text(issue.severity.upper(), style=sev_style),
                    line_str,
                    issue.category,
                    issue.message,
                    issue.suggestion,
                )

            console.print(table)

        # Summary panel
        error_count = sum(1 for i in review.issues if i.severity == "error")
        warning_count = sum(1 for i in review.issues if i.severity == "warning")
        info_count = sum(1 for i in review.issues if i.severity == "info")

        summary_parts = []
        if error_count:
            summary_parts.append(f"[red]{error_count} errors[/red]")
        if warning_count:
            summary_parts.append(f"[yellow]{warning_count} warnings[/yellow]")
        if info_count:
            summary_parts.append(f"[dim]{info_count} info[/dim]")
        if not summary_parts:
            summary_parts.append("[green]clean[/green]")

        summary_line = " | ".join(summary_parts)
        summary_line += f"  --  complexity score: [bold]{review.complexity_score}[/bold]"

        console.print(Panel(summary_line, title="Summary", expand=False, border_style="blue"))
        console.print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point for the code reviewer."""
    parser = argparse.ArgumentParser(
        description="Automated code reviewer for SQL and Python files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python utils/code_reviewer.py my_query.sql\n"
            "  python utils/code_reviewer.py solution.py\n"
            "  python utils/code_reviewer.py file1.sql file2.py\n"
        ),
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="One or more .sql or .py files to review.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose (DEBUG) logging.",
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    reviews: list[ReviewResult] = []
    for file_path in args.files:
        try:
            result = review_solution(file_path)
            reviews.append(result)
        except FileNotFoundError as exc:
            logger.error("File not found: %s", exc)
        except ValueError as exc:
            logger.error("Unsupported file: %s", exc)
        except Exception as exc:
            logger.error("Unexpected error reviewing %s: %s", file_path, exc)

    if reviews:
        generate_report(reviews)
    else:
        logger.warning("No files were successfully reviewed.")


if __name__ == "__main__":
    main()
