# -*- coding: utf-8 -*-
"""
Problem: Custom sorting for complex data scenarios

Difficulty: Medium
Estimated Time: 15 minutes
Topics: sorted, key functions, multi-key sorting, stable sort, custom comparisons

Sorting is deceptively important in data engineering -- from ordering results
to partitioning data to merge operations.

Tasks:
1. Multi-key sorting with mixed ascending/descending
2. Custom sort key for natural string ordering
3. Sort with priority tiers
"""

from typing import List, Dict, Any, Tuple, Callable


def multi_key_sort(
    records: List[Dict[str, Any]],
    sort_keys: List[Tuple[str, bool]]
) -> List[Dict[str, Any]]:
    """
    Sort records by multiple keys with independent ascending/descending per key.

    Args:
        records: List of dictionaries to sort
        sort_keys: List of (field_name, ascending) tuples.
                   First tuple is the primary sort key.
                   True = ascending, False = descending.

    Returns:
        Sorted list of records.

    Example:
        sort_keys = [('department', True), ('salary', False)]
        Sorts by department ascending, then salary descending within each department.
    """
    # TODO: Implement your solution here
    # Hint: You can use sorted() with a key function that returns a tuple.
    # For descending numeric fields, negate the value in the tuple.
    # For descending string fields, use a helper approach.
    pass


def natural_sort(strings: List[str]) -> List[str]:
    """
    Sort strings in natural order (numbers within strings sort numerically).

    Standard sort: ['item1', 'item10', 'item2', 'item9']
    Natural sort:  ['item1', 'item2', 'item9', 'item10']

    Args:
        strings: List of strings to sort

    Returns:
        Naturally sorted list of strings.
    """
    # TODO: Implement your solution here
    # Hint: Split each string into text and number parts, convert numbers to int
    import re
    pass


def priority_sort(
    tasks: List[Dict[str, Any]],
    priority_order: List[str]
) -> List[Dict[str, Any]]:
    """
    Sort tasks by a custom priority ordering, then by name within each priority.

    Args:
        tasks: List of task dicts with at least 'name' and 'priority' keys
        priority_order: List defining priority from highest to lowest.
                        e.g., ['critical', 'high', 'medium', 'low']
                        Items with priorities not in this list go to the end.

    Returns:
        Sorted list of tasks.
    """
    # TODO: Implement your solution here
    pass


def sort_by_dependency(
    items: List[str],
    dependencies: Dict[str, List[str]]
) -> List[str]:
    """
    Sort items so that dependencies come before dependents (simple topological hint).

    This is a simplified version -- just sort so items with fewer dependencies come first,
    breaking ties alphabetically.

    Args:
        items: List of item names
        dependencies: Dict mapping item -> list of items it depends on

    Returns:
        Sorted list where items with fewer dependencies come first.
        Ties are broken alphabetically.
    """
    # TODO: Implement your solution here
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_multi_key_sort():
    """Test multi-key sorting."""
    records = [
        {'name': 'Alice', 'dept': 'Engineering', 'salary': 120000},
        {'name': 'Bob', 'dept': 'Engineering', 'salary': 80000},
        {'name': 'Charlie', 'dept': 'Marketing', 'salary': 95000},
        {'name': 'Diana', 'dept': 'Engineering', 'salary': 115000},
        {'name': 'Eve', 'dept': 'Marketing', 'salary': 65000}
    ]

    # Sort by dept ascending, then salary descending
    result = multi_key_sort(records, [('dept', True), ('salary', False)])

    assert result[0]['name'] == 'Alice', f"First should be Alice (Eng, highest salary), got {result[0]['name']}"
    assert result[1]['name'] == 'Diana', f"Second should be Diana (Eng, second salary), got {result[1]['name']}"
    assert result[2]['name'] == 'Bob', f"Third should be Bob (Eng, lowest salary), got {result[2]['name']}"
    assert result[3]['name'] == 'Charlie', f"Fourth should be Charlie (Mkt, higher salary), got {result[3]['name']}"

    print("PASS: Multi-key sorting works correctly")


def test_natural_sort():
    """Test natural string sorting."""
    items = ['file10.txt', 'file2.txt', 'file1.txt', 'file20.txt', 'file3.txt']
    result = natural_sort(items)

    expected = ['file1.txt', 'file2.txt', 'file3.txt', 'file10.txt', 'file20.txt']
    assert result == expected, f"Expected {expected}, got {result}"

    # Test with mixed prefixes
    mixed = ['item1', 'thing2', 'item10', 'thing1', 'item2']
    result_mixed = natural_sort(mixed)
    expected_mixed = ['item1', 'item2', 'item10', 'thing1', 'thing2']
    assert result_mixed == expected_mixed, f"Expected {expected_mixed}, got {result_mixed}"

    print("PASS: Natural sort works correctly")


def test_priority_sort():
    """Test priority-based sorting."""
    tasks = [
        {'name': 'Deploy hotfix', 'priority': 'critical'},
        {'name': 'Update docs', 'priority': 'low'},
        {'name': 'Fix bug', 'priority': 'high'},
        {'name': 'Add feature', 'priority': 'medium'},
        {'name': 'Review PR', 'priority': 'high'},
        {'name': 'Unknown task', 'priority': 'unknown'}
    ]

    result = priority_sort(tasks, ['critical', 'high', 'medium', 'low'])

    assert result[0]['name'] == 'Deploy hotfix', f"First should be critical task, got {result[0]['name']}"
    assert result[1]['priority'] == 'high', f"Second should be high priority, got {result[1]['priority']}"
    assert result[-1]['priority'] == 'unknown', f"Last should be unknown priority, got {result[-1]['priority']}"

    # Within same priority, should be sorted by name
    high_tasks = [t for t in result if t['priority'] == 'high']
    assert high_tasks[0]['name'] == 'Fix bug', f"High tasks should be alphabetical: {high_tasks}"

    print("PASS: Priority sort works correctly")


def test_sort_by_dependency():
    """Test dependency-based sorting."""
    items = ['deploy', 'build', 'test', 'lint']
    dependencies = {
        'deploy': ['build', 'test'],
        'build': ['lint'],
        'test': ['build'],
        'lint': []
    }

    result = sort_by_dependency(items, dependencies)

    assert result[0] == 'lint', f"lint has 0 deps, should be first. Got {result[0]}"
    assert result[-1] == 'deploy', f"deploy has 2 deps, should be last. Got {result[-1]}"

    print("PASS: Dependency-based sorting works correctly")


if __name__ == "__main__":
    test_multi_key_sort()
    test_natural_sort()
    test_priority_sort()
    test_sort_by_dependency()
    print("\nAll tests passed! Great job!")
