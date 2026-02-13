# -*- coding: utf-8 -*-
"""
Problem: Master dictionary operations for data processing

Difficulty: Easy
Estimated Time: 15 minutes
Topics: dict comprehensions, merging, nested dicts, defaultdict, Counter

Dictionaries are the backbone of data processing in Python.
These exercises cover patterns used daily in data engineering.

Tasks:
1. Invert a dictionary (swap keys and values)
2. Merge multiple dicts with conflict resolution
3. Flatten nested dictionaries
4. Group records by a key using defaultdict
"""

from typing import List, Dict, Any, Optional
from collections import defaultdict


def invert_dict(d: Dict[str, int]) -> Dict[int, List[str]]:
    """
    Invert a dictionary: values become keys, keys become lists of values.

    Since multiple keys may map to the same value, the inverted dict maps
    each value to a list of original keys (sorted alphabetically).

    Args:
        d: Dictionary mapping strings to integers.

    Returns:
        Inverted dictionary mapping integers to sorted lists of strings.

    Example:
        {'a': 1, 'b': 2, 'c': 1} -> {1: ['a', 'c'], 2: ['b']}
    """
    # TODO: Implement your solution here
    pass


def merge_dicts_with_priority(dicts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge multiple dictionaries. Later dicts have higher priority for conflicts.

    Args:
        dicts: List of dictionaries to merge. Later entries override earlier ones.

    Returns:
        Single merged dictionary.

    Example:
        [{'a': 1, 'b': 2}, {'b': 3, 'c': 4}] -> {'a': 1, 'b': 3, 'c': 4}
    """
    # TODO: Implement your solution here
    pass


def flatten_nested_dict(
    d: Dict[str, Any],
    separator: str = '.',
    prefix: str = ''
) -> Dict[str, Any]:
    """
    Flatten a nested dictionary into a single level with dotted keys.

    Args:
        d: Nested dictionary
        separator: String to join nested keys (default: '.')
        prefix: Current prefix for recursion (default: '')

    Returns:
        Flat dictionary with dotted key paths.

    Example:
        {'a': {'b': 1, 'c': {'d': 2}}, 'e': 3}
        -> {'a.b': 1, 'a.c.d': 2, 'e': 3}
    """
    # TODO: Implement your solution here (use recursion)
    pass


def group_by_key(records: List[Dict[str, Any]], key: str) -> Dict[Any, List[Dict[str, Any]]]:
    """
    Group a list of records by a specified key.

    Args:
        records: List of dictionaries
        key: Key to group by

    Returns:
        Dictionary mapping each unique value of 'key' to a list of records
        with that value. The key itself should still be in each record.

    Example:
        records = [{'dept': 'eng', 'name': 'Alice'}, {'dept': 'eng', 'name': 'Bob'},
                   {'dept': 'sales', 'name': 'Charlie'}]
        group_by_key(records, 'dept') ->
        {'eng': [{'dept': 'eng', 'name': 'Alice'}, {'dept': 'eng', 'name': 'Bob'}],
         'sales': [{'dept': 'sales', 'name': 'Charlie'}]}
    """
    # TODO: Implement using defaultdict
    pass


# ============ TESTS (DO NOT MODIFY) ============

def test_invert_dict():
    """Test dictionary inversion."""
    result = invert_dict({'a': 1, 'b': 2, 'c': 1})
    assert result == {1: ['a', 'c'], 2: ['b']}, f"Got {result}"

    result_empty = invert_dict({})
    assert result_empty == {}, f"Empty dict should return empty dict, got {result_empty}"

    result_single = invert_dict({'x': 10})
    assert result_single == {10: ['x']}, f"Got {result_single}"

    print("PASS: Dictionary inversion works correctly")


def test_merge_dicts():
    """Test dictionary merging with priority."""
    result = merge_dicts_with_priority([
        {'a': 1, 'b': 2},
        {'b': 3, 'c': 4},
        {'c': 5, 'd': 6}
    ])
    assert result == {'a': 1, 'b': 3, 'c': 5, 'd': 6}, f"Got {result}"

    result_empty = merge_dicts_with_priority([])
    assert result_empty == {}, f"Empty list should return empty dict, got {result_empty}"

    print("PASS: Dictionary merging works correctly")


def test_flatten_nested_dict():
    """Test nested dictionary flattening."""
    nested = {'a': {'b': 1, 'c': {'d': 2}}, 'e': 3}
    result = flatten_nested_dict(nested)
    assert result == {'a.b': 1, 'a.c.d': 2, 'e': 3}, f"Got {result}"

    # Test with custom separator
    result_underscore = flatten_nested_dict(nested, separator='_')
    assert result_underscore == {'a_b': 1, 'a_c_d': 2, 'e': 3}, f"Got {result_underscore}"

    # Test flat dict (no nesting)
    result_flat = flatten_nested_dict({'x': 1, 'y': 2})
    assert result_flat == {'x': 1, 'y': 2}, f"Got {result_flat}"

    print("PASS: Nested dict flattening works correctly")


def test_group_by_key():
    """Test grouping records by key."""
    records = [
        {'dept': 'eng', 'name': 'Alice', 'salary': 100000},
        {'dept': 'eng', 'name': 'Bob', 'salary': 90000},
        {'dept': 'sales', 'name': 'Charlie', 'salary': 80000},
        {'dept': 'sales', 'name': 'Diana', 'salary': 85000},
        {'dept': 'eng', 'name': 'Eve', 'salary': 95000}
    ]

    result = group_by_key(records, 'dept')

    assert len(result) == 2, f"Expected 2 groups, got {len(result)}"
    assert len(result['eng']) == 3, f"Expected 3 engineers, got {len(result['eng'])}"
    assert len(result['sales']) == 2, f"Expected 2 sales, got {len(result['sales'])}"

    print("PASS: Group by key works correctly")


if __name__ == "__main__":
    test_invert_dict()
    test_merge_dicts()
    test_flatten_nested_dict()
    test_group_by_key()
    print("\nAll tests passed! Great job!")
