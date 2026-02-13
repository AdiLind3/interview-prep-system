# -*- coding: utf-8 -*-
"""
Problem: Advanced groupby operations on employee performance data

Difficulty: Medium
Estimated Time: 20 minutes
Topics: groupby, agg, transform, multi-level grouping, named aggregation

Given employee performance data:
1. Multi-level groupby with named aggregations
2. Use transform to add group-level statistics back to each row
3. Apply multiple aggregation functions to different columns

These patterns appear constantly in data pipelines and analytics queries.
"""

import pandas as pd
import numpy as np
from typing import Dict, List


def department_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a summary of each department using named aggregation.

    Args:
        df: DataFrame with columns [employee_id, name, department, role,
            salary, performance_score, years_experience]

    Returns:
        DataFrame indexed by department with columns:
        - employee_count: number of employees
        - avg_salary: mean salary, rounded to 2 decimals
        - max_salary: maximum salary
        - avg_performance: mean performance_score, rounded to 2 decimals
        - total_experience: sum of years_experience
        Sorted by department name.
    """
    # TODO: Implement your solution here
    pass


def add_group_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add department-level statistics to each row using transform.

    Args:
        df: DataFrame with columns [employee_id, name, department, salary, performance_score]

    Returns:
        Original DataFrame with additional columns:
        - dept_avg_salary: average salary in the employee's department
        - dept_avg_performance: average performance in the employee's department
        - salary_vs_dept_avg: employee salary minus dept_avg_salary
        All new columns rounded to 2 decimal places.
    """
    # TODO: Implement your solution here
    pass


def top_performers_per_group(
    df: pd.DataFrame,
    group_col: str,
    score_col: str,
    n: int = 1
) -> pd.DataFrame:
    """
    Find the top N performers in each group.

    Args:
        df: Input DataFrame
        group_col: Column to group by
        score_col: Column to rank by (higher is better)
        n: Number of top performers per group

    Returns:
        DataFrame containing only the top N rows per group,
        sorted by group_col then by score_col descending.
        Reset the index.
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def _make_test_data() -> pd.DataFrame:
    """Create test employee data."""
    return pd.DataFrame({
        'employee_id': range(1, 11),
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve',
                 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack'],
        'department': ['Engineering', 'Engineering', 'Engineering', 'Marketing', 'Marketing',
                       'Marketing', 'Sales', 'Sales', 'Sales', 'Sales'],
        'role': ['Senior', 'Junior', 'Senior', 'Manager', 'Junior',
                 'Senior', 'Manager', 'Senior', 'Junior', 'Junior'],
        'salary': [120000, 80000, 115000, 95000, 65000,
                   90000, 100000, 85000, 60000, 62000],
        'performance_score': [4.5, 3.8, 4.2, 4.0, 3.5,
                              4.3, 4.7, 3.9, 3.6, 4.1],
        'years_experience': [8, 2, 7, 6, 1, 5, 10, 4, 1, 2]
    })


def test_department_summary():
    """Test department summary aggregation."""
    df = _make_test_data()
    result = department_summary(df)

    assert len(result) == 3, f"Expected 3 departments, got {len(result)}"
    assert result.loc['Engineering', 'employee_count'] == 3, "Engineering should have 3 employees"
    assert result.loc['Engineering', 'avg_salary'] == round((120000 + 80000 + 115000) / 3, 2), \
        "Engineering avg salary is incorrect"
    assert result.loc['Sales', 'total_experience'] == 17, \
        f"Sales total experience should be 17, got {result.loc['Sales', 'total_experience']}"

    print("PASS: Department summary works correctly")


def test_add_group_stats():
    """Test adding group statistics via transform."""
    df = _make_test_data()
    result = add_group_stats(df)

    assert 'dept_avg_salary' in result.columns, "Missing 'dept_avg_salary' column"
    assert 'salary_vs_dept_avg' in result.columns, "Missing 'salary_vs_dept_avg' column"

    # Alice is in Engineering, avg salary = (120000+80000+115000)/3 = 105000
    alice = result[result['name'] == 'Alice'].iloc[0]
    assert alice['dept_avg_salary'] == round(105000, 2), \
        f"Alice dept_avg_salary should be 105000.0, got {alice['dept_avg_salary']}"
    assert alice['salary_vs_dept_avg'] == round(120000 - 105000, 2), \
        f"Alice salary_vs_dept_avg should be 15000.0, got {alice['salary_vs_dept_avg']}"

    print("PASS: Group stats added correctly")


def test_top_performers():
    """Test top performers per group."""
    df = _make_test_data()
    result = top_performers_per_group(df, 'department', 'performance_score', n=1)

    assert len(result) == 3, f"Expected 3 rows (1 per department), got {len(result)}"

    eng_top = result[result['department'] == 'Engineering'].iloc[0]
    assert eng_top['name'] == 'Alice', f"Top Engineering performer should be Alice, got {eng_top['name']}"

    sales_top = result[result['department'] == 'Sales'].iloc[0]
    assert sales_top['name'] == 'Grace', f"Top Sales performer should be Grace, got {sales_top['name']}"

    print("PASS: Top performers per group works correctly")


if __name__ == "__main__":
    test_department_summary()
    test_add_group_stats()
    test_top_performers()
    print("\nAll tests passed! Great job!")
